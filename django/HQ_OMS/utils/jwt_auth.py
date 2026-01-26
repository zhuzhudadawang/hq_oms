import datetime

import jwt
from rest_framework.authentication import BaseAuthentication

from HQ_OMS.settings import SECRET_KEY


def create_token(payload,timeout=120):
    headers = {
        'alg': 'HS256',  # 算法：HMAC SHA-256
        'typ': 'JWT'  # 类型：JWT
    }
    # payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)
    payload["exp"] = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=timeout) # 定义超时时间
    result =  jwt.encode(headers=headers, payload=payload, key=SECRET_KEY,algorithm='HS256')
    return result

def get_payload(token):
    result = {"status": False, "data": None,"error": None}
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        result["status"] = True
        result["data"] = payload
    except jwt.exceptions.DecodeError:
        print("Token decode error失败")
        result["error"] = "Token decode error失败"
    except jwt.exceptions.ExpiredSignatureError:
        print("Token expired失效")
        result["error"] = "Token expired失效"
    except jwt.exceptions.InvalidTokenError:
        print("Token invalid非法")
        result["error"] = "Token invalid非法"
    return result

# 用户在url中进行token的参数配置
class JwtQueryParamAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 从url中拿到token
        token = request.GET.get("token")
        result_payload = get_payload(token)
        print(result_payload)
        return (result_payload,token)
# 请求头传递
class JwtHeaderAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 从头信息中拿到token
        # print(request.META)
        # token = request.META.get("HTTP_TOKEN")  postman中这样获取
        token = request.META.get("HTTP_AUTHORIZATION")  # 浏览器中这样获取
        result_payload = get_payload(token)
        print(result_payload)
        return (result_payload,token)
