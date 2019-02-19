from asyncdjango.app.choices import OrderStatus, OrderEventStatus, MessageEvent
from asyncdjango.app.models import OrderEvent
from asyncdjango.app.services.messenger import Messenger
from asyncdjango.celery import app


@app.task
def check_order_status(event_id):
    try:
        event = OrderEvent.objects.get(pk=event_id)
    except OrderEvent.DoesNotExist:
        print('Order event {} does not exist'.format(event_id))
        return

    if event.status == OrderEventStatus.NEW.value:
        Messenger.send_event(
            event.driver,
            MessageEvent.DISMISSED.value,
            {'event_id': event.id}
        )
        event.set_timeout()

    if event.order.status == OrderStatus.NEW.value:
        # confirm to send event to next driver
        from asyncdjango.app.services.order import OrderService
        OrderService(event=event).confirm()
