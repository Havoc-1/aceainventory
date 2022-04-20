from django.contrib import admin
from .models import UserProfile #importing from model.py

# Register your models here.
admin.site.register(UserProfile)