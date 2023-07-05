from django.contrib import admin
from .models import Region,State,Zone,District

# Register your models here.
admin.site.register(Region)
admin.site.register(State)
admin.site.register(Zone)
admin.site.register(District)