from django.contrib import admin
from course.model.index import *


@admin.register(Course)
class MemberAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Course._meta.get_fields()]


@admin.register(CourseStyle)
class MemberAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CourseStyle._meta.get_fields()]
