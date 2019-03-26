from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user_role = models.CharField(max_length=12)
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __unicode__(self):
        return self.username
