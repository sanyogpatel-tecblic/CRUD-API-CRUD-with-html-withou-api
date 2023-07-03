
from .models import Task,User
from rest_framework.response import Response
from .serializers import UserSerializer,TaskSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view

from rest_framework.views import APIView
from DRF_app.utilities.utils import get_tokens_for_user
# Create your views here.

#Response is used to return API responses in DRF
#Decorators is used to specify the HTTP method
#task = Task.objects.all() it retrives all the instances of Task Model
#many=true defines that there are multiple instances to serailized
#serializer.data property retrieves the serialized data as JSON format.

@api_view(['GET'])
def GetAllTask(request):
    task = Task.objects.all()
    serializer = TaskSerializer(task, many=True)
    return Response(serializer.data)    
    
@api_view(['GET'])
def GetAllUser(request):
    user= User.objects.all()
    serializer = UserSerializer(user,many=True)
    return Response(serializer.data)

#request.data shows data sent in request
@api_view(['POST'])
def Create_Task(request):
    if request.method == 'POST':
      serializer = TaskSerializer(data=request.data)
      
      if serializer.is_valid():
          serializer.save()
          return Response("Task added", status=201)
      else:
          return Response(serializer.errors, status=400)

@api_view(['PUT'])
def Update_Task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response("Task not found", status=404)

    if request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Task updated", status=200)
        return Response(serializer.errors, status=400)
    
@api_view(['DELETE'])
def Delete_Task(request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response("Task not found", status=404)

        if request.method == 'DELETE':
            task.delete()
            return Response("Task deleted", status=204)

class LogIn(APIView):
    authentication_classes = []
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(username=username)
            if user.password == password:
                token = get_tokens_for_user(user)
                return Response({'access_token': token})
            else:
                # Invalid credentials
                return Response({"message": "Invalid credentials"}, status=401)
        except User.DoesNotExist:
            # Invalid credentials4
            return Response({"message": "Invalid Credentials"}, status=401)

