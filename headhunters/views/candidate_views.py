# headhunters/views/candidate_views.py

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from profile_cv.models import Profile_CV
from ..forms import CandidateProfileForm

class CandidateListView(ListView):
    model = Profile_CV
    template_name = 'candidates/candidate_list.html'
    context_object_name = 'candidates'

class CandidateDetailView(DetailView):
    model = Profile_CV
    template_name = 'candidates/candidate_detail.html'
    context_object_name = 'candidate'

class CandidateCreateView(CreateView):
    model = Profile_CV
    form_class = CandidateProfileForm
    template_name = 'candidates/candidate_form.html'
    success_url = reverse_lazy('candidate_list')

class CandidateUpdateView(UpdateView):
    model = Profile_CV
    form_class = CandidateProfileForm
    template_name = 'candidates/candidate_form.html'
    success_url = reverse_lazy('candidate_list')

class CandidateDeleteView(DeleteView):
    model = Profile_CV
    template_name = 'candidates/candidate_confirm_delete.html'
    success_url = reverse_lazy('candidate_list')
