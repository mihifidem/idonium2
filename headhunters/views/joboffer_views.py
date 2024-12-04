

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
    
    

class AddToExistingOfferView(View):
    def get(self, request, candidate_ids=None, *args, **kwargs):
        # Obtener todas las ofertas existentes
        offers = JobOffer.objects.all()

        # Procesar los IDs de candidatos seleccionados desde la URL
        selected_candidates = []
        if candidate_ids:
            candidate_ids_list = candidate_ids.split(",")
            selected_candidates = Profile_CV.objects.filter(id__in=candidate_ids_list)

        # Renderizar el template con los datos
        return render(request, 'joboffers/add_to_existing_offer.html', {
            'offers': offers,
            'selected_candidates': selected_candidates
        })

    def post(self, request, *args, **kwargs):
        # Obtener la oferta seleccionada
        offer_id = request.POST.get('selected_offer')
        if not offer_id:
            messages.error(request, 'Debe seleccionar una oferta.')
            return redirect('add_to_existing_offer', candidate_ids=",".join(request.POST.getlist('selected_candidates')))

        try:
            offer = JobOffer.objects.get(id=offer_id)
        except JobOffer.DoesNotExist:
            messages.error(request, 'Oferta no encontrada.')
            return redirect('add_to_existing_offer', candidate_ids=",".join(request.POST.getlist('selected_candidates')))
        # Obtener los IDs de candidatos seleccionados
        selected_candidates_ids = request.POST.getlist('selected_candidates')
        if not selected_candidates_ids:
            messages.error(request, 'No se seleccionaron candidatos.')
            return redirect('add_to_existing_offer', candidate_ids=",".join(request.POST.getlist('selected_candidates')))

        # Agregar los candidatos a la oferta evitando duplicados
        
        for candidate_id in selected_candidates_ids:
            try:
                candidate = Profile_CV.objects.get(id=candidate_id)
                 # Verificar si ya existe una relación entre el candidato y la oferta
                if not ManagementCandidates.objects.filter(job_offer=offer, candidate=candidate).exists():
                    # Si no existe, crear la relación
                    ManagementCandidates.objects.create(job_offer=offer, candidate=candidate)
                else:
                    messages.warning(request, f'El candidato {candidate.id} ya está asociado a esta oferta.')
                    
            except Profile_CV.DoesNotExist:
                messages.error(request, f'Candidato con ID {candidate_id} no encontrado.')
                continue

        messages.success(request, 'Candidatos agregados a la oferta con éxito.')
        return redirect('landing_headhunters')  # Cambiar a la página deseada después del éxito
