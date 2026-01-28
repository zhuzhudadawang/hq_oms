import datetime
import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


def get_secret_key():
    """延迟导入，避免循环导入"""
    from django.conf import settings
    return settings.SECRET_KEY


def create_token(payload, timeout=60*24*7):
    """创建 JWT token，默认7天有效"""
    headers = {
        'alg': 'HS256',
        'typ': 'JWT'
    }
    payload["exp"] = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=timeout)
    result = jwt.encode(headers=headers, payload=payload, key=get_secret_key(), algorithm='HS256')
    return result


def get_payload(token):
    """解析 token，返回 payload"""
    result = {"status": False, "data": None, "error": None}
    try:
        payload = jwt.decode(token, get_secret_key(), algorithms=['HS256'])
        result["status"] = True
        result["data"] = payload
    except jwt.exceptions.DecodeError:
        result["error"] = "Token 解析失败"
    except jwt.exceptions.ExpiredSignatureError:
        result["error"] = "Token 已过期"
    except jwt.exceptions.InvalidTokenError:
        result["error"] = "Token 无效"
    return result


class JwtQueryParamAuthentication(BaseAuthentication):
    """URL 参数传递 token"""
    def authenticate(self, request):
        token = request.GET.get("token")
        result_payload = get_payload(token)
        return (result_payload, token)


class JwtHeaderAuthentication(BaseAuthentication):
    """请求头传递 token"""
    def authenticate(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")
        
        if not token:
            raise AuthenticationFailed("未提供 Token")
        
        if token.startswith("Bearer "):
            token = token[7:]
        
        result_payload = get_payload(token)
        
        if not result_payload["status"]:
            raise AuthenticationFailed(result_payload["error"] or "Token 无效")
        
        return (result_payload["data"], token)
