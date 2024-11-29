from django.urls import path
from . import views
from django.urls import path, include

    # """URLS"""
urlpatterns = [
    path("create_test/", views.create_test, name="create_test"),
    path("add_questions/<int:test_id>/", views.add_questions, name="add_questions"),
    path("take_test/<int:test_id>/", views.take_test, name="take_test"),
    path('', views.quiz_view, name='quiz_view'),  # Initial quiz selection
    path('submit_test/', views.submit_quiz, name='submit_quiz'),  # Handle form submission and result display
    path("submit/", views.submit_quiz, name="submit_quiz"),
]