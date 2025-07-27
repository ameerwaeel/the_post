# main_app/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('interests/', InterestsListCreateAPIView.as_view(), name="interests"),
    path('interests/<uuid:uuid>/', InterestsDetailView.as_view(), name="interests"),
    path('contact/', ContactUSListCreateAPIView.as_view(), name="contact-us"),
    path('chat-contact/', ChatContactUSListCreateAPIView.as_view(), name="chat-contact-us"),
    path('newsletter/', NewsLetterListCreateView.as_view()),

]
