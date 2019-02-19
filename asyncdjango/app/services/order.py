from asyncdjango.app.choices import MessageEvent
from asyncdjango.app.models import Order, OrderEvent
from asyncdjango.app.services.messenger import Messenger
from asyncdjango.app.services.queue import QueueService
from asyncdjango.app.tasks import check_order_status


class OrderService(object):
    def __init__(self, order=None, event=None):
        self.event = event  # type: OrderEvent
        self.order = order or (event and event.order)  # type: Order

    def _create_event(self, driver):
        event, _ = OrderEvent.objects.get_or_create(
            order=self.order, driver=driver)
        return event

    def confirm(self, first=False):
        driver = QueueService.first() \
            if first \
            else QueueService.next(self.event.driver)

        if not driver:
            Messenger.send_event(
                self.order.client,
                MessageEvent.NO_DRIVERS.value,
                {'order_id': self.order.id}
            )
            self.order.set_timeout()
            return

        event = self._create_event(driver)
        Messenger.send_event(
            driver,
            MessageEvent.NEW_ORDER.value,
            {'event_id': event.id}
        )

        # run async task to check statuses after 30 secs
        check_order_status.apply_async(args=(event.id,), countdown=30)

    def cancel(self):
        for event in self.order.events.all():
            Messenger.send_event(
                event.driver,
                MessageEvent.ACCEPTED.value,
                {'event_id': event.id}
            )
            event.set_timeout()

        self.order.set_canceled()

    def accept(self):
        Messenger.send_event(
            self.order.client,
            MessageEvent.ACCEPTED.value,
            {'order_id': self.order.id}
        )
        self.order.set_accepted()
        self.event.set_accepted()

    def reject(self):
        self.confirm()
        self.event.set_rejected()

    def arrive(self):
        Messenger.send_event(
            self.order.driver,
            MessageEvent.ARRIVED.value,
            {'order_id': self.order.id}
        )

    def start(self):
        Messenger.send_event(
            self.order.driver,
            MessageEvent.STARTED.value,
            {'order_id': self.order.id}
        )
        self.order.set_started()

    def finish(self, price):
        Messenger.send_event(
            self.order.driver,
            MessageEvent.FINISHED.value,
            {'order_id': self.order.id, 'price': price}
        )

    def confirm_finish(self):
        self.order.set_finished()
