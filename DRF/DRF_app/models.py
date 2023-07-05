from django.db import models

    
class User(models.Model):
    username = models.CharField(max_length=264, unique=True)
    password = models.CharField(max_length=264)
    role = models.CharField(max_length=264,unique=False,null=True,default="user")
    def __str__(self):
        return self.username
    

class Task(models.Model):    
    task = models.CharField(max_length=10000, unique=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=2,default=0)
    def __str__(self):
        return self.task

class Role(models.Model):
    name=models.CharField