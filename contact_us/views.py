from django.shortcuts import render

# Create your views here.

from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from .models import *
from .serializers import *

from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response


import threading
from django.core.mail import EmailMessage
import logging

logger = logging.getLogger(__name__)


def send_form_email(subject, body, from_email, file_path=None):
    def send_email():
        try:
            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=from_email,
                to=["mrseller.prof@gmail.com"],
            )
            if file_path:
                email.attach_file(file_path)
            email.send()
        except Exception as e:
            logger.error(f"Failed to send email: {e}")

    threading.Thread(target=send_email).start()


class NewsLetterListCreateView(generics.ListCreateAPIView):
    queryset = NewsLetter.objects.all()
    serializer_class = NewsLetterSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    def perform_create(self, serializer):
        instance = serializer.save()
        subject = "New Newsletter Subscription"
        body = f"New subscription from: {instance.email}"
        send_form_email(subject, body, instance.email)


class InterestsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Interests.objects.all()
    serializer_class = InterestsSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

class InterestsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NewsLetter.objects.all()
    serializer_class = NewsLetterSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    lookup_field = 'uuid'


class ContactUSListCreateAPIView(generics.ListCreateAPIView):
    queryset = ContactUS.objects.all()
    serializer_class = ContactUSSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def perform_create(self, serializer):
        instance = serializer.save()
        subject = f"New Chat Contact Form Submission - {instance.full_name}"
        body = f"""
Full Name: {instance.full_name}
Email: {instance.email}
Phone: {instance.phone}
Company: {instance.company_name}
Budget: {instance.budget}
Interests: {instance.interests.name if instance.interests else "N/A"}
Comment:
{instance.comment}
"""
        file_path = instance.file.path if instance.file else None
        send_form_email(subject, body, instance.email, file_path=file_path)


class ChatContactUSListCreateAPIView(generics.ListCreateAPIView):
    queryset = ChatContactUS.objects.all()
    serializer_class = ChatContactUSSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def perform_create(self, serializer):
        instance = serializer.save()
        subject = f"New Chat Contact Form Submission - {instance.full_name}"
        body = f"""
Full Name: {instance.full_name}
Email: {instance.email}
Phone: {instance.phone}
Company: {instance.company_name}
Session ID: {instance.session}
Link: {instance.link}
Comment:
{instance.comment}
"""
        send_form_email(subject, body, instance.email)








