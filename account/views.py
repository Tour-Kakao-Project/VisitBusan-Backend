from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

import requests
import random
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from .model.Member import *
from visit_busan.settings import env
from visit_busan.enum.index import *
from visit_busan.utils.string_utils import *
from visit_busan.exception.Custom400Exception import *
from visit_busan.utils.email_util import send_sign_up_email
from account.cache.authorized_code import *


class KakaoLogin(APIView):
    @api_view(["GET"])
    @permission_classes([AllowAny])
    def kakao_back_login(request):
        client_id = env("KAKAO_CLIENT_ID")
        redirect_uri = env("KAKAO_REDIRECT_URI")
        response_type = "code"

        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type={response_type}"
        )

    @api_view(["GET"])
    @permission_classes([AllowAny])
    def kakao_back_login_redirect(request):
        # 1. Get Access token
        code = request.GET.get("code", None)

        headers = {
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        data = {
            "grant_type": "authorization_code",
            "client_id": env("KAKAO_CLIENT_ID"),
            "redirect_uri": env("KAKAO_REDIRECT_URI"),
            "code": code,
        }

        url = "https://kauth.kakao.com/oauth/token"

        token_req = requests.post(url, headers=headers, data=data)
        token_req_json = token_req.json()

        kakao_access_token = token_req_json.get("access_token")

        # 2. Get user info
        member, user = save_kakao_member(kakao_access_token)

        # 3. Get backend token
        jwt_token = get_tokens_for_user(user)

        # 4. Save refresh token
        member.refresh_token = jwt_token["refresh_token"]
        member.save()

        return Response(
            {
                "email": member.email,
                "kakao_access_token": kakao_access_token,
                "jwt_token": jwt_token,
            },
            status=status.HTTP_200_OK,
        )

    @api_view(["GET"])
    @permission_classes([AllowAny])
    def kakao_login(request):
        try:
            kakao_access_token = request.data["kakao_access_token"]

            # 1. Get user info
            member, user = save_kakao_member(kakao_access_token)

            # 2. Get backend token
            jwt_token = get_tokens_for_user(user)

            # 3. Save refresh token
            member.refresh_token = jwt_token["refresh_token"]
            member.save()

            return Response(
                {
                    "email": member.email,
                    "kakao_access_token": kakao_access_token,
                    "jwt_token": jwt_token,
                },
                status=status.HTTP_200_OK,
            )
        except:
            pass


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "access_token": str(refresh.access_token),  # access_token 호출
        "refresh_token": str(refresh),
    }


def save_kakao_member(kakao_access_token):
    kakao_api_response = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers={
            "Authorization": f"Bearer {kakao_access_token}",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        },
    )

    kakao_api_response = kakao_api_response.json()

    nickname = kakao_api_response["properties"]["nickname"]
    has_email = kakao_api_response["kakao_account"]["has_email"]
    if has_email:
        email = kakao_api_response["kakao_account"]["email"]
    else:
        raise Custom400Exception(ErrorCode_400.NOT_AGREE_EMAIL)

    member = Member.objects.filter(email=str(email))
    if member.exists():
        login_service = member.get().oauth_provider
        if login_service != "2":
            raise Custom400Exception(ErrorCode_400.ALREADY_SIGN_IN)

        user = User.objects.get(username=str(email))
    else:
        user = User.objects.create(username=str(email))
        user.save()
        member = Member.objects.create(
            user=user,
            email=email,
            first_name=nickname,
            oauth_provider=2,
            is_authorized=True,
        )
        member.save()
    return member.get(), user


class Visit_Busan_Login(APIView):
    @api_view(["POST"])
    @permission_classes([AllowAny])
    def visit_busan_sign_up(request):
        email = request.data["email"]
        passwd = request.data["password"]
        first_name = request.data["first_name"]
        last_name = request.data["last_name"]
        phone_number = request.data["phone_number"]

        # 1. Check the email
        member = Member.objects.filter(email=str(email))
        if member.exists():
            login_service = member.get().oauth_provider
            if login_service != "1":
                raise Custom400Exception(ErrorCode_400.ALREADY_SIGN_IN)
            else:
                raise Custom400Exception(ErrorCode_400.DUPLICATED_EMAIL)

        # 2. Check the password
        if not check_passwd_rule(passwd):
            raise Custom400Exception(ErrorCode_400.INVAILD_PASSED)

        # 3. Save
        user, member = save_member(email, first_name, last_name, 1, phone_number)

        # 4. Send email
        send_sign_up_email(member.email)

        return Response({"email": member.email}, status=status.HTTP_200_OK)

    @api_view(["GET"])
    @permission_classes([AllowAny])
    def visit_busan_login(request):
        email = request.data["email"]
        passwd = request.data["password"]

        # 1. Check the email
        member = Member.objects.filter(email=str(email))
        if member.exists():
            login_service = member.get().oauth_provider
            if login_service != "1":
                raise Custom400Exception(ErrorCode_400.ALREADY_SIGN_IN)

        # 2. Check the password
        if not check_passwd_rule(passwd):
            raise Custom400Exception(ErrorCode_400.INVAILD_PASSED)

        # 2. Get backend token
        user = User.objects.get(username=str(email))
        jwt_token = get_tokens_for_user(user)

        # 3. Save refresh token
        member = member.get()
        member.refresh_token = jwt_token["refresh_token"]
        member.save()

        return Response(
            {"email": member.email, "jwt_token": jwt_token}, status=status.HTTP_200_OK
        )


