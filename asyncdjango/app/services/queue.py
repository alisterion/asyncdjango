from django.db.models import Max

from asyncdjango.app.models import Queue


class QueueService(object):

    def __init__(self, driver):
        self.driver = driver

    @classmethod
    def first(cls):
        queue = Queue.objects.first()
        return queue and queue.driver

    def join(self):
        max_order = Queue.objects.aggregate(max=Max('order'))['max']
        queue, _ = Queue.objects.get_or_create(
            driver=self.driver,
            defaults={'order': max_order + 1}
        )
        return queue

    def left(self):
        Queue.objects.filter(driver=self.driver).delete()

    def next(self):
        try:
            queue = Queue.objects.get(driver=self.driver)
        except Queue.DoesNotExist:
            return
        return queue.next().driver
