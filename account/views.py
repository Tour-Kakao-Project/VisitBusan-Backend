from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse

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
from visit_busan.utils.email_util import (
    send_sign_up_email,
    send_sign_up_email_with_templete,
    send_passwd,
)
from account.cache.authorized_code import *
from account.service.google_api.google_oauth_api import (
    get_google_user_info_from_access_token,
    get_google_user_info_from_id_token,
)
from account.serializers import *


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

    @api_view(["POST"])
    @permission_classes([AllowAny])
    def kakao_login(request):
        print(requests.data)
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
        print(request.data)
        email = request.data["email"]
        passwd = request.data["password"]
        first_name = request.data["first_name"]
        last_name = request.data["last_name"]

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
        user, member = save_member(email, first_name, last_name, 1, passwd)

        # 4. Send email
        send_sign_up_email_with_templete(member.email)

        return Response({"email": member.email}, status=status.HTTP_200_OK)

    @api_view(["POST"])
    @permission_classes([AllowAny])
    def visit_busan_login(request):
        try:
            email = request.data["email"]
            passwd = request.data["password"]

            print(request.data)

            # 1. Check the email
            member = Member.objects.filter(email=str(email))
            if member.exists():
                login_service = member.get().oauth_provider
                if login_service != "1":
                    raise Custom400Exception(ErrorCode_400.OAUTH_MEMBER_REQUEST)

            # 2. Check the password
            if not check_passwd_rule(passwd):
                raise Custom400Exception(ErrorCode_400.INVAILD_PASSWD)

            if passwd != member.get().passwd:
                raise Custom400Exception(ErrorCode_400.WRONG_PASSWD)
            # + Check is_authoirzed
            member = member.get()
            # if not member.is_authorized:
            #     return Response(
            #         {"email": member.email, "is_authorized": False},
            #         status=status.HTTP_401_UNAUTHORIZED,
            #     )

            # 3. Get backend token
            user = User.objects.get(username=str(email))
            jwt_token = get_tokens_for_user(user)
            # 4. Save refresh token
            member.refresh_token = jwt_token["refresh_token"]
            member.save()

            return Response(
                {"email": member.email, "jwt_token": jwt_token},
                status=status.HTTP_200_OK,
            )
        except Custom400Exception as e:
            raise e
        except Exception as e:
            print(e)


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
        email, given_name, family_name = get_google_user_info_from_access_token(
            google_access_token
        )

        # 2. Get user info
        user, member = save_google_member(email, given_name, family_name)

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

    @api_view(["POST"])
    @permission_classes([AllowAny])
    def google_login(request):
        try:
            print("google_login")
            print(request.data)
            google_id_token = request.data["google_id_token"]
            email, given_name, family_name = get_google_user_info_from_id_token(
                google_id_token
            )

            # 1. Get user info
            user, member = save_google_member(email, given_name, family_name)

            # 2. Get backend token
            jwt_token = get_tokens_for_user(user)

            # 3. Save refresh token
            member.refresh_token = jwt_token["refresh_token"]
            member.save()

            return Response(
                {
                    "email": member.email,
                    "google_id_token": google_id_token,
                    "jwt_token": jwt_token,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            JsonResponse(
                {
                    "error": str(e),
                    "error_args": e.args,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


def save_member(email, first_name, last_name, oauth_provider_num, passwd):
    user = User.objects.create(username=str(email))
    user.save()

    member = Member.objects.create(
        user=user,
        email=email,
        first_name=first_name,
        last_name=last_name,
        oauth_provider=oauth_provider_num,
        is_authorized=False,
        passwd=passwd,
    )
    member.save()
    return user, member


def save_google_member(email, given_name, family_name):
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
            first_name=family_name,
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
    print(requests.data)
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

    send_sign_up_email_with_templete(email)

    return Response({"email": email, "result": "Success"}, status=status.HTTP_200_OK)


def find_member_by_email(email):
    member = Member.objects.filter(email=str(email))
    if member.exists():
        return member.get()
    else:
        raise Custom400Exception(ErrorCode_400.NOT_EXIST_EMAIL)


@api_view(["GET"])
@permission_classes([AllowAny])
def show_mail_templates(requests):
    try:
        context = {"email": "lchy0413@gmail.com", "authorized_code": 1234}
        return render(requests, "account/email_authentication_b.html", context=context)
    except Exception as e:
        e


class Visit_Busan_Member(APIView):
    @api_view(["GET"])
    @permission_classes([AllowAny])
    def find_passwd(request):
        email = request.data["email"]

        member = Member.objects.filter(email=str(email))
        if member.exists():
            member = member.get()
            if member.oauth_provider != "1":
                Custom400Exception(ErrorCode_400.OAUTH_MEMBER_REQUEST)
            else:
                send_passwd(email, member.passwd)
                return Response(
                    {"email": email, "result": "Success"},
                    status=status.HTTP_200_OK,
                )
        else:
            raise Custom400Exception(ErrorCode_400.NOT_EXIST_EMAIL)


class MemberView(APIView):
    # Send member info
    def get(self, request):
        member = request.user.member

        return Response(
            MemberSerializers(member).data,
            status=status.HTTP_200_OK,
        )

    # Remove member data(user, member, course)
    def delete(self, request):
        member = request.user.member
        email = member.email
        user = member.user

        user.delete()
        return Response(
            {"email": email, "result": "Success"},
            status=status.HTTP_200_OK,
        )
