from django.db import models

class ChatMessage(models.Model):
    session_id = models.CharField(max_length=255)
    message = models.TextField()
    sender = models.CharField(max_length=10, choices=(("user", "User"), ("bot", "Bot")))
    timestamp = models.DateTimeField(auto_now_add=True)

class UserSubmission(models.Model):
    session_id = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=100)
    address = models.TextField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
