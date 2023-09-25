from google.oauth2 import id_token
from google.auth.transport import requests

from visit_busan.settings import env


def get_user_info(user_id_token):
    user_info = id_token.verify_oauth2_token(
        user_id_token, requests.Request(), env("GOOGLE_WEB_CLIENT_ID")
    )

    email = user_info["email"]
    given_name = user_info["given_name"]
    faily_name = user_info["faily_name"]

    return user_info
