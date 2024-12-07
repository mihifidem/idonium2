from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ..forms import ScheduleForm
from ..models import Schedule,HeadHunterUser,JobOffer,ManagementCandidates
from profile_cv.models import Profile_CV
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse,request

# Vista para listar eventos en la agenda
class ScheduleListView(ListView):
    model = Schedule
    template_name = 'schedule/schedule_list.html'
    context_object_name = 'schedule'
    def get_queryset(self):
        headhunter = get_object_or_404(HeadHunterUser, user=self.request.user)
        return Schedule.objects.filter(headhunter=headhunter)

# Vista para ver detalles de un evento de la agenda
class ScheduleDetailView(DetailView):
    model = Schedule
    template_name = 'schedule/schedule_detail.html'
    context_object_name = 'schedule'

# Vista para crear un nuevo evento en la agenda
class ScheduleCreateView(CreateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'schedule/schedule_form.html'
    success_url = reverse_lazy('schedule_list')
    
    def get_initial(self):
        initial = super().get_initial()
        # Obtener los parámetros de la URL
        joboffer_id = self.request.GET.get('joboffer_id')
        candidate_id = self.request.GET.get('candidate_id')

        # Si existen los parámetros, pre-cargar los campos
        if joboffer_id:
            joboffer = get_object_or_404(JobOffer, id=joboffer_id)
            initial['joboffer'] = joboffer

        if candidate_id:
            candidate = get_object_or_404(Profile_CV, id=candidate_id)
            initial['candidate'] = candidate

        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        headhunter = get_object_or_404(HeadHunterUser, user=self.request.user)
        form.fields['joboffer'].queryset = JobOffer.objects.filter(headhunter=headhunter)
        # Obtener los parámetros de la URL
        joboffer_id = self.request.GET.get('joboffer_id')
        candidate_id = self.request.GET.get('candidate_id')

        if joboffer_id:
            joboffer = get_object_or_404(JobOffer, id=joboffer_id)
            form.instance.joboffer = joboffer

        if candidate_id:
            candidate = get_object_or_404(Profile_CV, id=candidate_id)
            form.instance.candidate = candidate
        return form

    def form_valid(self, form):
        headhunter = get_object_or_404(HeadHunterUser, user=self.request.user)
        form.instance.headhunter = headhunter
        return super().form_valid(form)


# Vista para actualizar un evento de la agenda
class ScheduleUpdateView(UpdateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'schedule/schedule_form.html'
    success_url = reverse_lazy('schedule_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        headhunter = get_object_or_404(HeadHunterUser, user=self.request.user)
        form.fields['joboffer'].queryset = JobOffer.objects.filter(headhunter=headhunter)
        return form
        
    def form_valid(self, form):
        headhunter = get_object_or_404(HeadHunterUser, user=self.request.user)
        form.instance.headhunter = headhunter
        return super().form_valid(form)

# Vista para eliminar un evento de la agenda
class ScheduleDeleteView(DeleteView):
    model = Schedule
    template_name = 'schedule/schedule_confirm_delete.html'
    success_url = reverse_lazy('schedule_list')
    
    
def get_candidates(request,joboffer_id):
    print(f"Esto es lo que recibo como joboffer {joboffer_id}" )
    
    candidate_ids = ManagementCandidates.objects.filter(job_offer_id=joboffer_id).values_list('candidate_id', flat=True)
    
    print(f"Los candidatos relaciondas a la oferta:  {joboffer_id} son los: {candidate_ids}" )
    
    candidates = Profile_CV.objects.filter(id__in=candidate_ids)

    candidates_list = [{'id': candidate.id, 'name': candidate.user.username} for candidate in candidates]
    print(JsonResponse({'candidates': candidates_list}))

    
    return JsonResponse({'candidates': candidates_list})
