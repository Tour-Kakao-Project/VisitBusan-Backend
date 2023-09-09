from django.db import models

SCHEDULE_STYLE = [
    ("1", "부지런하게"),
    ("2", "여유롭게"),
]

ACTIVITY_STYLE = [
    ("1", "액티비티_여행"),
    ("2", "잔잔한_여행"),
]

ACCOMMODATION_STYLE = [
    ("1", "시설"),
    ("2", "가성비"),
]

ATTRACTION_STYLE = [
    ("1", "유명한명소"),
    ("2", "덜유명한명소"),
]

TRAVEL_KEYWORD = [
    ("1", "한류"),
    ("2", "K-POP"),
    ("3", "첫 부산여행"),
    ("4", "전통문화"),
    ("5", "인스타그램"),
    ("6", "바다"),
]


class CourseStyle(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    choice_data = models.JSONField(null=True)  # 선택지 데이터
    """
    ages: "",
    disablity: "yes/no",
    total_people_cnt: int,
    schedule: "",
    activity: "",
    food: "",
    accommodation: "",
    attration: "",
    keyword: ""
    """

    start_date = models.DateField()
    end_date = models.DateField()
    place = models.JSONField(null=True)  # 사용자가 가고자 하는 장소 list
