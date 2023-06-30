from django.contrib import admin

# Register your models here.
from first_app.models import AccessRecord,Topic,User,Order

admin.site.register(AccessRecord)
admin.site.register(Topic)

admin.site.register(User)
admin.site.register(Order)