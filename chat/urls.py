from django.urls import path
from .views import SendMessageView, SubmitFormView ,ChatHistoryView

urlpatterns = [
    path('chat/send-message/', SendMessageView.as_view()),
    path('chat/submit-form/', SubmitFormView.as_view()),
    path('chat/history/', ChatHistoryView.as_view()),

]
