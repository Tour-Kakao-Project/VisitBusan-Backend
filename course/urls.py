from django.urls import path

from . import views

urlpatterns = [
    path("result", views.CourseResult.find_course_result),
    # test
    path("google-place", views.test_google),
    path("google-detail", views.test_detail),
]
