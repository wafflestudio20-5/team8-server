import os
import sys

import django

os.chdir('.')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'team8_server.settings')
django.setup()


from django.db.models import Count, F
from snu_course.models import Course
from snu_student.models import UserToCourse
from team8_server.constants import CourseSorts


pending_courses = UserToCourse.objects\
    .filter(sort=CourseSorts.CART)\
    .values('course')\
    .annotate(Count('user'))\
    .filter(user__count__gt=F('course__maximum'))\
    .values_list('course', flat=True)


queryset = Course.objects.filter(id__in=pending_courses)
queryset.update(pending=True)
