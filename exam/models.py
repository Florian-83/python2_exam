from django.db import models
from .helper import hash_password

class User(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    mail = models.EmailField(max_length=50, unique=True)
    is_teacher = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.password = hash_password(self.password)
        super().save(*args, **kwargs)

class Session(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class Answer(models.Model):
    mail = models.EmailField(max_length=50, unique=True)
    first_login = models.DateTimeField(null=True)
    percent = models.IntegerField(null=True)
    difficulty = models.CharField(max_length=50, null=True)
    progression = models.CharField(max_length=50, null=True)














# class user(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.CharField(max_length=50, unique=True)
#     password = models.CharField(max_length=50)

# class survey(models.Model):
#     name = models.CharField(max_length=50)
#     start_date = models.DateTimeField()
#     end_date = models.DateTimeField()
#     status = models.BooleanField()

# class answers(models.Model):
#     percent = models.CharField(max_length=50)
#     difficulty = models.CharField(max_length=50)
#     progression = models.CharField(max_length=50)
#     user = models.CharField(max_length=50)
#     send_date = models.DateTimeField()

