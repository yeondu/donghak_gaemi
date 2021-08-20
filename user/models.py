from django.db import models

class UserModel(models.Model):
    class Meta:
        db_table = "my_user"

    user_id = models.IntegerField(null=False, blank=False)
    email = models.CharField(max_length=50, null=False, blank=False)
    pwd = models.CharField(max_length=50, null=False, blank=False)
    username = models.CharField(max_length=30, null=False, blank=False)
    phone = models.CharField(max_length=30, null=False, blank=False)
    birthdate = models.DateField(null=False, blank=False)
    gender = models.CharField(max_length=10, null=False, blank=False)
