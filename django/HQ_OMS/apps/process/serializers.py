from django.utils import timezone
from rest_framework import serializers
from apps.process.models import Process

class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = '__all__'

class ProcessListSerializer(serializers.ModelSerializer):
    """工序列表序列化器（简化字段）"""
    sample_receive_date = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Process
        fields = ['process_id','customer', 'test_item','process_category','sample_id',
                  'status','sample_validity_hours','is_outsource','sample_receive_date']

class ProcessCreateSerializer(serializers.ModelSerializer):
    """创建工序序列化器（简化字段）"""

    class Meta:
        model = Process
        fields = ['process_id','customer', 'test_item','process_category','sample_id',
                  'status','is_outsource']

    # 自定义验证：确保工序编号唯一
    def validate_process_id(self, value):
        if Process.objects.filter(process_id=value).exists():
            raise serializers.ValidationError("工序编号已存在，请更换")
        return value

        # 重写创建方法，自动补充创建时间和修改时间

    def create(self, validated_data):
        # 自动添加创建/修改时间
        validated_data['create_time'] = timezone.now()
        validated_data['modify_time'] = timezone.now()
        return super().create(validated_data)

class ProcessUpdateSerializer(serializers.ModelSerializer):
    """更新工序序列化器（简化字段）"""

    class Meta:
        model = Process
        fields = ['process_id','customer', 'test_item','process_category','sample_id',
                  'status','is_outsource']

    # 重写更新方法，自动更新修改时间
    def update(self, instance, validated_data):
        # 自动更新修改时间为当前时间
        validated_data['modify_time'] = timezone.now()
        return super().update(instance, validated_data)
