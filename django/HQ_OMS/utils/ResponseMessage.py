from django.http import JsonResponse
# 订单的响应全是1开头的
# class OrderResponse():
#     @staticmethod
#     def success(data):
#         result = {"status": 1000, "data": data}
#         return JsonResponse(result,safe=False)# 更省事
#         #safe=False，则允许序列化任何可 JSON 序列化的数据类型（如列表、元组、字符串、数字等）
#     @staticmethod
#     def failed(data):
#         result = {"status": 1001, "data": data}
#         return JsonResponse(result,safe=False)
#
#     @staticmethod
#     def other(data):
#         result = {"status": 1002, "data": data}
#         return JsonResponse(result,safe=False)

class OrderResponse:
    # 定义状态码常量（与前端拦截器逻辑对齐）
    SUCCESS_CODE = 0  # 前端判断成功的条件：code === 0
    FAILED_CODE = 1   # 通用业务失败
    UNAUTHORIZED_CODE = 401  # 未授权（前端会跳转登录）
    OTHER_CODE = 4002  # 其他自定义状态

    @staticmethod
    def success(data=None, message="操作成功"):
        """成功响应：code=0（匹配前端成功判断）"""
        result = {
            "code": OrderResponse.SUCCESS_CODE,
            "message": message,
            "data": data
        }
        return JsonResponse(result, safe=False)

    @staticmethod
    def failed(message="操作失败", data=None):
        """业务失败响应：code=1（前端会提示message）"""
        result = {
            "code": OrderResponse.FAILED_CODE,
            "message": message,
            "data": data
        }
        return JsonResponse(result, safe=False)

    @staticmethod
    def unauthorized(message="登录已过期，请重新登录"):
        """未授权响应：code=401（前端会清除token并跳转登录）"""
        result = {
            "code": OrderResponse.UNAUTHORIZED_CODE,
            "message": message,
            "data": None
        }
        return JsonResponse(result, safe=False)

    @staticmethod
    def other(data=None, message="其他状态", code=OTHER_CODE):
        """其他自定义状态（可灵活指定code）"""
        result = {
            "code": code,
            "message": message,
            "data": data
        }
        return JsonResponse(result, safe=False)

# 机台的响应全是2开头的
class MachineResponse():
    @staticmethod
    def success(data):
        result = {"status": 2000, "data": data}
        return JsonResponse(result,safe=False)# 更省事
        #safe=False，则允许序列化任何可 JSON 序列化的数据类型（如列表、元组、字符串、数字等）
    @staticmethod
    def failed(data):
        result = {"status": 2001, "data": data}
        return JsonResponse(result,safe=False)

    @staticmethod
    def other(data):
        result = {"status": 2002, "data": data}
        return JsonResponse(result,safe=False)

# 样点的响应全是3开头的
class SampleResponse():
    @staticmethod
    def success(data):
        result = {"status": 3000, "data": data}
        return JsonResponse(result,safe=False)# 更省事
        #safe=False，则允许序列化任何可 JSON 序列化的数据类型（如列表、元组、字符串、数字等）
    @staticmethod
    def failed(data):
        result = {"status": 3001, "data": data}
        return JsonResponse(result,safe=False)

    @staticmethod
    def other(data):
        result = {"status": 3002, "data": data}
        return JsonResponse(result,safe=False)

# 工序的响应全是4开头的
class ProcessResponse():
    @staticmethod
    def success(data):
        result = {"status": 4000, "data": data}
        return JsonResponse(result, safe=False)

    @staticmethod
    def failed(data):
        result = {"status": 4001, "data": data}
        return JsonResponse(result, safe=False)

    @staticmethod
    def other(data):
        result = {"status": 4002, "data": data}
        return JsonResponse(result, safe=False)
