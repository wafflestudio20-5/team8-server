from django.db.models import Count, F
from django.http import HttpResponse
from rest_framework import generics

from snu_course.models import Course
from snu_student.models import UserToCourse
from team8_server.constants import CourseSorts
from .constants import Periods
from .models import ServerState
from .serializers import ServerStateSerializer


def change_period(request):
    state = ServerState.object()
    if int(state.period) == Periods.CART:
        state.period = Periods.REGISTRATION
        msg = '현재 수강신청 기간입니다.'
    else:
        state.period = Periods.CART
        msg = '현재 장바구니 기간입니다.'
    state.save()
    return HttpResponse(msg)


def confirm(request):
    pending_courses = UserToCourse.objects \
        .filter(sort=CourseSorts.CART) \
        .values('course') \
        .annotate(Count('user')) \
        .filter(course__pending=False, user__count__gt=F('course__maximum')) \
        .values_list('course', flat=True)
    pending_count = pending_courses.count()

    registered_courses = UserToCourse.objects \
        .filter(sort=CourseSorts.CART) \
        .values('course') \
        .annotate(Count('user')) \
        .filter(course__pending=False, user__count__lte=F('course__maximum'))
    registered_count = registered_courses.count()

    Course.objects.filter(id__in=pending_courses).update(pending=True)
    registered_courses.update(sort=CourseSorts.REGISTERED)

    return HttpResponse(f"{pending_count}개의 강좌가 장바구니 보류강좌로 전환되었습니다.<br>{registered_count}개의 강좌가 장바구니 확정되어 수강신청되었습니다.")


class StateDetail(generics.RetrieveAPIView):
    serializer_class = ServerStateSerializer
    queryset = ServerState.objects.all()

    def get_object(self):
        return self.queryset.first()
