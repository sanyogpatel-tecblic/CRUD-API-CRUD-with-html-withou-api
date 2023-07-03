from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse

from first_app.models import Topic,Webpage,AccessRecord,User
# Webpage_list = AccessRecord.objects.order_by('date') This line retrieves all objects from the AccessRecord model 
# U sing the objects manager and orders them by the date field in ascending order. The result is assigned to the webpage_list variable.

# Date_dict= {'access_records':webpage_list} This line creates a dictionary called date_dict with a key 'access_records' and assigns the webpage_list to it as the corresponding value.
# This dictionary will be passed as context data to the template.
def index(request):
    webpage_list = AccessRecord.objects.order_by('date')
    date_dict= {'access_records':webpage_list}
    return render(request,'index.html',context=date_dict)

def user(request):
    user_list = User.objects.order_by('first_name', 'last_name','email')
    context = {'user_list': user_list}
    return render(request, 'user.html', context)

def create_user(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        
        user = User.objects.create(first_name=first_name, last_name=last_name, email=email)
        # Redirect or render a response
        return redirect("/users2")
    else:
        return render(request, 'createuser.html')
    
def get_user(request):
    if request.method == 'GET':
        users = User.objects.all()
        
        return render (request,'user_list.html',{'users':users})
    else:
        return render(request, 'invalid_request.html')
    
def del_user(request,user_id):
     if request.method == 'GET':
        user = User.objects.get(id = user_id)
        user.delete()
        print("-------------------")
        return redirect("/users2")
     else:
        return render(request, 'invalid_request.html')
    
def update_user(request, id):
    user = User.objects.get(id=id)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        return redirect("/users2")
    else:
        user = User.objects.get(id=id)
        return render(request, 'updatepage.html',{'user':user})

    
