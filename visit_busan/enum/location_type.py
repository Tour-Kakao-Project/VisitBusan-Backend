from enum import Enum


class Location_Type(Enum):
    MUSEUM = "MUSEUM"
    RESTARTANT = "RESTARTANT"
    YACHT = "YACHT"

    def __init__(self, key):
        self.key = key

    def __str__(self):
        return self.key
