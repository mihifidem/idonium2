from django.urls import path
from .views import *

app_name = "courses"

urlpatterns = [
    # ----------- Course URL patterns --------------
    path('courses/', courses_list_view, name='courses-list'),                                    # List
    path('courses/<int:pk>/', course_detail_view, name='course-detail'),                         # Select/Read
    path('courses/add/', course_create_or_update_view, name='course-create'),                    # Create
    path('courses/<int:course_id>/edit/', course_create_or_update_view, name='course-update'),   # Update
    path('courses/<int:course_id>/delete/', course_delete_view, name='course-delete'),           # Delete

    # ----------- Module URL patterns --------------
    path('courses/<int:course_id>/module/add/', module_create_or_update_view, name='module-create'),                # Create
    path('courses/<int:course_id>/module/<int:module_id>/', module_create_or_update_view, name='module-update'),    # Update
    path('courses/<int:course_id>/module/<int:module_id>/delete/', module_delete_view, name='module-delete'),       # Delete

    # ----------- Lesson URL patterns --------------
    path('courses/<int:course_id>/module/<int:module_id>/lesson/add/', lesson_create_or_update_view, name='lesson-create'),                    # Create
    path('courses/<int:course_id>/module/<int:module_id>/lesson/<int:lesson_id>/edit/', lesson_create_or_update_view, name='lesson-update'),   # Update
    path('courses/<int:course_id>/module/<int:module_id>/lesson/<int:lesson_id>/delete/', lesson_delete_view, name='lesson-delete'),           # Delete

    # ----------- Resource_Course URL patterns --------------
    path('courses/<int:course_id>/module/<int:module_id>/lesson/<int:lesson_id>/resource/add/', 
        resource_course_create_or_update_view,                                                           
        name='resource-course-create'                                                                                           # Create
    ),  
    path('courses/<int:course_id>/module/<int:module_id>/lesson/<int:lesson_id>/resource/<int:resource_id>/edit/', 
        resource_course_create_or_update_view, 
        name='resource-course-update'                                                                                           # Update
    ),
    path('courses/<int:course_id>/module/<int:module_id>/lesson/<int:lesson_id>/resource/<int:resource_id>/delete/',
        resource_course_delete_view,
        name='resource-course-delete'                                                                                           # Delete
    ),

    # ----------- Certificate URL patterns --------------
    path('courses/<int:course_id>/certificate/add/', certificate_create_or_update_view, name='certificate-create'),                     # Create
    path('courses/<int:course_id>/certificate/<int:certificate_id>/', certificate_create_or_update_view, name='certificate-update'),    # Update
    path('courses/<int:course_id>/certificate/<int:certificate_id>/delete/', certificate_delete_view, name='certificate-delete'),       # Delete

    # ----------- Teacher URL patterns --------------
    path('teacher/courses/<int:course_id>/', teacher_course_detail_view, name='teacher-course-detail'),                  

    # ----------- Resources URL patterns --------------
    path('resources/', resources_list_view, name = 'resources-list'),
]