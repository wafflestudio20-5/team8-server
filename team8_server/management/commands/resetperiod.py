from django.core.management.base import BaseCommand
from django.db.models import Count, F

from snu_course.models import Course
from team8_server.constants import Periods


class Command(BaseCommand):
    help = '모든 UserToCourse의 ManyToMany 관계들을 초기화 합니다.'
    periods = Periods.to_dict()

    def change_period(self, state):
        state.period = Periods.PRE_SEMESTER
        state.save()
        self.stdout.write(self.style.SUCCESS('장바구니 전 상태로 변경되었습니다.'))

    def reset_pending(self):
        courses = Course.objects.filter(pending=True)
        course_count = courses.count()
        courses.update(pending=False)
        self.stdout.write(self.style.SUCCESS(f"{course_count}개의 pending이 초기화되었습니다."))

    def handle(self, *args, **kwargs):
        from team8_server.models import ServerState
        state = ServerState.objects.get()
        self.change_period(state)
        self.reset_pending()

        from snu_student.models import UserToCourse

        courses = UserToCourse.objects.all()
        delete_count = courses.count()
        courses.delete()

        self.stdout.write(self.style.SUCCESS(f"{delete_count}개의 관계가 삭제되었습니다."))

        self.stdout.write(self.style.SUCCESS('초기화가 완료되었습니다.'))


