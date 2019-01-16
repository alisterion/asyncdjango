from rest_framework import permissions

from asyncdjango.app.models import Order, OrderEvent
from asyncdjango.app.services.user import user_service


class IsDriver(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super(IsDriver, self).has_permission(request, view) and \
               user_service.has_driver_role(request.user)


class IsAuthorOfOrder(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: Order):
        return obj.client == request.user


class IsAuthorOfOrderEvent(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: OrderEvent):
        return obj.driver == request.user
