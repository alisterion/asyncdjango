Taxi app (Prototype of async app in django)
--

### Set up

0. install python3.5 virtualenv rabbitmq-server python3-dev
1. mkvirtualenv -p /usr/bin/python3.5 asyncdjango
2. pip install django djangorestframework channels celery django-extensions django-ordered-model
3. django-admin startproject asyncdjango
4. cd asyncdjango/asyncdjango/
5. django-admin startapp app
6. follow instructions:
    * https://www.django-rest-framework.org/
    * https://channels.readthedocs.io/en/latest/installation.html
    * http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
