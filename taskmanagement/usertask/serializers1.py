from rest_framework import serializers
from .models import Task

class TaskReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'completion_report', 'worked_hours']
