from django.db import models
from django.contrib.auth.models import User


OAUTH_PROVIDER_CHOICES = [
    ('1', 'NONE'),
    ('2', 'KAKAO'),
    ('3', 'GOOGLE'),
]

class Member(models.Model):
    email = models.EmailField(max_length=300) # 이메일
    passwd = models.CharField( max_length=50, blank=True)
    first_name = models.CharField(max_length=30, blank=True) # 이름: 이름
    last_name = models.CharField(max_length=150, blank=True) # 이름: 성
    phone_number = models.CharField(max_length=15, blank=True)
    
    oauth_provider = models.CharField(max_length=50, choices=OAUTH_PROVIDER_CHOICES, default=OAUTH_PROVIDER_CHOICES[0]) # 로그인 제공

    def __str__(self):
        return self.email  # 닉네임 값을 대표값으로 설정