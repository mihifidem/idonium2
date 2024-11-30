

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ..models import JobOffer, ManagementCandidates
from ..forms import JobOfferForm
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from profile_cv.models import Profile_CV


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
    




class CreateOfferView(View):
    def get(self, request, candidate_ids):
        # Obtener los IDs de candidatos seleccionados
        candidate_ids_list = candidate_ids.split(",")
        
        # Filtrar los candidatos según los IDs proporcionados
        candidates = Profile_CV.objects.filter(id__in=candidate_ids_list)
        
        # Crear un formulario vacío para crear una oferta de trabajo
        form = JobOfferForm()
        
        # Renderizar la plantilla con los candidatos y el formulario
        return render(request, 'joboffers/create_offer.html', {'form': form, 'candidates': candidates})

    def post(self, request, candidate_ids):
        # Manejar el envío del formulario
        form = JobOfferForm(request.POST)
        
        if form.is_valid():
            # Guardar la nueva oferta de trabajo
            job_offer = form.save()
            
            # Obtener los candidatos seleccionados con los IDs
            candidate_ids_list = candidate_ids.split(",")
            candidates = Profile_CV.objects.filter(id__in=candidate_ids_list)
            
            # Asociar los candidatos seleccionados a la oferta de trabajo
            for candidate in candidates:
                ManagementCandidates.objects.create(
                    job_offer=job_offer,
                    candidate=candidate,
                    is_selected_by_headhunter=True,
                )
            
            # Mostrar mensaje de éxito
            messages.success(request, '¡La oferta ha sido creada exitosamente y los candidatos han sido asociados!')
            
            # Redirigir al landing page o a otra vista después de crear la oferta
            return redirect('landing_headhunters')
        
        # Si el formulario no es válido, volver a mostrar el formulario con los errores
        return render(request, 'joboffers/create_offer.html', {'form': form})
