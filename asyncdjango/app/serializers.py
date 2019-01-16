from django.contrib.auth import get_user_model
from rest_framework import serializers

from asyncdjango.app.models import Order, OrderEvent, Queue

User = get_user_model()


class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = ('driver', 'order', )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('client', 'description', )

    client = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )


class OrderFinishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('comment', )


class OrderEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderEvent
        fields = ('client', 'description', 'status', )

    client = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='order.client', read_only=True)
    description = serializers.CharField(
        source='order.description', read_only=True)
    status = serializers.IntegerField(read_only=True)


class OrderEventFinishSerializer(OrderEventSerializer):
    class Meta:
        model = OrderEvent
        fields = ('client', 'description', 'status', 'price', )

    price = serializers.DecimalField(
        source='order.price', decimal_places=2, max_digits=6)
