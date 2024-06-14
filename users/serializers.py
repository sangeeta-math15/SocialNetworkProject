from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import FriendRequest, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email').lower()
        password = data.get('password')
        user = User.objects.filter(email__iexact=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return {
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
            }
        raise serializers.ValidationError('Invalid credentials')


class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']
        read_only_fields = ['from_user', 'status', 'created_at']
