from django.urls import path
from .views import LeadProcessView, ai_form_view

urlpatterns = [
    path('html/', ai_form_view, name='ai-form'),
    path('process/', LeadProcessView.as_view(), name='lead-process'),
]