from django.urls import path
from .views import *

app_name = "courses"

urlpatterns = [


    path('courses/', courses_list_view, name = 'courses-list'),
    path('courses/<int:pk>', course_detail_view, name='course-detail'),
   

]