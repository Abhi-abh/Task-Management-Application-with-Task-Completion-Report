# serializers.py

from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'  # or list only the fields you want to expose, e.g. ['id', 'title', 'status', ...]
