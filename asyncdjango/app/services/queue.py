from django.db.models import Max

from asyncdjango.app.models import Queue


class QueueService(object):
    @staticmethod
    def first():
        queue = Queue.objects.first()
        return queue and queue.driver

    @staticmethod
    def join(driver):
        max_order = Queue.objects.aggregate(max=Max('order'))['max']
        queue, _ = Queue.objects.get_or_create(
            driver=driver,
            defaults={'order': max_order + 1}
        )
        return queue

    @staticmethod
    def left(driver):
        Queue.objects.filter(driver=driver).delete()

    @staticmethod
    def next(driver):
        try:
            queue = Queue.objects.get(driver=driver)
        except Queue.DoesNotExist:
            return
        return queue.next().driver
