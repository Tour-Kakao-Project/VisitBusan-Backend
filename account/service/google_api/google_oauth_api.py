from google.oauth2 import id_token

from visit_busan.settings import env


def get_google_user_info_from_id_token(user_id_token):
    from google.auth.transport import requests

    try:
        user_info = id_token.verify_oauth2_token(
            user_id_token, requests.Request(), env("GOOGLE_WEB_CLIENT_ID")
        )
    except Exception as e:
        print(f"Fail: get google user info \n reason: {e}")

    email = user_info["email"]
    given_name = user_info["given_name"]
    family_name = user_info["family_name"]

    return email, given_name, family_name


def get_google_user_info_from_access_token(user_access_token):
    import requests

    google_api_response = requests.get(
        "https://www.googleapis.com/userinfo/v2/me",
        headers={
            "Authorization": f"Bearer {user_access_token}",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        },
    )

    google_api_response = google_api_response.json()

    email = google_api_response["email"]
    family_name = google_api_response["name"]
    given_name = google_api_response["given_name"]
    return email, given_name, family_name
