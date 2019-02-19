Taxi app (Prototype of async app in django)
--

### Set up

0. install python3.5 virtualenv rabbitmq-server python3-dev
1. mkvirtualenv -p /usr/bin/python3.5 asyncdjango
2. pip install django djangorestframework django-rest-swagger channels==1.1.8 asgi_redis celery django-extensions django-ordered-model Pillow
3. django-admin startproject asyncdjango
4. cd asyncdjango/asyncdjango/
5. django-admin startapp app
6. follow instructions:
    * https://www.django-rest-framework.org/
    * https://django-rest-swagger.readthedocs.io/en/latest/
    * https://channels.readthedocs.io/en/1.x/installation.html
    * http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
7. Models: 
    * Driver
        - car
    * Client
        - phone
    * Queue
        - driver
    * Order
        - client
        - driver
        - description
        - price
        - comment
        - status
    * OrderEvent
        - order
        - driver
        - status
8. Choices:
    * OrderStatus
        - new
        - accepted
        - started
        - finished
        - canceled
        - timeout
    * OrderEventStatus:
        - new
        - accepted
        - rejected
        - timeout
    * MessageEvent:
        - new_order
        - canceled
        - dismissed
        - no_drivers
        - accepted
        - arrived
        - started
        - finished
9. Serializers:
    * UserSerializer
    * ClientSerializer
    * DriverSerializer
    * QueueSerializer
    * OrderSerializer
    * OrderFinishSerializer
    * OrderEventSerializer
    * OrderFinishSerializer
10. Permissions:
    * IsDriver
    * IsAuthorOfOrder
    * IsAuthorOfOrderEvent
11. Services:
    * QueueService:
        * join
        * left
        * first
        * next
    * Messenger:
        * send_event
    * OrderService:
        * confirm
        * cancel
        * accept
        * reject
        * arrive
        * start
        * finish
        * confirm_finish
12. ViewSet:
    * QueueViewSet
        * join
        * left
    * OrderViewSet
        * retrieve
        * list
        * create
        * cancel
        * confirm_finish
    * OrderEventViewSet
        * retrieve
        * list
        * accept
        * reject
        * arrive
        * start
        * finish
13. Urls
14. Consumers:
    * ws_connect
    * ws_disconnect
