# headhunters/views/candidate_views.py

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ..models import CandidateProfile
from ..forms import CandidateProfileForm

class CandidateListView(ListView):
    model = CandidateProfile
    template_name = 'candidates/candidate_list.html'
    context_object_name = 'candidates'

class CandidateDetailView(DetailView):
    model = CandidateProfile
    template_name = 'candidates/candidate_detail.html'
    context_object_name = 'candidate'

class CandidateCreateView(CreateView):
    model = CandidateProfile
    form_class = CandidateProfileForm
    template_name = 'candidates/candidate_form.html'
    success_url = reverse_lazy('candidate_list')

class CandidateUpdateView(UpdateView):
    model = CandidateProfile
    form_class = CandidateProfileForm
    template_name = 'candidates/candidate_form.html'
    success_url = reverse_lazy('candidate_list')

class CandidateDeleteView(DeleteView):
    model = CandidateProfile
    template_name = 'candidates/candidate_confirm_delete.html'
    success_url = reverse_lazy('candidate_list')
