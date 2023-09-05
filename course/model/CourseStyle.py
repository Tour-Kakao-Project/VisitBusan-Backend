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

    # schedule_style = models.CharField(max_length=50, choices=SCHEDULE_STYLE)
    # activity_style = models.CharField(max_length=50, choices=ACTIVITY_STYLE)
    # accommodation_style = models.CharField(max_length=50, choices=ACCOMMODATION_STYLE)
    # attraction_style = models.CharField(max_length=50, choices=ATTRACTION_STYLE)
    # travel_keyword = models.CharField(max_length=50, choices=TRAVEL_KEYWORD)

    start_date = models.DateField()
    end_date = models.DateField()
    place = models.JSONField(null=True)  # 사용자가 가고자 하는 장소 list
