from enum import IntEnum


class OrderStatusCode(IntEnum):
    CONFIRMED = 0
    PREPARED = 1
    FINISHED = 2
    CANCELLED = 3
