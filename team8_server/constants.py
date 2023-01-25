class Enum:
    @classmethod
    def to_dict(cls):
        return {getattr(cls, attr): attr for attr in dir(cls) if not callable(getattr(cls, attr)) if not attr.startswith('__')}

    @classmethod
    def choices(cls):
        return tuple(cls.to_dict().items())


class Periods(Enum):
    PRE_SEMESTER = 0
    CART = 1
    CART_CONFIRMATION = 2
    REGISTRATION = 3
    SEMESTER = 4


class CourseSorts(Enum):
    INTEREST = 0
    CART = 1
    REGISTERED = 2
