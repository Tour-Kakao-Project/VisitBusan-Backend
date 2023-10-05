from datetime import timedelta

from visit_busan.enum.index import *
from course.model.vo.CoureseLocationVo import CourseLocationVo
from course.service.kakao_api.kakao_location_api import *


def create_course_result(course_style):
    ages = course_style.choice_data["ages"]
    disablity = course_style.choice_data["disablity"]
    total_people_cnt = course_style.choice_data["total_people_cnt"]
    schedule_style = course_style.choice_data["schedule"]
    activity_style = course_style.choice_data["activity"]
    food_style = course_style.choice_data["food"]
    accommodation_style = course_style.choice_data["accommodation"]
    attration_style = course_style.choice_data["attration"]
    keyword = course_style.choice_data["keyword"]
    start_date = course_style.start_date
    end_date = course_style.end_date
    place = course_style.place

    # TBD algorithm
    ## Test 데이터
    locations = [
        CourseLocationVo(
            "청사포다릿돌전망대",
            "https://maps.app.goo.gl/rSELDxwxMyysZ8cL7",
            "부산광역시 해운대구 중동 산 3-9",
            4.3,
            Location_Type.OBSERVATORY.key,
        ),
        CourseLocationVo(
            "해운대해변열차",
            "https://maps.app.goo.gl/BkZSVmETzetnR4ck9",
            "부산광역시 해운대구 달맞이길 62번길 13",
            4.3,
            Location_Type.ACTIVITY.key,
        ),
        CourseLocationVo(
            "해운대해수욕장‧송림공원",
            "https://maps.app.goo.gl/pEf5ZEkHaMk5Rrw17",
            "부산광역시 해운대구 해운대해변로 266",
            4.5,
            Location_Type.BEACH.key,
        ),
        CourseLocationVo(
            "부산아쿠아리움",
            "https://maps.app.goo.gl/hZW5G9cUzoTmysTR6",
            "부산광역시 영도구 전망로 24",
            4.2,
            Location_Type.AQUARIUM.key,
        ),
    ]

    get_longitude_and_latitude(locations)

    check_date = start_date
    course_detail = []
    while end_date != check_date:
        course_detail.append(
            {
                "date": check_date.strftime("%Y-%m-%d"),
                "location": [location.json for location in locations],
            }
        )

        check_date += timedelta(days=1)

    course_result = {
        "departure": place[0]["name"],
        "destination": place[-1]["name"],
        "total_people_cnt": total_people_cnt,
        "course_detail": course_detail,
    }

    return course_result


def get_longitude_and_latitude(locations):
    for courseVO in locations:
        address = courseVO.location_address
        longitude, latitude = request_longitude_and_latitude(address)

        courseVO.setLongitude_setLatitude(longitude, latitude)
