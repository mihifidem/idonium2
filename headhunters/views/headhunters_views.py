

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ..models import HeadHunter
from ..forms import HeadHunterForm

class HeadhunterListView(ListView):
    model = HeadHunter
    template_name = 'headhunters/headhunter_list.html'
    context_object_name = 'headhunters'

class HeadhunterDetailView(DetailView):
    model = HeadHunter
    template_name = 'headhunters/headhunter_detail.html'
    context_object_name = 'headhunter'

class HeadhunterCreateView(CreateView):
    model = HeadHunter
    form_class = HeadHunterForm
    template_name = 'headhunters/headhunter_form.html'
    success_url = reverse_lazy('headhunter_list')

class HeadhunterUpdateView(UpdateView):
    model = HeadHunter
    form_class = HeadHunterForm
    template_name = 'headhunters/headhunter_form.html'
    success_url = reverse_lazy('headhunter_list')

class HeadhunterDeleteView(DeleteView):
    model = HeadHunter
    template_name = 'headhunters/headhunter_confirm_delete.html'
    success_url = reverse_lazy('headhunter_list')
