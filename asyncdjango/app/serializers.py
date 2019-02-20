from rest_framework import serializers

from asyncdjango.app.models import Order, OrderEvent, Queue, Client, Driver


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'phone', )


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ('first_name', 'last_name', 'car', )


class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = ('driver', 'order', )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('client', 'description', 'driver', 'status', )
        read_only_fields = ('client', 'driver', 'status', )

    driver = DriverSerializer()
    client = ClientSerializer()


class OrderFinishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('comment', )


class OrderEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderEvent
        fields = ('client', 'description', 'status', )
        read_only_fields = ('client', 'description', 'status', )

    client = ClientSerializer(source='order.client')
    description = serializers.CharField(source='order.description')


class OrderEventFinishSerializer(OrderEventSerializer):
    class Meta(OrderEventSerializer.Meta):
        model = OrderEvent
        fields = ('client', 'description', 'status', 'price', )

    price = serializers.DecimalField(
        source='order.price', decimal_places=2, max_digits=6)
