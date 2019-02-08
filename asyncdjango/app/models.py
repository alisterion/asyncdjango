from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TimeStampedModel
from ordered_model.models import OrderedModel

from asyncdjango.app.choices import OrderStatus, OrderEventStatus

User = get_user_model()


class Driver(User):
    car = models.ImageField(blank=True)


class Client(User):
    phone = models.CharField(max_length=20)


class Queue(OrderedModel):
    driver = models.OneToOneField(Driver, models.CASCADE)

    def __str__(self):
        return '{}: {}'.format(self.driver, self.order)


class Order(TimeStampedModel):
    client = models.ForeignKey(
        Client,
        models.CASCADE,
        related_name='my_orders'
    )
    driver = models.ForeignKey(
        Driver,
        models.CASCADE,
        related_name='orders',
        null=True,
        blank=True
    )
    description = models.TextField(max_length=255, blank=True, default='')
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )
    comment = models.TextField(max_length=255, blank=True, default='')
    status = models.PositiveIntegerField(choices=OrderStatus.choices())

    def __str__(self):
        return 'Order {}: {}'.format(self.id, self.client)


class OrderEvent(TimeStampedModel):
    order = models.ForeignKey(
        Order,
        models.CASCADE,
        related_name='events'
    )
    driver = models.ForeignKey(
        Driver,
        models.CASCADE,
        related_name='events'
    )
    status = models.PositiveIntegerField(
        choices=OrderEventStatus.choices()
    )

    def __str__(self):
        return 'Order event {}: {}'.format(self.id, self.driver)
