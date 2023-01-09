from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


SORTS_OF_COURSE = (
    ('I', 'interest'),
    ('C', 'cart'),
    ('R', 'registered')
)


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('must have user email')
        if not name:
            raise ValueError('must have user name')
        user = self.model(
            email=self.normalize_email(email),
            name=name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email,
            password=password,
            name=name
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # student_id_validator = RegexValidator(regex=r'^([0-9]{4})-([0-9]{5})$')

    id = models.AutoField(primary_key=True)
    email = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True)
    name = models.CharField(default='', max_length=100, null=False, blank=False)
    # student_id = models.CharField(validators=[student_id_validator], default='', max_length=, null=False, blank=False)
    # college = models.CharField(default='', max_length=100, null=False, blank=False)
    # department = models.CharField(default='', max_length=100, null=False, blank=False)
    # program = models.CharField(default='', max_length=100, null=False, blank=False)
    # academic_year = models.IntegerField(validators=[MinValueValidator(1)], null=False, blank=False)
    # year_of_entrance = models.IntegerField(null=False, blank=False)
    # number_of_semesters = models.IntegerField(validators=[MinValueValidator(1)], null=False, blank=False)
    # major = models.CharField(default='', max_length=100, null=False, blank=False)
    # second_major = models.CharField(default='', max_length=100, null=True, blank=True)
    # double_major = models.CharField(default='', max_length=100, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    courses = models.ManyToManyField('snu_course.Course', related_name='users', through='UserToCourse')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)  # expiration time

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

    def __str__(self):
        return self.email


class UserToCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('snu_course.Course', on_delete=models.CASCADE)
    sort = models.CharField(max_length=1, choices=SORTS_OF_COURSE)
