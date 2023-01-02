from django.db import models
from django.core.validators import MinValueValidator, RegexValidator


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