from rest_framework import serializers
from apps.machine.models import MachineUsageRecord

class MachineUsageRecordSerializer(serializers.ModelSerializer):
    # 查询序列化器
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    creation_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)

    class Meta:
        model = MachineUsageRecord
        fields = '__all__'

class MachineUsageRecordCreateSerializer(serializers.ModelSerializer):
    # 新增序列化器

    class Meta:
        model = MachineUsageRecord
        fields = ['record_id', 'machine_name', 'usage_type','duration_minutes','creator_name',
                  'device_code']

class MachineUsageRecordUpdateSerializer(serializers.ModelSerializer):
    # 更新序列化器

    class Meta:
        model = MachineUsageRecord
        fields = ['record_id', 'machine_name', 'usage_type','duration_minutes','creator_name',
                  'device_code']


