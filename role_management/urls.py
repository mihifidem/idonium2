from django.urls import path
from .views import teacher_dashboard,dashboard

urlpatterns = [
    path('',dashboard,name='dashboard'),
     path('teacher_dashboard/', teacher_dashboard, name='teacher_dashboard'),
 
    
]
