from rest_framework import serializers
from .models import ChatMessage, UserSubmission

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'

class UserSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubmission
        fields = '__all__'
