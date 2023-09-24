from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

import datetime

from .model.index import *
from .service.index import *
from .serializers import *

from course.service.google_api.google_place_api import *


class CourseResult(APIView):
    @api_view(["POST"])
    @permission_classes([AllowAny])
    def find_course_result(request):
        try:
            member = request.user.member
            start_date = datetime.datetime.strptime(
                request.data["start_date"], "%Y-%m-%d"
            ).date()
            end_date = datetime.datetime.strptime(
                request.data["end_date"], "%Y-%m-%d"
            ).date()
            place = request.data["place"]
            choice_result = request.data["choice_result"]

            # Save selected course style
            course_style = CourseStyle.objects.create(
                choice_data=choice_result,
                start_date=start_date,
                end_date=end_date,
                place=place,
            )
            course_style.save()

            # Find course data
            course_result = create_course_result(course_style)

            # Save course result
            course = Course.objects.create(
                course_style=course_style,
                member=member,
                start_date=course_style.start_date,
                end_date=course_style.end_date,
                departure=course_result["departure"],
                destination=course_result["destination"],
                total_people_cnt=course_result["total_people_cnt"],
                course_detail=course_result["course_detail"],
            )

            return Response(
                {"data": CourseSerializers(course).data}, status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)


@api_view(["GET"])
@permission_classes([AllowAny])
def test_google(request):
    address = "부산광역시 해운대구 중동 산 3-9"
    result = get_place_id("129.196262235317", "35.1641953523606", "청사포 다릿돌전망대")
    place_id = result["results"][0]["place_id"]
    return Response({"result": place_id}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def test_detail(request):
    place_id = "ChIJUQsDVhuNaDURJo5GeByloeQ"
    result = get_place_detail(place_id)
    location_result = result["result"]
    location_rating = location_result["rating"]
    location_url = location_result["url"]
    location_user_ratings_total = location_result["user_ratings_total"]
    return Response({"result": location_result}, status=status.HTTP_200_OK)
