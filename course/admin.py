from django.contrib import admin
from course.model.index import *


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["id", "member", "departure", "destination"]


@admin.register(CourseStyle)
class CourseStyleAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "choice_data",
        "start_date",
        "end_date",
        "place",
        "updated_at",
    ]


@admin.register(CourseData)
class CourseDataAdmin(admin.ModelAdmin):
    list_display = ["id"]
