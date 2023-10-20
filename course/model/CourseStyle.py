from django.db import models


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
    attration: "",
    keyword: ""
    """

    start_date = models.DateField()
    end_date = models.DateField()
    place = models.JSONField(null=True)  # 사용자가 가고자 하는 장소 list

    class Meta:
        db_table = "course_styles"
