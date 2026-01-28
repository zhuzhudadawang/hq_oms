from rest_framework.views import exception_handler
from rest_framework.response import Response as DRFResponse
from rest_framework.exceptions import AuthenticationFailed


def custom_exception_handler(exc, context):
    """自定义异常处理，确保认证失败返回 401"""
    response = exception_handler(exc, context)
    
    if isinstance(exc, AuthenticationFailed):
        return DRFResponse(
            {'code': 401, 'message': str(exc.detail), 'data': None},
            status=401
        )
    
    return response
