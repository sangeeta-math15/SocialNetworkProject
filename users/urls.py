from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserSearchView, FriendRequestViewSet, UserViewSet

router = DefaultRouter()
router.register(r'users/friend-requests', FriendRequestViewSet, basename='friend-request')
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('users/search/', UserSearchView.as_view(), name='user-search'),
    path('', include(router.urls)),
]