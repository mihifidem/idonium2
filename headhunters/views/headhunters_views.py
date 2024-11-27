

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ..models import HeadHunterUser
from ..forms import HeadHunterForm

class HeadhunterListView(ListView):
    model = HeadHunterUser
    template_name = 'headhunters/headhunter_list.html'
    context_object_name = 'headhunters'

class HeadhunterDetailView(DetailView):
    model = HeadHunterUser
    template_name = 'headhunters/headhunter_detail.html'
    context_object_name = 'headhunter'

class HeadhunterCreateView(CreateView):
    model = HeadHunterUser
    form_class = HeadHunterForm
    template_name = 'headhunters/headhunter_form.html'
    success_url = reverse_lazy('headhunter_list')

class HeadhunterUpdateView(UpdateView):
    model = HeadHunterUser
    form_class = HeadHunterForm
    template_name = 'headhunters/headhunter_form.html'
    success_url = reverse_lazy('headhunter_list')

class HeadhunterDeleteView(DeleteView):
    model = HeadHunterUser
    template_name = 'headhunters/headhunter_confirm_delete.html'
    success_url = reverse_lazy('headhunter_list')
