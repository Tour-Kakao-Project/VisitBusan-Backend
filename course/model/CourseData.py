from django.db import models

TRAVELING_COMPANION_STYLE = []

SCHEDULE_STYLE = [
    ("1", "Diligently"),
    ("2", "Leisurely"),
]

ACTIVITY_STYLE = [("1", "Walking"), ("2", "Dynamic"), ("3", "Calm")]

ATTRACTION_STYLE = [
    ("1", "Urban"),
    ("2", "Nature"),
]

TRAVEL_KEYWORD = [
    ("1", "한류"),
    ("2", "K-POP"),
    ("3", "첫 부산여행"),
    ("4", "전통문화"),
    ("5", "인스타그램"),
    ("6", "바다"),
]


class CourseData(models.Model):
    traveling_companion = models.CharField(
        max_length=50, choices=TRAVELING_COMPANION_STYLE
    )
    is_disablity = models.BooleanField()

    schedule = models.CharField(max_length=50, choices=SCHEDULE_STYLE)
    activity = models.CharField(max_length=50, choices=ACTIVITY_STYLE)
    attraction = models.CharField(max_length=50, choices=ATTRACTION_STYLE)
    keyword = models.CharField(max_length=50, choices=TRAVEL_KEYWORD)

    days = models.IntegerField(null=True)

    location = models.CharField(max_length=50)

    detail = models.JSONField()

    class Meta:
        db_table = "course_data"
