from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager

class UserModel(AbstractUser):
    class Meta:
        db_table = "my_user"

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.CharField(max_length=100, null=False, blank=False, unique=True)
    name = models.CharField(max_length=30, default='', null=False, blank=False)
    phone = models.CharField(max_length=30, null=False, blank=False)
    birthdate = models.DateField(null=False, blank=False)
    gender = models.CharField(max_length=10, null=False, blank=False)

    def create_superuser(self, username, password):
        if not username:
            raise ValueError("User must have a name")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            username = self.normalize_username(username)
        )
        user.username= username
        user.set_password(password)
        return user