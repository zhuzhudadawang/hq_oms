from rest_framework.generics import GenericAPIView
from apps.user.models import Users
from apps.user.serializers import UserSerializer
from utils.Response import ApiResponse
from utils.jwt_auth import create_token
from utils.password_encode import get_md5


class LoginAPIView(GenericAPIView):
    def post(self, request):
        return_data = {}
        request_data = request.data
        username = request_data.get("username")
        try:
            user_data = Users.objects.get(username=username)
        except Exception:
            return ApiResponse.failed(message="用户名或密码错误")

        user_ser = UserSerializer(instance=user_data, many=False)
        # 用户输入的密码
        user_password = request_data.get("password")
        md5_user_password = get_md5(user_password)
        # 数据库的密码
        db_user_password = user_ser.data.get("password")
        if md5_user_password != db_user_password:
            return ApiResponse.failed(message="用户名或密码错误")
        else:
            token_info = {
                "username": username,
                "role": user_ser.data.get("role"),
            }
            token_data = create_token(token_info)
            return_data["token"] = token_data
            return_data["userInfo"] = {
                "id": user_ser.data.get("id"),
                "username": username,
                "nickname": user_ser.data.get("nickname"),
            }
            return_data["roles"] = [user_ser.data.get("role")]
            return ApiResponse.success(data=return_data, message="登录成功")
