from rest_framework import serializers
from .models import User, Task

# UserSerializer inherits from serializers.ModelSerializer
# model=user means user model is associated with serializer using the model attribute
#In Django REST Framework (DRF), the extra_kwargs attribute is a dictionary that allows you to 
# specify additional options for individual fields in a serializer's Meta class.
#It provides a way to customize the behavior of specific fields in the serializer.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role']
        extra_kwargs = {
            'username': {'required': True} 
        }

    def validate_username(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("Username Must be at least 4 characters long")
        return value

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['task','user']

    def validate_task(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("Task should be at least 4 characters long.")
        return value
    

