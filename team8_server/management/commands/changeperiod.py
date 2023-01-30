from django.core.management.base import BaseCommand
from django.db.models import Count, F

from team8_server.constants import Periods


class Command(BaseCommand):
    help = '현재 기간을 변경. \n' \
           'PRE_SEMESTER = 0 \n ' \
           'CART = 1 \n ' \
           'CART_CONFIRMATION = 2 \n' \
           'REGISTRATION = 3 \n ' \
           'SEMESTER = 4 \n ' \
           '의 순서로 변경됨'
    periods = Periods.to_dict()

    def change_period(self, state):
        state.period = (int(state.period) + 1) % 5
        state.save()
        self.stdout.write(self.style.SUCCESS(self.periods[state.period] + ' 기간으로 변경되었습니다.'))

    def handle(self, *args, **kwargs):
        from team8_server.models import ServerState
        state = ServerState.objects.get()
        self.change_period(state)

        if state.period == Periods.CART_CONFIRMATION:
            from snu_course.models import Course
            from snu_student.models import UserToCourse
            from team8_server.constants import CourseSorts

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

            self.stdout.write(self.style.SUCCESS(f"{pending_count}개의 강좌가 장바구니 보류강좌로 전환되었습니다.<br>{registered_count}개의 강좌가 장바구니 확정되어 수강신청되었습니다."))
