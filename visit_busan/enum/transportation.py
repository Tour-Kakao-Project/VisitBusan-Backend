from enum import Enum


class Transportation(Enum):
    WALK = "WALK"
    CAR = "CAR"
    SUBWAY = "SUBWAY"
    BUS = "BUS"

    def __init__(self, key):
        self.key = key

    def __str__(self):
        return self.key
