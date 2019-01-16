from asyncdjango.app.choices import OrderEventStatus
from asyncdjango.app.models import Order, OrderEvent
from asyncdjango.app.services.queue import QueueService


class OrderService(object):
    def __init__(self, order=None, event=None):
        self.event = event
        self.order = order or (event and event.order)

    def _create_event(self, driver):
        event, _ = OrderEvent.objects.get_or_create(
            order=self.order, driver=driver)
        return event

    def confirm(self):
        first_driver = QueueService.first()
        if not first_driver:
            # TODO: send order to free space or send event 'no_drivers' to user
            pass
        event = self._create_event(first_driver)
        # TODO: send async event to first driver in queue
        # TODO: run async task to check statuses after 30 secs

    def cancel(self):
        # TODO:
        pass

    def accept(self):
        # TODO:
        pass

    def reject(self):
        # TODO:
        pass

    def arrive(self):
        # TODO:
        pass

    def start(self):
        # TODO:
        pass

    def finish(self):
        # TODO:
        pass

    def confirm_finish(self):
        # TODO:
        pass

    def check_event_timeout(self):
        if self.event.status == OrderEventStatus.NEW.value:
            # TODO: send 'dismiss' to event.driver
            next_driver = QueueService(self.event.driver).next()
            if not next_driver:
                # TODO: send order to free space or send event 'no_drivers' to user
                pass
            event = self._create_event(next_driver)
            # TODO: send async event to first driver in queue
            # TODO: run async task to check statuses after 30 secs
        pass
