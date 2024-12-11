from django.urls import path

import users
from . import views
from .views import chatbot_response
from django.contrib import admin
from django.urls import path, include
from .views import chatbot_response

    # """URLS"""
urlpatterns = [
    path('', views.quiz_view, name = 'quiz_view'),
    path("create_test/", views.create_test, name="create_test"),
    path("add_questions/<int:test_id>/", views.add_questions, name="add_questions"),
    path("take_test/<int:test_id>/", views.take_test, name="take_test"),
    #path("avalable_tests/", views.available_tests, name="avalable_tests"),
    # path("resolve_json_test/", views.resolve_json_test, name="resolve_json_test"),
    # path('test_view', views.quiz_view, name='quiz_view'),  # Initial quiz selection
    # path("register/", views.register, name="register"),
    # path("login/", views.login_view, name="login"),
    # path('admin/', admin.site.urls),
   # Include the quiz app URLs
    path("submit/", views.submit_quiz, name="submit_quiz"),
    path('chatbot/', views.chatbot_page, name='chatbot_page'),  # This renders the chatbot page (GET)
    path('chatbot/view/', views.chatbot_view, name='chatbot_view'),  # This handles chatbot interaction (POST)
]