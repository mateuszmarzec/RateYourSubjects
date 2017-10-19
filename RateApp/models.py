from django.db import models
from django.utils.timezone import now
from . import fields

# Create your models here.

### To authenticate
class UserData(models.Model):
    login = models.CharField(max_length=30, unique=True)
    password_hash = models.CharField(max_length=100)
    password_salt = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    last_login = models.DateField(null=True)
    registration_date = models.DateField(default=now())
    has_usable_password = models.BooleanField(default=True)

    def __str__(self):
        return '%s %s %s %s' % (self.login, self.is_active, self.email, self.last_login)

    def get_email_field_name(cls):
        try:
            return cls.EMAIL_FIELD
        except AttributeError:
            return 'email'


### Main Content
class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    department = models.CharField(max_length=50)

    def __str__(self):
        return '%s %s %s' % (self.first_name, self.last, self.department)

class Subject(models.Model):
    name = models.CharField(max_length=30, unique=True)
    shortcut = models.CharField(max_length=6, unique=True)
    leaders = models.ManyToManyField(Teacher)

    def __str__(self):
        return '%s %s' % (self.name, self.leader)

class Rate(models.Model):
    how_interesting = fields.IntegerRangeField(max_value=100, min_value=0)
    how_easy = fields.IntegerRangeField(max_value=100, min_value=0)
    description = models.CharField(max_length=500)
    date = models.DateField(default=now())
    user = models.ForeignKey('UserData', on_delete=models.CASCADE)
    leader = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.id, self.dates)





