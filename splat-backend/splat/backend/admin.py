from django.contrib import admin

# Register your models here.
from .models import Student, Assignment, Submission

admin.site.register(Student)
admin.site.register(Assignment)
admin.site.register(Submission)