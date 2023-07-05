from .models import Task,User
from rest_framework.response import Response
from .serializers import UserSerializer,TaskSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view,authentication_classes,permission_classes

from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import TokenError
from DRF_app.utilities.utils import get_tokens_for_user
# Create your views here.

#Response is used to return API responses in DRF
#Decorators is used to specify the HTTP method
#task = Task.objects.all() it retrives all the instances of Task Model
#many=true defines that there are multiple instances to serailized
#serializer.data property retrieves the serialized data as JSON format.
@api_view(['GET'])
def GetAllUser(request):
    user= User.objects.all()
    serializer = UserSerializer(user,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def GetTaskByUser(request):
    tasks = Task.objects.filter(user=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def GetDoneTasks(request):
    status = Task.objects.filter(status=1)
    if status.exists:
        tasks= Task.objects.filter(user=request.user,status=1)
        serializer =TaskSerializer(tasks,many=True)
        return Response(serializer.data)
    else:
        return Response("No done tasks found", status=201)

@api_view(['POST'])
def Create_Task(request):
    if request.method == 'POST':
        request.data['user']=request.user.id
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Task added", status=201)
        else:
            return Response(serializer.errors, status=400)
        
@api_view(['POST'])
@authentication_classes([])
def Register(request): 
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("New User Added",status=200)
        else:
            return Response(serializer.errors, status=400)

@api_view(['PUT'])
def Update_Task(request, task_id):  
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response("Task not found", status=404)
    if request.method == 'PUT' and task.user == request.user:
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Task Updated", status=200)
        return Response(serializer.errors, status=400)
    else:
        return Response("YOU CAN NOT PERFORM ANY ACTION IN OTHER USER'S TASK")
    
@api_view(['DELETE'])
def Delete_Task(request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response("Task not found", status=404)

        if request.method == 'DELETE' and task.user == request.user:
            task.delete()
            return Response("Task deleted", status=204)

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
        task.status = 1
        task.save()
        
        serializer = TaskSerializer(task)
        message = {"message": "Task marked as done."}  
        return Response({**serializer.data, **message})  
    
    message = {"message": "You cannot perform any action on another user's task."}
    return Response(message, status=403)

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
                return Response({"message": "Invalid credentials"}, status=401)
        except User.DoesNotExist:
            return Response({"message": "Invalid Credentials"}, status=401)

