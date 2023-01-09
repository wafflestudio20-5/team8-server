from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

from snu_student.models import User

DAYS_OF_WEEK = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)


class Course(models.Model):
    class_number_validator = RegexValidator(regex=r'^[0-9]{3}$')

    name = models.CharField(max_length=100)
    curriculum = models.CharField(max_length=100)
    professor = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    department = models.CharField(default='', max_length=100, blank=True)
    degree = models.CharField(max_length=100)
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


class TimeInfo(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(null=True, blank=True)
    is_updated = models.BooleanField(default=False)

#    published_at = models.DateTimeField(null=True, blank=True)
#    is_published = models.BooleanField(default=False)

    title = models.CharField(max_length=100)
    content = models.TextField()

    rate = models.IntegerField(null=True, blank=True)
    semester = models.CharField(max_length=100, null=True, blank=True)


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(null=True, blank=True)
    is_updated = models.BooleanField(default=False)

    content = models.TextField()

