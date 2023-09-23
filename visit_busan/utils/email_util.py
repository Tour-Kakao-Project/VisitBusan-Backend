from django.core.mail import EmailMessage

import random

from account.cache.authorized_code import save_authorized_code

RANDOM_CONDE_LENGTH = 4


def send_sign_up_email(email):
    # 1. 인증 코드 생성 및 저장
    authorized_code = random.randrange(1000, 10000)
    save_authorized_code(authorized_code, email)

    # 2. 이메일 전송
    title = "Visit Busan Tour 이메일 인증"
    content = f"인증코드: {authorized_code}"
    email = EmailMessage(title, content, to=[email])
    email.send()
