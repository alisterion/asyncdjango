from channels import Group
from channels.auth import channel_session_user
from channels.sessions import channel_session

from asyncdjango.app.channel_auth import token_from_http
from asyncdjango.app.utils import set_user_session


def add_user_to_channel_group(user, message):
    Group('user_%d' % user.pk).add(message.reply_channel)


def remove_user_from_channel_group(user, message):
    Group('user_%d' % user.pk).discard(message.reply_channel)


@channel_session
@token_from_http
def ws_connect(message, **kwargs):
    message.reply_channel.send({"accept": True}, immediately=True)
    user = message.user

    if user.is_authenticated():
        add_user_to_channel_group(user, message)
        set_user_session(user, message.channel_session)

    return message


@channel_session
@channel_session_user
def ws_disconnect(message, **kwargs):
    user = message.user
    if user and user.is_authenticated:
        remove_user_from_channel_group(user, message)
