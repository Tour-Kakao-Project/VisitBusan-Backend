from enum import Enum


class Traveling_Companion(Enum):
    INFANT = ("Infant", "1")
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

    def get_traveling_company(string_key):
        for ele in list(Traveling_Companion):
            if ele.string_key == string_key:
                return ele


class Schedule_Style(Enum):
    DILIGENTLY = ("Diligently", "1")
    LEISURELY = ("Leisurely", "2")

    def __init__(self, string_key, db_index):
        self.string_key = string_key
        self.db_index = db_index

    def __str__(self):
        return self.error_code

    def get_schedule_style(string_key):
        for ele in list(Schedule_Style):
            if ele.string_key == string_key:
                return ele


class Activity_Style(Enum):
    WALKING = ("Walking", "1")
    DYNAMIC = ("Dynamic", "2")
    CALM = ("Calm", "3")

    def __init__(self, string_key, db_index):
        self.string_key = string_key
        self.db_index = db_index

    def __str__(self):
        return self.error_code

    def get_activity_style(string_key):
        for ele in list(Activity_Style):
            if ele.string_key == string_key:
                return ele


class Attraction_Style(Enum):
    URBAN = ("Urban", "1")
    NATURE = ("Nature", "2")

    def __init__(self, string_key, db_index):
        self.string_key = string_key
        self.db_index = db_index

    def __str__(self):
        return self.error_code

    def get_attraction_style(string_key):
        for ele in list(Attraction_Style):
            if ele.string_key == string_key:
                return ele


class Travel_KeyWord(Enum):
    K_POP = ("K-POP", "1")
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

    def get_travel_keyword(string_key):
        for ele in list(Travel_KeyWord):
            if ele.string_key == string_key:
                return ele
