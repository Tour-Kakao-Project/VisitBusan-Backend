import requests

from visit_busan.settings import env


def get_place_id(longitude, latitude, keyword):
    headers = {
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=100&language=ko&keyword={keyword}&key={env("GOOGLE_API_KEY")}'
    response = requests.get(headers=headers, url=url)
    return response.json()


def get_place_detail(place_id):
    headers = {
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={env("GOOGLE_API_KEY")}'
    response = requests.get(headers=headers, url=url)
    return response.json()
