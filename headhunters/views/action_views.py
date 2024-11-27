# headhunters/views/action_views.py

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ..models import Action
from ..forms import ActionForm

class ActionListView(ListView):
    model = Action
    template_name = 'actions/action_list.html'
    context_object_name = 'actions'

class ActionDetailView(DetailView):
    model = Action
    template_name = 'actions/action_detail.html'
    context_object_name = 'action'

class ActionCreateView(CreateView):
    model = Action
    form_class = ActionForm
    template_name = 'actions/action_form.html'
    success_url = reverse_lazy('action_list')

class ActionUpdateView(UpdateView):
    model = Action
    form_class = ActionForm
    template_name = 'actions/action_form.html'
    success_url = reverse_lazy('action_list')

class ActionDeleteView(DeleteView):
    model = Action
    template_name = 'actions/action_confirm_delete.html'
    success_url = reverse_lazy('action_list')
