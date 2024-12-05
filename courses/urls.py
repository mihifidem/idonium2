from django.urls import path
from .views import *

app_name = "courses"

urlpatterns = [
    # Course URL patterns
    path('courses/', courses_list_view, name = 'courses-list'),
    path('courses/<int:pk>/', course_detail_view, name='course-detail'),
    path('courses/edit/<int:pk>/', course_create_or_update_view, name='course-update'),
    path('courses/add/', course_create_or_update_view, name='course-create'),
    #path('courses/<int:course_id>/edit/', course_module_view, name='course_module_view'),

    # Teacher URL patterns
    path('teacher/courses/', teacher_courses_list_view, name='teacher-courses-list'),

    # Resource URL patterns
    path('resources/', resources_list_view, name = 'resources-list'),
]