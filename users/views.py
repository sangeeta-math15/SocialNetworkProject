from django.db.models import Q
from .serializers import LoginSerializer, UserSearchSerializer, UserSerializer, FriendRequestSerializer
from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from django_ratelimit.decorators import ratelimit
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from .models import User, FriendRequest
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
            API for user login
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(user, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """
            API for user logout
        """
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserSearchView(generics.ListAPIView):
    """
    API for searching users by name or email with pagination

    """
    serializer_class = UserSearchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.all()
        search_term = self.request.query_params.get('search', None)

        if search_term:
            if '@' in search_term:
                queryset = queryset.filter(email__iexact=search_term)
            else:
                # Otherwise, search for the term in the username, first name, or last name
                queryset = queryset.filter(
                    Q(username__icontains=search_term) |
                    Q(first_name__icontains=search_term) |
                    Q(last_name__icontains=search_term)
                )
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FriendRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling friend requests

    """
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='user_or_ip', rate='3/m', method='POST'))
    def create(self, request, *args, **kwargs):
        from_user = request.user
        to_user_id = request.data.get('to_user_id')

        # Validate to_user_id
        if not to_user_id:
            return Response({'detail': 'to_user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Prevent sending friend request to self
        if from_user == to_user:
            return Response({'detail': 'You cannot send a friend request to yourself'},
                            status=status.HTTP_400_BAD_REQUEST)

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response({'detail': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new friend request
        try:
            friend_request = FriendRequest(from_user=from_user, to_user=to_user)
            friend_request.save()
            return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['put'])
    def accept_request(self, request, pk=None):
        user = request.user
        try:
            friend_request = FriendRequest.objects.get(id=pk)
            if friend_request.to_user != user or friend_request.status != 'pending':
                return Response({'detail': 'Friend request not found or not pending'}, status=status.HTTP_404_NOT_FOUND)
        except FriendRequest.DoesNotExist:
            return Response({'detail': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)

        # Accept the friend request
        try:
            friend_request.status = 'accepted'
            friend_request.save()
            user.friends.add(friend_request.from_user)
            friend_request.from_user.friends.add(user)
            return Response({'status': 'Friend request accepted'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['put'])
    def reject_request(self, request, pk=None):
        user = request.user
        try:
            friend_request = FriendRequest.objects.get(id=pk)
            if friend_request.to_user != user or friend_request.status != 'pending':
                return Response({'detail': 'Friend request not found or not pending'}, status=status.HTTP_404_NOT_FOUND)
        except FriendRequest.DoesNotExist:
            return Response({'detail': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)

        # Reject the friend request
        try:
            friend_request.status = 'rejected'
            friend_request.save()
            return Response({'status': 'Friend request rejected'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def list_friends(self, request):
        user = request.user
        try:
            accepted_friend_requests = FriendRequest.objects.filter(
                Q(from_user=user, status='accepted') | Q(to_user=user, status='accepted')
            )

            friends_ids = set()
            for friend_request in accepted_friend_requests:
                if friend_request.from_user == user:
                    friends_ids.add(friend_request.to_user.id)
                else:
                    friends_ids.add(friend_request.from_user.id)

            friends = User.objects.filter(id__in=friends_ids)
            serializer = UserSerializer(friends, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def list_pending_requests(self, request):
        user = request.user
        try:
            pending_requests = FriendRequest.objects.filter(to_user=user, status='pending')
            serializer = FriendRequestSerializer(pending_requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
