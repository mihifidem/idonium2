

from django.urls import path
from .views import (
    JobOfferListView, JobOfferDetailView, JobOfferCreateView, JobOfferUpdateView, JobOfferDeleteView,
    HeadhunterListView, HeadhunterDetailView, HeadhunterCreateView, HeadhunterUpdateView, HeadhunterDeleteView,
    ScheduleListView, ScheduleDetailView, ScheduleCreateView, ScheduleUpdateView, ScheduleDeleteView,
    LandingHeadHuntersView,
    manage_candidates,
    # #create_offer_view, add_to_offer_view,
)


urlpatterns = [
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
    path("landing/", LandingHeadHuntersView.as_view(), name="landing_headhunters"),
    
     #Rutas para gestion de candidatos en la landing
     #
    path("manage-candidates/", manage_candidates, name="manage_candidates"),
    # path("create-offer/<str:candidate_ids>/", create_offer_view, name="create_offer"),
    # path("add-to-offer/<str:candidate_ids>/", add_to_offer_view, name="add_to_offer"),
]
