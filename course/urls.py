from django.urls import path

from . import views

urlpatterns = [
    path("result", views.CourseResult.find_course_result),
    path("", views.get_all_course),
    # test
    path("google-place", views.test_google),
    path("google-detail", views.test_detail),
]
