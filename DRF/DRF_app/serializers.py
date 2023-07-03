from rest_framework import serializers
from .models import User, Task

# UserSerializer inherits from serializers.ModelSerializer
# model=user means user model is associated with serializer using the model attribute


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'task']

    def validate_task(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("Task should be at least 4 characters long.")
        return value
    

