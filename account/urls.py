from django.urls import path

from . import views

urlpatterns = [
    # local test
    ## kakao login
    path("back/oauth/kakao", views.KakaoLogin.kakao_back_login),
    path("oauth/kakao", views.KakaoLogin.kakao_back_login_redirect),
    ## google login
    path("back/oauth/google", views.GoogleLogin.google_back_login),
    path("oauth/google", views.GoogleLogin.google_back_login_redirect),
    # front
    ##login
    path("login/oauth/kakao", views.KakaoLogin.kakao_login),
    path("login/oauth/google", views.GoogleLogin.google_login),
    path("login/visit-busan", views.Visit_Busan_Login.visit_busan_login),
    # sign up
    path("sign-up", views.Visit_Busan_Login.visit_busan_sign_up),
    path("sign-up/duplicated-email", views.check_duplicated_email),
    path("authorize", views.check_authentication_code),
    # test
    path("email", views.test_email),
]
