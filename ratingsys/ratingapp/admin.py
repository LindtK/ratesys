from django.contrib import admin
from .models import Lecturer, Module, Student, Result, ModuleRating
# Register your models here.
admin.site.register(Lecturer)
admin.site.register(Module)
admin.site.register(Student)
admin.site.register(Result)
admin.site.register(ModuleRating)
