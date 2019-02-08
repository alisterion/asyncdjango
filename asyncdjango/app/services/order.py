from asyncdjango.app.choices import OrderEventStatus, OrderStatus
from asyncdjango.app.models import Order, OrderEvent
from asyncdjango.app.services.queue import QueueService
from asyncdjango.celery import app


@app.task
def check_order_status(event_id):
    try:
        event = OrderEvent.objects.get(pk=event_id)
    except OrderEvent.DoesNotExist:
        print('Order event {} does not exist'.format(event_id))
        return

    if event.status == OrderEventStatus.NEW.value:
        # TODO: send dismiss event to driver
        event.set_timeout()

    if event.order.status == OrderStatus.NEW.value:
        OrderService(event=event).confirm()


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
            else QueueService(self.event.driver).next()

        if not driver:
            # TODO: send event 'no_drivers' to user
            self.order.set_timeout()
            return

        event = self._create_event(driver)
        # TODO: send async event to next driver in queue

        # run async task to check statuses after 30 secs
        check_order_status.apply_async(args=(event.id,), countdown=30)

    def cancel(self):
        # TODO: send cancel event to drivers
        self.order.set_canceled()

    def accept(self):
        # TODO: send accept event to client
        self.order.set_accepted()
        self.event.set_accepted()

    def reject(self):
        self.confirm()
        self.event.set_rejected()

    def arrive(self):
        # TODO: send arrive event to client
        pass

    def start(self):
        # TODO: send start event to client
        self.order.set_started()

    def finish(self):
        # TODO: send finish event with price to client
        pass

    def confirm_finish(self):
        self.order.set_finished()
