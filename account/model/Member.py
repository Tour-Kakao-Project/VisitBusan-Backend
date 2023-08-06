from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=50) # 이메일
    first_name = models.CharField(max_length=50) # 이름: 이름
    last_name = models.CharField(max_length=50) # 이름: 성

    def __str__(self):
        return self.email  # 닉네임 값을 대표값으로 설정