from datetime import timedelta

from visit_busan.enum.index import *


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
    location = [
        {
            "location_name": "뮤지임원",
            "location_url": "https://kunst1.co.kr/museumone",
            "location_type": Location_Type.MUSEUM.key,
            "location_score": 4.2,
            "next_location_transportation_time": 6,
            "next_location_transportation": Transportation.WALK.key,
        },
        {
            "location_name": "엘룬",
            "location_url": "http://localmap.co.kr/web/splus/kmap/view.php?sigun=6260000&gugun=3360000&keyno=126&keyname=%EC%97%98%EB%A3%AC%28elune%29&keylink=3360000-101-2017-00187",
            "location_type": Location_Type.RESTARTANT.key,
            "location_score": 4.2,
            "next_location_transportation_time": 7,
            "next_location_transportation": Transportation.CAR.key,
        },
        {
            "location_name": "요트홀릭 렉셔리 요트 투어",
            "location_url": "https://www.myrealtrip.com/offers/103284",
            "location_type": Location_Type.YACHT.key,
            "location_score": 4.7,
            "next_location_transportation_time": 3,
            "next_location_transportation": Transportation.WALK.key,
        },
        {
            "location_name": "우미",
            "location_url": "https://app.catchtable.co.kr/ct/shop/umi",
            "location_score": 4.3,
            "next_location_transportation_time": 0,
            "next_location_transportation": None,
        },
    ]

    check_date = start_date
    course_detail = []
    while end_date != check_date:
        course_detail.append(
            {
                "date": check_date.strftime("%Y-%m-%d"),
                "location": location,
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
