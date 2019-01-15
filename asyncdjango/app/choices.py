from enum import Enum


class IntEnum(int, Enum):
    @classmethod
    def choices(cls):
        return tuple([
            (enum.value, name) for name, enum in cls.__members__.items()
        ])

    @classmethod
    def get_description(cls, value):
        return dict(cls.choices()).get(value)


class OrderStatus(IntEnum):
    NEW = 10
    ACCEPTED = 20
    STARTED = 30
    FINISHED = 40
    CANCELED = 50
    NO_DRIVERS = 60


class OrderEventStatus(IntEnum):
    NEW = 10
    ACCEPTED = 20
    REJECTED = 30
    TIMEOUT = 40
