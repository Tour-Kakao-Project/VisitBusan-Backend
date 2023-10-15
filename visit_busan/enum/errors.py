from enum import Enum


class ErrorCode_400(Enum):
    NOT_AGREE_EMAIL = ("001_NOT_AGREE_EMAIL", "이메일을 동의하지 않았습니다.")
    ALREADY_SIGN_IN = ("002_ALREADY_SIGN_IN", "회원가입 이력이 있는 이메일입니다.")
    DUPLICATED_EMAIL = ("003_DUPLICATED_EMAIL", "이미 존재하는 이메일입니다.")
    INVAILD_PASSWD = ("004_INVAILD_PASSWD", "패스워드 형식이 올바르지 않습니다.")
    INVAILD_AUTHENTICATION_CODE = (
        "005_INVAILD_AUTHENTICATION_CODE",
        "만료된 인증 코드를 요청하셨습니다. 다시 인증코드를 요청하세요.",
    )
    NOT_MATCH_AUTHENTICATION_CODE = (
        "006_NOT_MATCH_AUTHENTICATION_CODE",
        "올바르지 않은 인증 코드를 요청하셨습니다.",
    )
    NOT_EXIST_EMAIL = ("007_NOT_EXIST_EMAIL", "존재하지 않는 이메일을 요청하셨습니다.")
    OAUTH_MEMBER_REQUEST = (
        "008_OAUTH_MEMBER_REQUEST",
        "간편 로그인으로 회원가입한 사용자의 정보로 요청하셨습니다.",
    )
    WRONG_PASSWD = ("009_WRONG_PASSWD", "잘못된 비밀번호를 요청하셨습니다.")

    def __init__(self, error_code, error_msg):
        self.error_code = error_code
        self.error_msg = error_msg

    def __str__(self):
        return self.error_code
