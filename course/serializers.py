from rest_framework import serializers

from .model.index import *


class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "start_date",
            "end_date",
            "departure",
            "destination",
            "total_people_cnt",
            "course_detail",
        ]
