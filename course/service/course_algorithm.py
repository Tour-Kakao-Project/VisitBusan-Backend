from datetime import timedelta

from visit_busan.enum.index import *
from course.model.vo.CoureseLocationVo import CourseLocationVo
from course.service.kakao_api.kakao_location_api import *


def create_course_result(course_style):
    # course style step 1
    traveling_companion = [
        Traveling_Companion.get_traveling_company(ele["name"])
        for ele in course_style.choice_data["traveling_companion"]
    ]
    is_disablity = True if course_style.choice_data["disablity"] == "yes" else False
    total_people_cnt = course_style.choice_data["total_people_cnt"]

    # course style step 2
    schedule_style = Schedule_Style.get_schedule_style(
        course_style.choice_data["schedule"]
    )
    activity_style = Activity_Style.get_activity_style(
        course_style.choice_data["activity"]
    )
    attration_style = Attraction_Style.get_attraction_style(
        course_style.choice_data["attration"]
    )
    keyword = [
        Travel_KeyWord.get_travel_keyword(ele["name"])
        for ele in course_style.choice_data["keyword"]
    ]

    # course style step 3
    start_date = course_style.start_date
    end_date = course_style.end_date

    # course style step 4
    place = [
        Busan_Location.get_busan_location(ele["name"]) for ele in course_style.place
    ]

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
        "departure": place[0].string_key,
        "destination": place[-1].string_key,
        "total_people_cnt": total_people_cnt,
        "course_detail": course_detail,
    }

    return course_result


def get_longitude_and_latitude(locations):
    for courseVO in locations:
        address = courseVO.location_address
        longitude, latitude = request_longitude_and_latitude(address)

        courseVO.setLongitude_setLatitude(longitude, latitude)
