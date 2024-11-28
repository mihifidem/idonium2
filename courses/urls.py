from django.urls import path
from .views import *

app_name = "courses"

urlpatterns = [


    path('courses/', courses_list_view, name = 'courses-list'),
    path('courses_detail/', course_detail_view, name='course-detail'),
    # path('police_officers/', CourseListView.as_view(), name='course-list'),
    # path('police_officer/create/',CourseCreateView.as_view(), name='course-create'),
    # path('police_officer/<int:pk>/update/', CourseUpdateView.as_view(), name='course-update'),
    # path('courses/user-certificates/<int:pk>/update/', CertificationUpdateView.as_view(), name= 'usercertification-update'),
    # path('courses/user-certificates/create/', CertificationCreateView.as_view(), name= 'usercertification-create'),
    # path('courses/user-certificates/', UserCertificateListView.as_view(), name='usercertification-list'),
    # path('courses/certificates/', CertificateListView.as_view(), name='certificate-list'),
    # path('courses/certificates/<int:pk>/update/', CertificateUpdateView.as_view(), name='certificate-update'),
    # path('courses/certificates/create/', CertificateCreateView.as_view(), name='certificate-create'),

]