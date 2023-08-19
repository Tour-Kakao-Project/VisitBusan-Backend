from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .model.Member import *
from visit_busan.settings import env
from visit_busan.utils.errors import *
from visit_busan.utils.string_utils import *

class KakaoLogin():
    
    @api_view(['GET'])
    @permission_classes([AllowAny])
    def kakao_back_login(request):
        client_id = env('KAKAO_CLIENT_ID')
        redirect_uri = env('KAKAO_REDIRECT_URI')
        response_type = "code"

        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type={response_type}"
        )
    
    @api_view(['GET'])
    @permission_classes([AllowAny])
    def kakao_back_login_redirect(request):
        # 1. Get Access token
        code = request.GET.get('code', None)

        headers = {
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
        }
        data = {
            'grant_type': 'authorization_code',
            'client_id': env('KAKAO_CLIENT_ID'),
            'redirect_uri': env('KAKAO_REDIRECT_URI'),
            'code': code
        }

        url = 'https://kauth.kakao.com/oauth/token'

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
        
        return Response({"email":member.email, "kakao_access_token": kakao_access_token, "jwt_token":jwt_token}, status=status.HTTP_200_OK)
    
    @api_view(['GET'])
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
            
            return Response({"email":member.email, "kakao_access_token": kakao_access_token, "jwt_token":jwt_token}, status=status.HTTP_200_OK)
        except:
            pass
    
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access_token': str(refresh.access_token),  # access_token 호출
        'refresh_token': str(refresh)
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
        return Response({"error_code": ErrorCode_404.NOT_AGREE_EMAIL, "error_msg": "이메일을 동의하지 않았습니다."},
                        status=status.HTTP_404_NOT_FOUND)
        
    member = Member.objects.filter(email=str(email))
    if member.exists():
        login_service = member.get().oauth_provider
        if (login_service != '2'):
            return Response({"error_code": ErrorCode_404.ALREADY_SIGN_IN, "error_msg": "회원가입 이력이 있는 이메일입니다."},
                status=status.HTTP_404_NOT_FOUND)
        
        user = User.objects.get(username=str(email))
    else:
        user = User.objects.create(username=str(email))
        user.save()
        member = Member.objects.create(user=user,
                                        email=email,
                                        first_name=nickname,
                                        oauth_provider=2)
        member.save()
    return member.get(), user

class Visit_Busan_Login():
    
    @api_view(['POST'])
    @permission_classes([AllowAny])
    def visit_busan_sign_up(request):
        email = request.data["email"]
        passwd = request.data["password"]
        name = request.data["name"]
        phone_number = request.data["phone_number"]
        
        # 1. Check the email
        member = Member.objects.filter(email=str(email))
        if member.exists():
            login_service = member.get().oauth_provider
            if (login_service != '1'):
                return Response({"error_code": ErrorCode_404.ALREADY_SIGN_IN, "error_msg": "다른 서비스로 가입이 되어 있는 계정입니다."},
                           status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"error_code": ErrorCode_404.DUPLICATED_EMAIL, "error_msg": "이미 존재하는 이메일입니다."},
                           status=status.HTTP_404_NOT_FOUND)
        
        # 2. Check the password
        if (not check_passwd_rule(passwd)):
            return Response({"error_code": ErrorCode_404.INVAILD_PASSED, "error_msg": "패스워드 형식이 올바르지 않습니다."},
                           status=status.HTTP_404_NOT_FOUND) 
        
        # 3. Save
        user, member = save_member(email, name, 1, phone_number)
            
        return Response({"email":member.email}, status=status.HTTP_200_OK)
    
    @api_view(['GET'])
    @permission_classes([AllowAny])
    def visit_busan_login(request):
        email = request.data['email']
        passwd = request.data['password']
        
        # 1. Check the email
        member = Member.objects.filter(email=str(email))
        if member.exists():
            login_service = member.get().oauth_provider
            if (login_service != '1'):
                return Response({"error_code": ErrorCode_404.ALREADY_SIGN_IN, "error_msg": "다른 서비스로 가입이 되어 있는 계정입니다."},
                           status=status.HTTP_404_NOT_FOUND)
        
        # 2. Check the password
        if (not check_passwd_rule(passwd)):
            return Response({"error_code": ErrorCode_404.INVAILD_PASSED, "error_msg": "패스워드 형식이 올바르지 않습니다."},
                           status=status.HTTP_404_NOT_FOUND)
                
        # 2. Get backend token
        user = User.objects.get(username=str(email))
        jwt_token = get_tokens_for_user(user)
        
        # 3. Save refresh token
        member = member.get()
        member.refresh_token = jwt_token["refresh_token"]
        member.save()
        
        return Response({"email":member.email, "jwt_token":jwt_token}, status=status.HTTP_200_OK)
        
        
def save_member(email, name, oauth_provider_num, phone_number):
    user = User.objects.create(username=str(email))
    user.save()
    
    member = Member.objects.create(
        user = user,
        email = email,
        first_name = name,
        oauth_provider = oauth_provider_num,
        phone_number = phone_number
    )
    member.save()
    return user, member