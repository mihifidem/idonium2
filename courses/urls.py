from django.urls import path
from .views import *

app_name = "courses"

urlpatterns = [
    # ----------- Course URL patterns --------------
    # Courses URLs
    path('courses/', courses_list_view, name='courses-list'),
    path('courses/<int:pk>/', course_detail_view, name='course-detail'),
    path('courses/add/', course_create_or_update_view, name='course-create'),
    path('courses/<int:course_id>/edit/', course_create_or_update_view, name='course-update'),

    # Module URLs
    path('courses/<int:course_id>/module/add/', module_create_or_update_view, name='module-create'),
    path('courses/<int:course_id>/module/<int:module_id>/', module_create_or_update_view, name='module-update'),

    # Lesson URLs
    path('courses/<int:course_id>/module/<int:module_id>/lesson/add/', lesson_create_or_update_view, name='lesson-create'),
    path('courses/<int:course_id>/module/<int:module_id>/lesson/<int:lesson_id>/edit/', lesson_create_or_update_view, name='lesson-update'),

    # Resource_course URLs
    path('courses/<int:course_id>/module/<int:module_id>/lesson/<int:lesson_id>/resource/add/', resource_course_create_or_update_view, name='resource-create'),
    path('courses/<int:course_id>/module/<int:module_id>/lesson/<int:lesson_id>/resource/<int:resource_id>/edit/', resource_course_create_or_update_view, name='resource-update'),

    # ----------- Teacher URL patterns --------------
    path('teacher/courses/', teacher_courses_list_view, name='teacher-courses-list'),
    path('teacher/courses/<int:course_id>/', teacher_course_detail_view, name='teacher-course-detail'),

    # ----------- Resources URL patterns --------------
    path('resources/', resources_list_view, name = 'resources-list'),
]