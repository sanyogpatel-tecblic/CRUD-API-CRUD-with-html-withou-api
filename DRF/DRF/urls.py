"""
URL configuration for DRF project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from DRF_app import views
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
    

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('DRF_app.urls')),
    path('task/',views.GetTaskByUser,name= 'task_list'),
    path('users/',views.GetAllUser,name= 'user_list'),
    path('create_task/',views.Create_Task,name= 'create_task'),
    path('update_task/<int:task_id>',views.Update_Task,name= 'update_task'),    
    path('delete_task/<int:task_id>',views.Delete_Task,name= 'delete_task'),
    path('login',views.LogIn.as_view(),name='login'),
    # path('login',views.LoginVaibhav,name='login'),
    path('markasdone/<int:task_id>',views.MarkAsDone,name='markasdone'),
    path('donetasks',views.GetDoneTasks,name='donetasks'),
    path('register',views.Register,name='register'),
    path('delete_user/<int:user_id>',views.DeleteUser,name='delete'),
    
    path('search_task/',views.Search_Task,name='searchtask'),
    path('verify_link/<id>/<token>/',views.verifyLink.as_view(),name = "Verify Email Link"),
    path('verifypassword/', views.VerifyPassword.as_view(), name='verify-password'),
    path('login/', views.LogIn.as_view(), name='login'),    
]
 


