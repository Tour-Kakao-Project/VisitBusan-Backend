import requests

from visit_busan.settings import env


def request_longitude_and_latitude(address):
    header = {"Authorization": f'KakaoAK {env("KAKAO_REST_API_KEY")}'}
    url = f"https://dapi.kakao.com/v2/local/search/address.JSON?query={address}"

    response = requests.get(url=url, headers=header)
    response_json = response.json()

    if response_json["meta"]["total_count"] > 0:
        address_detail = response_json["documents"][0]["address"]
        return address_detail["x"], address_detail["y"]
    else:
        print("좌표 요청하는 것을 실패했습니다.")
