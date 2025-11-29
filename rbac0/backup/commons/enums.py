import enum
from enum import Enum

@enum.unique
class Gender(Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3