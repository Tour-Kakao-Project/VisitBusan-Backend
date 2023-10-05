from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

from visit_busan.enum.errors import *


class Custom400Exception(APIException):
    status_code = 400
    default_code = "BadRequest"
    default_detail = "다시 확인해주세요"

    def __init__(self, error_code, error_detail=""):
        self.detail = {
            "error_code": error_code.value[0],
            "error_msg": error_code.value[1],
            "error_detail": error_detail,
        }
