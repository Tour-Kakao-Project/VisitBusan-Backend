from django.urls import path

from . import views

urlpatterns = [
    path("result", views.CourseResult.find_course_result),
]
