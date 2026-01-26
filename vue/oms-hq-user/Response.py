from django.http import JsonResponse

class ApiResponse:
    # status=200(success)
    @classmethod
    def success(cls, data=None, message="操作成功"):

        response_data = {
            "code": 0,
            "error": 0,
            "message": message,
            "data": data or {}
        }
        return JsonResponse(response_data, status=200)

    # status=200(fail)
    @classmethod
    def failed(cls, code=1, message="操作失败", data=None):

        response_data = {
            "code": code,
            "error": 1,
            "message": message,
            "data": data or {}
        }
        return JsonResponse(response_data, status=200)

    @classmethod
    def http_error(cls, status_code, message=None):

        default_messages = {
            401: "登录已过期，请重新登录",
            403: "没有权限访问",
            404: "请求的资源不存在",
            500: "服务器错误"
        }
        # 优先使用自定义message，否则用默认提示
        response_data = {
            "message": message or default_messages.get(status_code, "请求失败")
        }
        return JsonResponse(response_data, status=status_code)