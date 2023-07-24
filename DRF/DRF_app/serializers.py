from rest_framework import serializers
from .models import User, Task
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.utils.encoding import DjangoUnicodeDecodeError, force_bytes, smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

# UserSerializer inherits from serializers.ModelSerializer
# model=user means user model is associated with serializer using the model attribute
#In Django REST Framework (DRF), the extra_kwargs attribute is a dictionary that allows you to 
# specify additional options for individual fields in a serializer's Meta class.
#It provides a way to customize the behavior of specific fields in the serializer.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'role_id']
        extra_kwargs = {
            'username': {'required': True} 
        }

    def validate_username(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("Username Must be at least 4 characters long")
        return value

# class UserFakerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User_Faker
#         fields= ['first_name','last_name','email']
        
# class TaskFakerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task_Faker
#         fields= ['task','role_id','user_id']
        
class VerifyPasswordSerializer(serializers.Serializer):
    newpassword = serializers.CharField(style={"input_type": "password"})
    confirmpassword = serializers.CharField(style={"input_type": "password"})

    def validate(self, attrs):
        try:
            password = attrs.get("newpassword")
            password2 = attrs.get("confirmpassword")
            id = self.context["request"].query_params.get("id")
            token = self.context["request"].query_params.get("token")
            id = smart_str(urlsafe_base64_decode(id))
            
            user = User.objects.get(id=id)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError(
                    {"Error": "Token is not valid or expired"}
                )
            if password != password2:
                raise serializers.ValidationError(
                    {"Error": "Passwords do not match"}
                )
            user.set_password(password)
            user.save()
            return attrs
        except User.DoesNotExist:
            raise serializers.ValidationError({"Error": "User does not exist"})
        except DjangoUnicodeDecodeError:
            raise serializers.ValidationError({"Error": "Token is not valid or expired"})

        
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['task','user']

    def validate_task(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("Task should be at least 4 characters long.")
        return value
    
# class TaskFakeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = ['task','user']

    
