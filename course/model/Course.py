from django.db import models

from course.model.CourseStyle import CourseStyle


class Course(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    course_style = models.ForeignKey(CourseStyle, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    departure = models.CharField(max_length=50)  # 출발지
    destination = models.CharField(max_length=50)  # 도착지
    course_detail = models.JSONField()
