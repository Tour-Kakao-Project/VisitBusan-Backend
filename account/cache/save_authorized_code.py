from django.core.cache import cache

from account.model.vo.AuthroizedCodeVO import AuthroizedCodeVO

RANDOM_CONDE_LENGTH = 4
INVAILD_TIME_DAY = 1


def save_authorized_code(code, email):
    data = AuthroizedCodeVO(code, email).json
    is_existed = cache.get(email)
    if not is_existed:
        cache.set(email, data, 1 * 24 * 60)
        return data
    else:
        print("이미 존재합니다.")
        return is_existed
