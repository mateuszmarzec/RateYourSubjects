from django.db import models


# Create your models here.

class UserData(models.Model):
    login = models.CharField(max_length=30, unique=True)
    password_hash = models.CharField(max_length=100)
    password_salt = models.CharField(max_length=100)
    email = models.EmailField()
    is_active = models.BooleanField(default=False)
    last_login = models.DateField(null=True)

    def __str__(self):
        return '%s %s %s %s' % (self.login, self.is_active, self.email, self.last_login)

