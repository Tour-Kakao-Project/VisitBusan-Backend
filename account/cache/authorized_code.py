from django.core.cache import cache

from account.model.vo.AuthroizedCodeVO import AuthroizedCodeVO
from visit_busan.exception.Custom400Exception import *

RANDOM_CONDE_LENGTH = 4
INVAILD_TIME_HOUR = 1


def save_authorized_code(code, email):
    data = AuthroizedCodeVO(code, email).json
    is_existed = cache.get(email)
    if not is_existed:
        cache.set(email, data, 1 * 600 * 600)
        return data
    else:
        print("이미 존재합니다.")
        return is_existed


def authorize_code(authentication_code, email):
    response = cache.get(email)
    if response == None:
        raise Custom400Exception(ErrorCode_400.INVAILD_AUTHENTICATION_CODE)
    else:
        response_code = response["code"]
        if str(response_code) == str(authentication_code):
            cache.delete(email)
            return True
        else:
            raise Custom400Exception(ErrorCode_400.NOT_MATCH_AUTHENTICATION_CODE)
