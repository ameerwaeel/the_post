from django.contrib import admin

# Register your models here.
from .models import ChatMessage, UserSubmission
admin.site.register(ChatMessage)
admin.site.register(UserSubmission)