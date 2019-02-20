from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel
from ordered_model.models import OrderedModel

from asyncdjango.app.choices import OrderStatus, OrderEventStatus


class Driver(User):
    class Meta(User.Meta):
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'

    car = models.ImageField(blank=True)


class Client(User):
    class Meta(User.Meta):
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

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
    status = models.PositiveIntegerField(
        choices=OrderStatus.choices(),
        default=OrderStatus.NEW.value
    )

    def __str__(self):
        return 'Order {}: {}'.format(self.id, self.client)

    def _set_status(self, status):
        self.status = status.value
        self.save(update_fields=['status'])

    def set_accepted(self):
        self._set_status(OrderStatus.ACCEPTED)

    def set_started(self):
        self._set_status(OrderStatus.STARTED)

    def set_finished(self):
        self._set_status(OrderStatus.FINISHED)

    def set_canceled(self):
        self._set_status(OrderStatus.CANCELED)

    def set_timeout(self):
        self._set_status(OrderStatus.TIMEOUT)


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
        choices=OrderEventStatus.choices(),
        default=OrderEventStatus.NEW.value
    )

    def __str__(self):
        return 'Order event {}: {}'.format(self.id, self.driver)

    def _set_status(self, status):
        self.status = status.value
        self.save(update_fields=['status'])

    def set_accepted(self):
        self._set_status(OrderEventStatus.ACCEPTED)

    def set_rejected(self):
        self._set_status(OrderEventStatus.REJECTED)

    def set_timeout(self):
        self._set_status(OrderEventStatus.TIMEOUT)
