from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ..forms import ScheduleForm
from ..models import Schedule
from django.contrib.auth.mixins import LoginRequiredMixin

# Vista para listar eventos en la agenda
class ScheduleListView(ListView):
    model = Schedule
    template_name = 'schedule/schedule_list.html'
    context_object_name = 'schedule_list'

    # def get_queryset(self):
    #     # Filtra los eventos de la agenda para el headhunter actual
    #     return Schedule.objects.filter(headhunter=self.request.user.headhunter)

# Vista para ver detalles de un evento de la agenda
class ScheduleDetailView(DetailView):
    model = Schedule
    template_name = 'schedule/schedule_detail.html'
    context_object_name = 'schedule'

    # def get_queryset(self):
    #     # Solo permite acceder a eventos del headhunter actual
    #     return Schedule.objects.filter(headhunter=self.request.user.headhunter)

# Vista para crear un nuevo evento en la agenda
class ScheduleCreateView(CreateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'schedule/schedule_form.html'
    success_url = reverse_lazy('schedule_list')

    # def form_valid(self, form):
    #     # Asocia el evento al headhunter actual
    #     form.instance.headhunter = self.request.user.headhunter
    #     return super().form_valid(form)

# Vista para actualizar un evento de la agenda
class ScheduleUpdateView(UpdateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'schedule/schedule_form.html'
    success_url = reverse_lazy('schedule_list')

    # def get_queryset(self):
    #     # Solo permite actualizar eventos del headhunter actual
    #     return Schedule.objects.filter(headhunter=self.request.user.headhunter)

# Vista para eliminar un evento de la agenda
class ScheduleDeleteView(DeleteView):
    model = Schedule
    template_name = 'schedule/schedule_confirm_delete.html'
    success_url = reverse_lazy('schedule_list')

    # def get_queryset(self):
        # Solo permite eliminar eventos del headhunter actual
        # return Schedule.objects.filter(headhunter=self.request.user.headhunter)
