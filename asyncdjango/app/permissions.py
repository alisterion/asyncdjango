from rest_framework import permissions

from asyncdjango.app.models import Order, OrderEvent, Driver


class IsDriver(permissions.IsAuthenticated):
    def is_driver(self, user):
        try:
            return bool(user.driver)
        except Driver.DoesNotExist:
            return False

    def has_permission(self, request, view):
        return super(IsDriver, self).has_permission(request, view) and \
               self.is_driver(request.user)


class IsAuthorOfOrder(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: Order):
        return obj.client == request.user


class IsAuthorOfOrderEvent(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: OrderEvent):
        return obj.driver == request.user
