from django.urls import path
from . import views  # Make sure this import is correct

urlpatterns = [
    path('api/chatbot/', views.chatbot),
]
