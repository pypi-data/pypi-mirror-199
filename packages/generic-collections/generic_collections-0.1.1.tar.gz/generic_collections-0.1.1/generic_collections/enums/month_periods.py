from enum import IntEnum


class MonthsPeriodEnum(IntEnum):
    monthly: int = 1
    bimonthly: int = 2
    quarterly: int = 3
    four_moth: int = 4
    semester: int = 6
    yearly: int = 12