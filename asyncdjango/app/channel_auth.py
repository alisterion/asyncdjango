import re
from functools import wraps

from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token

TOKEN_CHECK = re.compile(r'auth_token=([\d\w]+)')


def token_from_http(func):
    """
    Checks the presence of a "token" field on the connect url and
    tries to authenticate the user based on its content.
    """
    @wraps(func)
    def inner(message, *args, **kwargs):

        try:
            query_string = message.get('query_string', message['path'])
        except (KeyError, ValueError, TypeError):
            message.reply_channel.send(
                {'close': True, 'text': 'Missed connection string'}
            )
        else:
            try:
                token = TOKEN_CHECK.findall(query_string)[0]
            except IndexError:
                token = None
            if not token:
                message.reply_channel.send(
                    {'text': "Missing token field."}
                )

            try:
                token_obj = Token.objects.get(key=token)
            except Token.DoesNotExist:
                message.user = AnonymousUser()
                message.reply_channel.send(
                    {'text': "Token not exist. Please update token."}
                )
            else:
                message.user = token_obj.user
        return func(message, *args, **kwargs)
    return inner
