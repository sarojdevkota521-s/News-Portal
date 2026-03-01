from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(max_length= 255, unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class PasswordReset(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id=models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"password reset for {self.user.username} at {self.created_when }"