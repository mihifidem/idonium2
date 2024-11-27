

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ..models import JobOffer
from ..forms import JobOfferForm

class JobOfferListView(ListView):
    model = JobOffer
    template_name = 'joboffers/joboffer_list.html'
    context_object_name = 'job_offers'

class JobOfferDetailView(DetailView):
    model = JobOffer
    template_name = 'joboffers/joboffer_detail.html'
    context_object_name = 'job_offer'

class JobOfferCreateView(CreateView):
    model = JobOffer
    form_class = JobOfferForm
    template_name = 'joboffers/joboffer_form.html'
    success_url = reverse_lazy('joboffer_list')

class JobOfferUpdateView(UpdateView):
    model = JobOffer
    form_class = JobOfferForm
    template_name = 'joboffers/joboffer_form.html'
    success_url = reverse_lazy('joboffer_list')

class JobOfferDeleteView(DeleteView):
    model = JobOffer
    template_name = 'joboffers/joboffer_confirm_delete.html'
    success_url = reverse_lazy('joboffer_list')
