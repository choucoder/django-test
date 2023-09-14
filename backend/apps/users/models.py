from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    SUPER_ADMIN = 1
    STAFF = 2
    CUSTOMER = 3

    USER_TYPE_CHOICES = (
        (SUPER_ADMIN, 'super admin'),
        (STAFF, 'staffs'),
        (CUSTOMER, 'customer'),
    )

    email = models.EmailField(
        unique=True,
        error_messages={
            "unique": "A user with that email already exists.",
        },
    )
    is_customer = models.BooleanField('Customer user', default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def get_tokens(self):
        refresh = RefreshToken.for_user(self)
        data = {}
        data['access'] = str(refresh.access_token)
        data['refresh'] = str(refresh)
        return data

    def __str__(self):
        return "{id}, {email}, {username}, {user_type}".format(
            id=self.id,
            email=self.email,
            username=self.username,
            user_type=self.get_user_type_display()
        )
