from .models import Task, User, Role
from rest_framework.response import Response
from .serializers import UserSerializer, TaskSerializer,VerifyPasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import status

from DRF_app.utilities.utils import get_tokens_for_user
from django.utils.encoding import DjangoUnicodeDecodeError, force_bytes, smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.views import APIView
import os
from DRF_app.utilities.utils import Util
import sendgrid
from sendgrid.helpers.mail import Mail
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

# Response is used to return API responses in DRF
# Decorators is used to specify the HTTP method
# task = Task.objects.all() it retrives all the instances of Task Model
# many=true defines that there are multiple instances to serailized
# serializer.data property retrieves the serialized data as JSON format.
from rest_framework.permissions import BasePermission

class IsAdminOnly(BasePermission):
    
    def has_permission(self, request, view):
        # Print the role of the logged-in user
        return request.user.role.name == 'admin'

@api_view(['POST'])
@authentication_classes([])
def Register(request):
    if request.method == 'POST':
        role = Role.objects.filter(name='user').first()
        if role:
            roleid = role.id
        else:
            return Response("Role not found", status=404)
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            print(roleid)
            serializer.validated_data['role_id'] = roleid 
          
            user = serializer.save()
            print("Mail sent!")
            return Response("New User Added", status=200)
        else:
            return Response(serializer.errors, status=400)
        
class verifyLink(APIView):
    authentication_classes = []
    def get(self,request,id,token):
        id = smart_str(urlsafe_base64_decode(id))
        user = User.objects.get(id=id) 
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"message":"your token is expired"},status=status.HTTP_400_BAD_REQUEST)
        user.is_verify = True
        user.save()
        return Response({"message":"User Email verify Successfully"},status=status.HTTP_200_OK)

class VerifyPassword(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = VerifyPasswordSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            response = {
                "message": "Password changed successfully",
                "status": status.HTTP_200_OK,
            }
            return Response(response, status=status.HTTP_200_OK)
        response = serializer.errors
        response["status"] = status.HTTP_400_BAD_REQUEST
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

@api_view(['GET'])
@permission_classes([IsAdminOnly])
def GetAllUser(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminOnly])
def DeleteUser(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response("User Not Found", status=404)
    
    if request.method == 'DELETE':
        user.delete()
        return Response("User Deleted", status=204) 

@api_view(['GET'])
def GetTaskByUser(request):
    if request.user.is_verify == True:
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    else:
        message={"message":"You have not verfied your email address yet please check your email to verify your account"}
        return Response(message,status=400) 

@api_view(['GET'])
def GetDoneTasks(request):
    if request.user.is_verify == True:
        status = Task.objects.filter(status=1)
        if status.exists:
            tasks = Task.objects.filter(user=request.user, status=1)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)
        else:
            return Response("No done tasks found", status=201)
    else:
        message={"message":"You have not verfied your email address yet please check your email to verify your account"}
        return Response(message,status=400)

@api_view(['POST'])
def Create_Task(request):
    if request.method == 'POST':
        #below line defines that u  are addig new key value pair in request.data 
        if request.user.is_verify == True:
            request.data['user'] = request.user.id
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("Task added", status=201)
            else:
                return Response(serializer.errors, status=400)
        else:
            message={"message":"You have not verfied your email address yet please check your email to verify your account"}
            return Response(message,status=400)

#use the |= operator to combine multiple Q objects with the OR operator, 
#ensuring that at least one of the words is matched in the task field
#The Q() object in Django is used to define complex queries by combining multiple 
#conditions using logical operators such as OR (|) and AND (&).
#here |= is used to check each word against the task field it is used to combine each word 
@api_view(['GET'])
def Search_Task(request):
    if request.method == 'GET':
        if request.user.is_verify == True:
            search = request.query_params.get('search')
            words = search.split()
            query = Q()
        
            for word in words:
                    query = Q(task__icontains=word) | Q(status__icontains=word)

            tasks = Task.objects.filter(query,user=request.user)
            if tasks:
                serializer = TaskSerializer(tasks, many=True)
                return Response(serializer.data)   
            else:
                return Response("Task not found",status= 400)
        else:
            message={"message":"You have not verfied your email address yet please check your email to verify your account"}
            return Response(message,status=400)
       
@api_view(['PUT'])
def Update_Task(request, task_id):
    
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response("Task not found", status=404)
    if request.method == 'PUT' and task.user == request.user:
        if request.user.is_verify == True:
            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("Task updated", status=200)
            return Response(serializer.errors, status=400)
        else:
            message={"message":"You have not verfied your email address yet please check your email to verify your account"}
            return Response(message,status=400)
    else:
        return Response("YOU CAN NOT PERFORM ANY ACTION IN OTHER USER'S TASK")

@api_view(['DELETE'])
def Delete_Task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response("Task not found", status=404)

    if request.method == 'DELETE' and task.user == request.user:
        if request.user.is_verify == True:
            task.delete()
            return Response("Task deleted", status=204)
        else:
            message={"message":"You have not verfied your email address yet please check your email to verify your account"}
            return Response(message,status=400)
        
@api_view(['PUT'])
def MarkAsDone(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        # task.user == request.data['user']
        print(task)
    except Task.DoesNotExist:
        return Response("Task not found", status=404)
    print(task.user.id)
    print(request.user.id)
    if request.method == 'PUT' and task.user == request.user:
        if request.user.is_verify == True:
    
            task.status = 1
            task.save()
            serializer = TaskSerializer(task)
            message = {"message": "Task marked as done."}
            return Response({**serializer.data, **message})
        else:
            message={"message":"You have not verfied your email address yet please check your email to verify your account"}
            return Response(message,status=400)
    message = {"message": "You cannot perform any action on another user's task."}
    return Response(message, status=403)

class LogIn(APIView):
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = authenticate(email=email, password=password)
            if user:
                token = get_tokens_for_user(user)
                return Response({'access_token': token})
            else:
                return Response({"message": "Invalid credentials"}, status=401)
        except User.DoesNotExist:
            return Response({"message": "Invalid Credentials"}, status=401)
         
