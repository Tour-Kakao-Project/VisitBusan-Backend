from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

from visit_busan.utils.errors import *

class Custom404Exception(APIException):
    status_code = 404
    default_code = 'NotFound'
    default_detail = '다시 확인해주세요'
    
    def __init__ (self, error_code, error_detail=""):
        self.detail = {
            "code": error_code.value,
            "error_detail": error_detail
        }
        

def custom_404_exception(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['error_code'] = response.data['code'][0]
        response.data['error_msg'] = response.data['code'][1]
        response.data['error_detail'] = response.data['error_detail']
        
    del response.data['code']

    return response