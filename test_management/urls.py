from django.urls import path

import users
from . import views
from .views import chatbot_response
from django.contrib import admin
from django.urls import path, include
from .views import chatbot_response

    # """URLS"""
urlpatterns = [
    # Quiz URLs
    path('', views.quiz_view, name='quiz_view'),
    path("submit/", views.submit_quiz, name="submit_quiz"),
    # Chatbot URLs
    path('chatbot/', views.chatbot_page, name='chatbot_page'),
    path('chatbot/view/', views.chatbot_view, name='chatbot_view'),  # Chatbot backend endpoint
]