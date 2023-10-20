from enum import Enum


class Busan_Location(Enum):
    Gijang = ("Gijang", "1")
    Dongnae = ("Dongnae", "2")
    Haeundae = ("Haeundae", "3")
    Seomyeon = ("Seomyeon", "4")
    Gwangan = ("Gwangan", "5")
    Sasang_Gangseo = ("Sasang/Gangseo", "6")
    Yeongdo = ("Yeongdo", "7")

    def __init__(self, string_key, db_index):
        self.string_key = string_key
        self.db_index = db_index

    def __str__(self):
        return self.error_code

    def get_busan_location(string_key):
        for ele in list(Busan_Location):
            if ele.string_key == string_key:
                return ele
