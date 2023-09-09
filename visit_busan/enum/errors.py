from enum import Enum


class ErrorCode_404(Enum):
    NOT_AGREE_EMAIL = ("001_NOT_AGREE_EMAIL", "이메일을 동의하지 않았습니다.")
    ALREADY_SIGN_IN = ("002_ALREADY_SIGN_IN", "회원가입 이력이 있는 이메일입니다.")
    DUPLICATED_EMAIL = ("003_DUPLICATED_EMAIL", "이미 존재하는 이메일입니다.")
    INVAILD_PASSED = ("004_INVAILD_PASSED", "패스워드 형식이 올바르지 않습니다.")

    def __init__(self, error_code, error_msg):
        self.error_code = error_code
        self.error_msg = error_msg

    def __str__(self):
        return self.error_code