class GoogleLogin:
    @api_view(["GET"])
    @permission_classes([AllowAny])
    def google_back_login(request):
        google_client_id = env("GOOGLE_WEB_CLIENT_ID")
        redirect_uri = env("GOOGLE_REDIRECT_URI")
        response_type = "code"
        scope = "email profile"

        return redirect(
            f"https://accounts.google.com/o/oauth2/v2/auth?client_id={google_client_id}&redirect_uri={redirect_uri}&scope={scope}&response_type={response_type}"
        )

    @api_view(["GET"])
    @permission_classes([AllowAny])
    def google_back_login_redirect(request):
        # 1. Get access token
        code = request.GET.get("code")
        headers = {
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        data = {
            "grant_type": "authorization_code",
            "client_id": env("GOOGLE_WEB_CLIENT_ID"),
            "client_secret": env("GOOGLE_WEB_SECRET_KEY"),
            "redirect_uri": env("GOOGLE_REDIRECT_URI"),
            "code": code,
            "state": env("GOOGLE_STATE"),
        }

        url = "https://oauth2.googleapis.com/token"

        token_req = requests.post(url, headers=headers, data=data)
        token_req_json = token_req.json()
        google_access_token = token_req_json.get("access_token")

        # 2. Get user info
        user, member = save_google_member(google_access_token)

        # 3. Get backend token
        jwt_token = get_tokens_for_user(user)

        # 4. Save refresh token
        member.refresh_token = jwt_token["refresh_token"]

        return Response(
            {
                "email": member.email,
                "google_access_token": google_access_token,
                "jwt_token": jwt_token,
            },
            status=status.HTTP_200_OK,
        )

    @api_view(["GET"])
    @permission_classes([AllowAny])
    def google_login(request):
        try:
            google_access_token = request.data["google_access_token"]

            # 1. Get user info
            user, member = save_google_member(google_access_token)

            # 2. Get backend token
            jwt_token = get_tokens_for_user(user)

            # 3. Save refresh token
            member.refresh_token = jwt_token["refresh_token"]
            member.save()

            return Response(
                {
                    "email": member.email,
                    "google_access_token": google_access_token,
                    "jwt_token": jwt_token,
                },
                status=status.HTTP_200_OK,
            )
        except:
            pass


def save_member(email, first_name, last_name, oauth_provider_num, phone_number):
    user = User.objects.create(username=str(email))
    user.save()

    member = Member.objects.create(
        user=user,
        email=email,
        first_name=first_name,
        last_name=last_name,
        oauth_provider=oauth_provider_num,
        phone_number=phone_number,
        is_authorized=False,
    )
    member.save()
    return user, member


def save_google_member(google_access_token):
    google_api_response = requests.get(
        "https://www.googleapis.com/userinfo/v2/me",
        headers={
            "Authorization": f"Bearer {google_access_token}",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        },
    )

    google_api_response = google_api_response.json()

    email = google_api_response["email"]
    name = google_api_response["name"]
    given_name = google_api_response["given_name"]

    member = Member.objects.filter(email=str(email))
    if member.exists():
        member = member.get()
        login_service = member.oauth_provider
        if login_service != "3":
            raise Custom400Exception(ErrorCode_400.ALREADY_SIGN_IN)

        user = User.objects.get(username=str(email))
    else:
        user = User.objects.create(username=str(email))
        user.save()
        member = Member.objects.create(
            user=user,
            email=email,
            first_name=name,
            last_name=given_name,
            oauth_provider=3,
            is_authorized=True,
        )
        member.save()

    return user, member


@api_view(["GET"])
@permission_classes([AllowAny])
def check_duplicated_email(request):
    email = request.data["email"]

    member = Member.objects.filter(email=str(email))
    if member.exists():
        raise Custom400Exception(ErrorCode_400.ALREADY_SIGN_IN)
    else:
        return Response(
            {
                "email": email,
                "msg": "사용할 수 있는 이메일 입니다.",
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def check_authentication_code(request):
    email = request.data["email"]
    code = request.data["authentication_code"]

    member = find_member_by_email(email)

    result = authorize_code(code, email)
    if result == True:
        member.is_authorized = 1
        member.save()

        return Response(
            {"email": member.email, "result": "Success"}, status=status.HTTP_200_OK
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def reissue_authentication_code(request):
    email = request.data["email"]
    authorized_code = random.randrange(1000, 10000)

    save_authorized_code(authorized_code, email)

    return Response(
        {"email": authorized_code, "result": "Success"}, status=status.HTTP_200_OK
    )


def find_member_by_email(email):
    member = Member.objects.filter(email=str(email))
    if member.exists():
        return member.get()
    else:
        raise Custom400Exception(ErrorCode_400.NOT_EXIST_EMAIL)
