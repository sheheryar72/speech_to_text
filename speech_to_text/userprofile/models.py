from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    sex = models.CharField(max_length=8)
    phone_no = models.CharField(max_length=15)
    country = models.CharField(max_length=30)

    class Meta:
        managed = True
        db_table = 'UserProfile'
    def __str__(self):
        return self.user.username