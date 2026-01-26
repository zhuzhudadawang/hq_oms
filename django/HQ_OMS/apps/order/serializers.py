from django.utils import timezone
from rest_framework import serializers
from apps.order.models import Order

class OrderDetailSerializer(serializers.ModelSerializer):
    """订单详情序列化器（简化字段）"""
    requirement_confirm_date = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    modify_time = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Order
        fields = ['order_id', 'order_status', 'customer', 'sample_quantity', 'customer_requirement',
                  'validity_requirement_hours', 'execution_place', 'order_salesman', 'requirement_confirm_date',
                  'order_amount', 'create_time', 'modify_time', 'priority']

class OrderListSerializer(serializers.ModelSerializer):
    """订单列表序列化器（简化字段）"""
    requirement_confirm_date = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    modify_time = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Order
        fields = ['order_id', 'order_status', 'customer','sample_quantity','customer_requirement',
                  'validity_requirement_hours','execution_place','order_salesman','requirement_confirm_date',
                  'order_amount','create_time', 'modify_time','priority']

class OrderCreateSerializer(serializers.ModelSerializer):
    """订单创建序列化器"""
    class Meta:
        model = Order
        fields = [
            'order_id', 'customer', 'order_status', 'customer_requirement',
            'sample_quantity', 'execution_place','validity_requirement_hours',
            'order_salesman',
        ]

    # 自定义验证：确保订单编号唯一
    def validate_order_id(self, value):
        if Order.objects.filter(order_id=value).exists():
            raise serializers.ValidationError("订单编号已存在，请更换")
        return value

    # 重写创建方法，自动补充创建时间和修改时间
    def create(self, validated_data):
        # 自动添加创建/修改时间
        validated_data['create_time'] = timezone.now()
        validated_data['modify_time'] = timezone.now()
        return super().create(validated_data)

class OrderUpdateSerializer(serializers.ModelSerializer):
    """订单更新序列化器"""
    order_id = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'order_id', 'customer', 'order_status', 'customer_requirement',
            'sample_quantity', 'execution_place','validity_requirement_hours',
            'order_salesman',
        ]

    # 重写更新方法，自动更新修改时间
    def update(self, instance, validated_data):
        # 自动更新修改时间为当前时间
        validated_data['modify_time'] = timezone.now()
        return super().update(instance, validated_data)


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
