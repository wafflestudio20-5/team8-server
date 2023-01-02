from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator

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


class Course(models.Model):
    class_number_validator = RegexValidator(regex=r'^[0-9]{3}$')

    name = models.CharField(max_length=100)
    curriculum = models.CharField(max_length=100)
    professor = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    department = models.CharField(default='', max_length=100, blank=True)
    course = models.CharField(max_length=100)
    grade = models.IntegerField(default=0, blank=True)
    number = models.CharField(max_length=100)
    class_number = models.IntegerField(validators=[class_number_validator])
    maximum = models.IntegerField()
    current = models.IntegerField(default=0, blank=True)
    time = models.CharField(default='', max_length=100, blank=True)
    credit = models.IntegerField(validators=[MinValueValidator(1)])
    lecture = models.IntegerField()
    lab = models.IntegerField()
    form = models.CharField(default='', max_length=100, blank=True)
    classroom = models.CharField(default='', max_length=100, blank=True)
    cart = models.IntegerField(default=0, blank=True)
    rate = models.IntegerField(null=True)
    # parsed_time