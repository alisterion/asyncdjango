from asyncdjango.app.settings import DRIVER_GROUP


class UserService(object):
    @classmethod
    def has_driver_role(cls, user):
        return user.objects.groups.filter(name=DRIVER_GROUP).exists()

user_service = UserService()
