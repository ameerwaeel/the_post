from django.urls import path
from .views import LeadProcessView

urlpatterns = [
    path('process/', LeadProcessView.as_view(), name='lead-process'),
]