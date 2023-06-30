from django.db import models

class User(models.Model):
    username = models.CharField(max_length=264, unique=True)
    password = models.CharField(max_length=264,unique=True)
    def __str__(self):
        return self.username
    

class Task(models.Model):    
    task = models.CharField(max_length=10000, unique=False)

    def __str__(self):
        return self.task
    