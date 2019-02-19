import json

from channels import Group


class Messenger(object):

    @staticmethod
    def send_event(user, event, data):
        group_name = 'user_%d' % user.pk
        message = {
            'event': event,
            'data': data,
        }
        Group(group_name).send(
            {'text': json.dumps(message)},
            immediately=True
        )
