from rest_framework import permissions

from team8_server.constants import Periods
from team8_server.models import ServerState


def IsPeriod(p):
    class _IsPeriod(permissions.BasePermission):
        period = p

        def has_object_permission(self, request, view, obj):
            return self.has_permission(request, view)

        def has_permission(self, request, view):
            return request.method in permissions.SAFE_METHODS or int(ServerState.object().period) == self.period

    if p == Periods.CART:
        _IsPeriod.message = '장바구니 기간이 아닙니다.'
    elif p == Periods.REGISTRATION:
        _IsPeriod.message = '수강신청 기간이 아닙니다.'

    return _IsPeriod
