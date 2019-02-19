from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple([
            (enum.value, name) for name, enum in cls.__members__.items()
        ])

    @classmethod
    def get_description(cls, value):
        return dict(cls.choices()).get(value)


class IntEnum(int, BaseEnum):
    pass


class CharEnum(str, BaseEnum):
    pass


class OrderStatus(IntEnum):
    NEW = 10
    ACCEPTED = 20
    STARTED = 30
    FINISHED = 40
    CANCELED = 50
    TIMEOUT = 60


class OrderEventStatus(IntEnum):
    NEW = 10
    ACCEPTED = 20
    REJECTED = 30
    TIMEOUT = 40


class MessageEvent(CharEnum):
    # drivers
    NEW_ORDER = 'new_order'
    CANCELED = 'canceled'
    DISMISSED = 'dismissed'

    # clients
    NO_DRIVERS = 'no_drivers'
    ACCEPTED = 'accepted'
    ARRIVED = 'arrived'
    STARTED = 'started'
    FINISHED = 'finished'
