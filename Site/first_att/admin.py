from django.contrib import admin
from .models import Student, Articles#, Events
# Register your models here.


admin.site.register(Student)
# admin.site.register(Events)
admin.site.register(Articles)