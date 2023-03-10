from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.db.models import Q

from snu_student.models import User, UserToCourse
from team8_server.constants import CourseSorts

DAYS_OF_WEEK = (
    ('MON', 'Monday'),
    ('TUE', 'Tuesday'),
    ('WED', 'Wednesday'),
    ('THU', 'Thursday'),
    ('FRI', 'Friday'),
    ('SAT', 'Saturday'),
    ('SUN', 'Sunday'),
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
    time = models.CharField(default='', max_length=100, blank=True)
    credit = models.IntegerField(validators=[MinValueValidator(1)])
    lecture = models.IntegerField()
    lab = models.IntegerField()
    form = models.CharField(default='', max_length=100, blank=True)
    classroom = models.CharField(default='', max_length=100, blank=True)
    pending = models.BooleanField(default=False, editable=False)
    # parsed_time

    @property
    def interest(self):
        return UserToCourse.objects.filter(course=self, sort=CourseSorts.INTEREST).count()

    @property
    def cart(self):
        return UserToCourse.objects.filter(course=self, sort=CourseSorts.CART).count()

    @property
    def current(self):
        return UserToCourse.objects.filter(course=self, sort=CourseSorts.REGISTERED).count()

    def can_insert_into(self, course_list):
        if not course_list or not course_list.exists() or not self.timeinfo_set.exists() : return True
        q = Q()
        for course in course_list:
            for timeinfo in self.timeinfo_set.all():
                q |= Q(course=course, day=timeinfo.day, start_time__lt=timeinfo.end_time, end_time__gt=timeinfo.start_time)
        return not TimeInfo.objects.filter(q).exists()


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

    rate = models.IntegerField(default=0)
    semester = models.CharField(max_length=100, null=True)


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(null=True, blank=True)
    is_updated = models.BooleanField(default=False)

    content = models.TextField()

