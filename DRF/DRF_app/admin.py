from django.contrib import admin
from DRF_app.models import Task
from .models import User,Role
# Register your models here.
admin.site.register(User)
admin.site.register(Task)
admin.site.register(Role)