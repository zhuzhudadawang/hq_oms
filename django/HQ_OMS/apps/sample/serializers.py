from rest_framework import serializers
from apps.sample.models import Sample

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = '__all__'

class SampleDetailSerializer(serializers.ModelSerializer):
    """样点详情序列化器（简化字段）"""
    receive_time = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    delivery_date = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model = Sample
        fields = ['order_id', 'customer_sample_id', 'customer_name','receive_time','sender',
                  'status','sample_quantity','sample_validity_hours','sample_id',
                  'delivery_date']

class SampleListSerializer(serializers.ModelSerializer):
    """样点列表序列化器（简化字段）"""
    receive_time = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    delivery_date = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model = Sample
        fields = ['order_id', 'customer_sample_id', 'customer_name','receive_time','sender',
                  'status','sample_quantity','sample_validity_hours','sample_id',
                  'delivery_date']

class SampleCreateSerializer(serializers.ModelSerializer):
    """样点创建序列化器（简化字段）"""
    class Meta:
        model = Sample
        fields = ['order_id', 'customer_sample_id', 'customer_name','sender',
                  'status','sample_quantity','sample_validity_hours','sample_id']

    # 自定义验证：确保样点编号唯一
    def validate_sample_id(self, value):
        if Sample.objects.filter(sample_id=value).exists():
            raise serializers.ValidationError("样点编号已存在，请更换")
        return value