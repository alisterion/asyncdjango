from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import action

from asyncdjango.app.models import Order
from asyncdjango.app.serializers import OrderSerializer


class OrderViewSet(viewsets.ReadOnlyModelViewSet,
                   mixins.CreateModelMixin):
    queryset = Order.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order = super(OrderViewSet, self).perform_create(serializer)
        # TODO: send async events to first driver in queue
