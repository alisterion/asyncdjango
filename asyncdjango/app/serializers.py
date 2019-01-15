from django.contrib.auth import get_user_model
from rest_framework import serializers

from asyncdjango.app.models import Order

User = get_user_model()


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('client', 'description', )

    client = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
