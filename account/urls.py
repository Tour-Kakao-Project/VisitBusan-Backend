from django.urls import path

from . import views

urlpatterns = [
    # local test
    ## kakao login
    path('back/oauth/kakao', views.KakaoLogin.kakao_back_login),
    path('oauth/kakao', views.KakaoLogin.kakao_back_login_redirect),
    
    path('login/oauth/kakao', views.KakaoLogin.kakao_login),
    path('login/visit-busan', views.Visit_Busan_Login.visit_busan_login),
    
    path('sign-up', views.Visit_Busan_Login.visit_busan_sign_up),
]