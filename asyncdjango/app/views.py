from rest_framework import viewsets, permissions, mixins, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from asyncdjango.app.models import Order, OrderEvent, Queue
from asyncdjango.app.permissions import (
    IsDriver,
    IsAuthorOfOrder,
    IsAuthorOfOrderEvent,
)
from asyncdjango.app.serializers import (
    QueueSerializer,
    OrderSerializer,
    OrderFinishSerializer,
    OrderEventSerializer,
    OrderEventFinishSerializer,
)
from asyncdjango.app.services.order import OrderService
from asyncdjango.app.services.queue import QueueService


class QueueViewSet(viewsets.GenericViewSet):
    queryset = Queue.objects.all()
    permission_classes = (IsDriver, )
    serializer_class = QueueSerializer

    @action(methods=['post'], detail=False)
    def join(self, request):
        queue = QueueService.join(request.user)
        sz = self.get_serializer(queue)
        return Response(sz.data)

    @action(methods=['delete'], detail=False)
    def left(self, request):
        QueueService.left(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(viewsets.ReadOnlyModelViewSet,
                   mixins.CreateModelMixin):
    queryset = Order.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order = super(OrderViewSet, self).perform_create(serializer)
        OrderService(order).confirm(first=True)

    @action(methods=['put'], detail=True,
            permission_classes=[IsAuthorOfOrder],
            serializer_class=serializers.Serializer)
    def cancel(self, request, *args, **kwargs):
        order = self.get_object()
        OrderService(order).cancel()
        sz = self.get_serializer(order)
        return Response(sz.data)

    @action(methods=['put'], detail=True,
            permission_classes=[IsAuthorOfOrder],
            serializer_class=OrderFinishSerializer)
    def confirm_finish(self, request, *args, **kwargs):
        order = self.get_object()
        sz = self.get_serializer(order)
        sz.save()
        OrderService(order).confirm_finish()
        return Response(sz.data)


class OrderEventViewSet(viewsets.GenericViewSet):
    queryset = OrderEvent.objects.all()
    permission_classes = (IsDriver, )
    serializer_class = OrderEventSerializer

    @action(methods=['put'], detail=True,
            permission_classes=[IsAuthorOfOrderEvent],
            serializer_class=serializers.Serializer)
    def accept(self, request, *args, **kwargs):
        event = self.get_object()
        OrderService(event=event).accept()
        sz = self.get_serializer(event)
        return Response(sz.data)

    @action(methods=['put'], detail=True,
            permission_classes=[IsAuthorOfOrderEvent],
            serializer_class=serializers.Serializer)
    def reject(self, request, *args, **kwargs):
        event = self.get_object()
        OrderService(event=event).reject()
        sz = self.get_serializer(event)
        return Response(sz.data)

    @action(methods=['put'], detail=True,
            permission_classes=[IsAuthorOfOrderEvent],
            serializer_class=serializers.Serializer)
    def arrive(self, request, *args, **kwargs):
        event = self.get_object()
        OrderService(event=event).arrive()
        sz = self.get_serializer(event)
        return Response(sz.data)

    @action(methods=['put'], detail=True,
            permission_classes=[IsAuthorOfOrderEvent],
            serializer_class=serializers.Serializer)
    def start(self, request, *args, **kwargs):
        event = self.get_object()
        OrderService(event=event).start()
        sz = self.get_serializer(event)
        return Response(sz.data)

    @action(methods=['put'], detail=True,
            permission_classes=[IsAuthorOfOrderEvent],
            serializer_class=OrderEventFinishSerializer)
    def finish(self, request, *args, **kwargs):
        event = self.get_object()
        sz = self.get_serializer(event)
        sz.save()
        OrderService(event=event).finish()
        return Response(sz.data)
