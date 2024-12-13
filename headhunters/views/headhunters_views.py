

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ..models import HeadHunterUser,JobOffer,ManagementCandidates
from ..forms import HeadHunterForm
from django.shortcuts import render,redirect,get_object_or_404
from profile_cv.models import Profile_CV,HardSkill, SoftSkill
from django.views import View
from django.http import JsonResponse
from django.db.models import Q




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
    
    def form_valid(self, form):
        #Guardo el headhunter en la base de datos
        headhunter = form.save()
        #lo redirigo a el detalle del headhunter
        return redirect('headhunter_detail', pk=headhunter.pk)

class HeadhunterUpdateView(UpdateView):
    model = HeadHunterUser
    form_class = HeadHunterForm
    template_name = 'headhunters/headhunter_form.html'
    success_url = reverse_lazy('headhunter_list')

class HeadhunterDeleteView(DeleteView):
    model = HeadHunterUser
    template_name = 'headhunters/headhunter_confirm_delete.html'
    success_url = reverse_lazy('headhunter_list')
    
    
class LandingHeadHuntersView(ListView):
    model = Profile_CV
    template_name = 'headhunters/landing_headhunters.html'
    context_object_name = 'candidates'
    
    

    def get_queryset(self):
        queryset = super().get_queryset()

        # Obtener filtros de manera más segura
        location_filter = self.request.GET.get('location', '')
        availability_filter = self.request.GET.get('open_to_work', '')
        vehicle_filter = self.request.GET.get('vehicle', '')
        disability_filter = self.request.GET.get('disability', '')
        disability_percentage_filter = self.request.GET.get('disability_percentage', '')

        # Filtrar por ubicación
        if location_filter:
            queryset = queryset.filter(address__icontains=location_filter)

        # Filtro por disponibilidad
        if availability_filter.lower() in ['true', 'false']:
            queryset = queryset.filter(open_to_work=availability_filter.lower() == 'true')

        # Filtro por vehículo
        if vehicle_filter.lower() in ['true', 'false']:
            queryset = queryset.filter(vehicle=vehicle_filter.lower() == 'true')

        # Filtro por discapacidad
        if disability_filter.lower() in ['true', 'false']:
            queryset = queryset.filter(disability=disability_filter.lower() == 'true')

        # Filtro por porcentaje de discapacidad
        if disability_percentage_filter.isdigit():
            queryset = queryset.filter(disability_percentage__gte=int(disability_percentage_filter))

        return queryset



 #Esta Vista relacionara los candidatos seleccionados con la oferta:


class ManageCandidatesView(View):
    def post(self, request, *args, **kwargs):
        # Obtener los candidatos seleccionados y la acción
        selected_candidates_ids = request.POST.getlist("selected_candidates")
        action = request.POST.get("action")

        # Verificar si se seleccionaron candidatos
        if not selected_candidates_ids:
            return redirect("landing_headhunters")

        candidates = Profile_CV.objects.filter(id__in=selected_candidates_ids)

        # Realizar acción según el valor de 'action'
        if action == "create_offer":
            return redirect("create_offer", candidate_ids=",".join(selected_candidates_ids))

        elif action == "add_to_existing_offer":
            return redirect("add_to_existing_offer", candidate_ids=",".join(selected_candidates_ids))

        return redirect("landing_headhunters")
    
    

from django.db.models import Q
from django.http import JsonResponse
from django.views import View

class CandidateSearchView(View):
    """
    View to search candidates based on specific criteria.
    """
    def get(self, request):
        query = request.GET.get('query', '').lower()

        # Separar palabras de la consulta
        search_keywords = query.split()

        # Inicializar queryset base
        candidates = Profile_CV.objects.all()

        # Crear un objeto Q vacío para combinar los filtros
        filter_conditions = Q()

        # Filtrar por cada palabra clave
        for keyword in search_keywords:
            # Filtrar por habilidades técnicas
            filter_conditions |= Q(
                hardskilluser__hard_skill__name_hard_skill__icontains=keyword
            )
            # Filtrar por habilidades blandas
            filter_conditions |= Q(
                softskilluser__soft_skill__name_soft_skill__icontains=keyword
            )
            # Filtrar por dirección
            filter_conditions |= Q(address__icontains=keyword)
            # Filtrar por biografía
            filter_conditions |= Q(biography__icontains=keyword)
            # Filtrar por vehículo
            if keyword in ['vehicle', 'car', 'transport']:
                filter_conditions |= Q(vehicle=True)
            # Filtrar por discapacidad
            if keyword in ['disability', 'disabled', 'accessible']:
                filter_conditions |= Q(disability=True)


        # Aplicar el filtro compuesto al queryset
        candidates = candidates.filter(filter_conditions)

        # Quitar duplicados en caso de filtros múltiples
        candidates = candidates.distinct()

        # Serializar resultados
        results = [
            {
                "id": candidate.id,
                "username": candidate.user.username,
                "email": candidate.email_1,
                "phone": candidate.phone_1,
                "address": candidate.address,
                "biography": candidate.biography,
                "vehicle": candidate.vehicle,
                "disability": candidate.disability,
                "disability_percentage": candidate.disability_percentage,
            }
            for candidate in candidates
        ]

        return JsonResponse({"candidates": results})
