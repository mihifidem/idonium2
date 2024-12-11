

from django.urls import path
from .views import (
    CandidateListView, CandidateDetailView, CandidateCreateView, CandidateUpdateView, CandidateDeleteView,
    JobOfferListView, JobOfferDetailView, JobOfferCreateView, JobOfferUpdateView, JobOfferDeleteView,
    HeadhunterListView, HeadhunterDetailView, HeadhunterCreateView, HeadhunterUpdateView, HeadhunterDeleteView,
    ScheduleListView, ScheduleDetailView, ScheduleCreateView, ScheduleUpdateView, ScheduleDeleteView
)

urlpatterns = [
    path('candidates/', CandidateListView.as_view(), name='candidate_list'),
    path('candidates/<int:pk>/', CandidateDetailView.as_view(), name='candidate_detail'),
    path('candidates/create/', CandidateCreateView.as_view(), name='candidate_create'),
    path('candidates/<int:pk>/update/', CandidateUpdateView.as_view(), name='candidate_update'),
    path('candidates/<int:pk>/delete/', CandidateDeleteView.as_view(), name='candidate_delete'),

    path('joboffers/', JobOfferListView.as_view(), name='joboffer_list'),
    path('joboffers/<int:pk>/', JobOfferDetailView.as_view(), name='joboffer_detail'),
    path('joboffers/create/', JobOfferCreateView.as_view(), name='joboffer_create'),
    path('joboffers/<int:pk>/update/', JobOfferUpdateView.as_view(), name='joboffer_update'),
    path('joboffers/<int:pk>/delete/', JobOfferDeleteView.as_view(), name='joboffer_delete'),

    path('headhunters/', HeadhunterListView.as_view(), name='headhunter_list'),
    path('headhunters/<int:pk>/', HeadhunterDetailView.as_view(), name='headhunter_detail'),
    path('headhunters/create/', HeadhunterCreateView.as_view(), name='headhunter_create'),
    path('headhunters/<int:pk>/update/', HeadhunterUpdateView.as_view(), name='headhunter_update'),
    path('headhunters/<int:pk>/delete/', HeadhunterDeleteView.as_view(), name='headhunter_delete'),
    
    path('schedule/', ScheduleListView.as_view(), name='schedule_list'),
    path('schedule/<int:pk>/', ScheduleDetailView.as_view(), name='schedule_detail'),
    path('schedule/create/', ScheduleCreateView.as_view(), name='schedule_create'),
    path('schedule/<int:pk>/update/', ScheduleUpdateView.as_view(), name='schedule_update'),
    path('schedule/<int:pk>/delete/', ScheduleDeleteView.as_view(), name='schedule_delete'),
]
