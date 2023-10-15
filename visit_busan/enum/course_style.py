from enum import Enum


class Traveling_Company(Enum):
    INFANT = ("Infannt", "1")
    CHILD = ("Child", "2")
    TEENS = ("Teens", "3")
    E20S = ("20s", "4")
    E30S = ("30s", "5")
    E40S = ("40s", "6")
    E50S = ("50s", "7")
    E60S = ("60s", "8")
    E70S_OR = ("70sOr", "9")

    def __init__(self, string_key, db_index):
        self.string_key = string_key
        self.db_index = db_index

    def __str__(self):
        return self.error_code


class Schedule_Style(Enum):
    DILIGENTLY = ("Diligently", "1")
    LEISURELY = ("Leisurely", "2")

    def __init__(self, string_key, db_index):
        self.string_key = string_key
        self.db_index = db_index

    def __str__(self):
        return self.error_code


class Activity_Style(Enum):
    WALKING = ("Walking", "1")
    DYNAMIC = ("Dynamic", "2")
    CALM = ("Calm", "3")

    def __init__(self, string_key, db_index):
        self.string_key = string_key
        self.db_index = db_index

    def __str__(self):
        return self.error_code


class Attraction_Style(Enum):
    URBAN = ("Urban", "1")
    NATURE = ("Nature", "2")

    def __init__(self, string_key, db_index):
        self.string_key = string_key
        self.db_index = db_index

    def __str__(self):
        return self.error_code


class Travel_KeyWord(Enum):
    K_POP = ("K-pop", "1")
    With_FAMILY = ("With Family", "2")
    TRADITIONAL = ("Traditional", "3")
    WITH_FRIEND = ("With friend", "4")
    INSTAGRAMABLE = ("Instagramable", "5")
    OCEAN = ("Ocean", "6")

    def __init__(self, string_key, db_index):
        self.string_key = string_key
        self.db_index = db_index

    def __str__(self):
        return self.error_code
