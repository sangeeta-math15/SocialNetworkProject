from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    friends = models.ManyToManyField('self', symmetrical=False)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='send_request', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_request', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,
                              choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')),
                              default='pending')
