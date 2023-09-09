from django.contrib import admin
from course.model.index import *


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Course._meta.get_fields()]


@admin.register(CourseStyle)
class CourseStyleAdmin(admin.ModelAdmin):
    list_display = ["choice_data", "start_date", "end_date", "place", "updated_at"]
