from django.conf import settings
from django.db import models

from asyncdjango.app.choices import OrderStatus, OrderEventStatus


class Queue(models.Model):
    driver = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE)
    number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{}: {}'.format(self.driver, self.number)


class Order(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='my_orders')
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='orders', null=True, blank=True)
    description = models.TextField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    status = models.PositiveIntegerField(choices=OrderStatus.choices())


class OrderEvent(models.Model):
    order = models.ForeignKey(Order, models.CASCADE)
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    status = models.PositiveIntegerField(choices=OrderEventStatus.choices())
