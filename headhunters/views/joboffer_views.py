

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from ..models import JobOffer, ManagementCandidates, HeadHunterUser,JobOffersWishList
from ..forms import JobOfferForm
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from profile_cv.models import Profile_CV
from django.contrib.auth.mixins import LoginRequiredMixin



class JobOfferListView(ListView):
    model = JobOffer
    template_name = 'joboffers/joboffer_list.html'
    context_object_name = 'job_offers'
    def get_queryset(self):
        groups = list(self.request.user.groups.all())
        if 'premium' in [group.name for group in groups] or 'freemium' in [group.name for group in groups]:
            return JobOffer.objects.all()
        if 'headhunter' in [group.name for group in groups]:
            headhunter = get_object_or_404(HeadHunterUser, user=self.request.user)
            return JobOffer.objects.filter(headhunter=headhunter)

class JobOfferDetailView(DetailView):
    model = JobOffer
    template_name = 'joboffers/joboffer_detail.html'
    context_object_name = 'job_offer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener la oferta de trabajo actual
        job_offer = self.get_object()

        # Obtener todos los candidatos relacionados a través de ManagementCandidates
        all_candidates = ManagementCandidates.objects.filter(job_offer=job_offer).select_related('candidate')

        # Filtrar candidatos por los que están seleccionados por el headhunter
        selected_candidates = all_candidates.filter(is_selected_by_headhunter=True)
        
        # Filtrar candidatos por los que aplicaron directamente
        direct_application_candidates = all_candidates.filter(applied_directly=True)

        # Añadir los candidatos seleccionados y los aplicados directamente al contexto
        context['selected_candidates'] = selected_candidates
        context['direct_application_candidates'] = direct_application_candidates

        return context



class JobOfferUpdateView(UpdateView):
    model = JobOffer
    form_class = JobOfferForm
    template_name = 'joboffers/update_offer.html'
    success_url = reverse_lazy('joboffer_list')
    def get_object(self, queryset=None):
        # Usamos el ID de la oferta de trabajo que se pasa a través de la URL
        job_offer_id = self.kwargs.get('pk') 
        return get_object_or_404(JobOffer, id=job_offer_id)
    
    def form_valid(self, form):
        # Aquí puedes agregar cualquier lógica adicional antes de guardar los datos
        headhunter = get_object_or_404(HeadHunterUser, user=self.request.user)
        form.instance.headhunter = headhunter
        return super().form_valid(form)
    
    

class JobOfferDeleteView(DeleteView):
    model = JobOffer
    template_name = 'joboffers/joboffer_confirm_delete.html'
    success_url = reverse_lazy('joboffer_list')
    
class JobOfferCreateView(CreateView):
    model = JobOffer
    form_class = JobOfferForm
    template_name = 'joboffers/create_offer.html'
    success_url = reverse_lazy('joboffer_list')
    
    def form_valid(self, form):
        # Aquí puedes agregar cualquier lógica adicional antes de guardar los datos
        headhunter = get_object_or_404(HeadHunterUser, user=self.request.user)
        form.instance.headhunter = headhunter
        return super().form_valid(form)



class CreateOfferFromSelectedView(View):
    def get(self, request, candidate_ids=None):
        # Obtener los IDs de candidatos seleccionados si se proporcionan
        candidates = []
        if candidate_ids:
            candidate_ids_list = candidate_ids.split(",")
            candidates = Profile_CV.objects.filter(id__in=candidate_ids_list)
        
        # Crear un formulario vacío para crear una oferta de trabajo
        form = JobOfferForm()
        
        # Renderizar la plantilla con los candidatos y el formulario
        return render(request, 'joboffers/create_offer_from_selected.html', {'form': form, 'candidates': candidates})

    def post(self, request, candidate_ids=None):
        # Manejar el envío del formulario
        form = JobOfferForm(request.POST)
        
        if form.is_valid():
            # Obtener el objeto HeadhunterUser correspondiente al usuario autenticado
            headhunter = get_object_or_404(HeadHunterUser, user=self.request.user)
            
            # Asignar el headhunter al formulario antes de guardarlo
            job_offer = form.save(commit=False)
            job_offer.headhunter = headhunter
            job_offer.save()
            
            # Obtener los candidatos seleccionados si se proporcionan
            if candidate_ids:
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
            #messages.success(request, '¡La oferta ha sido creada exitosamente y los candidatos han sido asociados!')
            
            # Redirigir al landing page o a otra vista después de crear la oferta
            return redirect('landing_headhunters')
        
        # Si el formulario no es válido, volver a mostrar el formulario con los errores
        return render(request, 'joboffers/create_offer_from_selected.html', {'form': form})
    
    

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
                    ManagementCandidates.objects.create(job_offer=offer, candidate=candidate, is_selected_by_headhunter=True)
                    
                else:
                    messages.warning(request, f'El candidato {candidate.id} ya está asociado a esta oferta.')
                    
            except Profile_CV.DoesNotExist:
                messages.error(request, f'Candidato con ID {candidate_id} no encontrado.')
                continue

        messages.success(request, 'Candidatos agregados a la oferta con éxito.')
        return redirect('landing_headhunters')  # Cambiar a la página deseada después del éxito
    
    
class DeleteCandidateView(LoginRequiredMixin, DeleteView):
    model = ManagementCandidates
    template_name = 'joboffers/candidate_confirm_delete.html'
    def get_success_url(self):
        # Redirige al detalle de la oferta después de la eliminación
        job_offer_id = self.object.job_offer.id
        return reverse('joboffer_detail', kwargs={'pk': job_offer_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar información adicional para mostrar en la confirmación de eliminación
        context['candidate_name'] = self.object.candidate.user.username
        context['job_offer_title'] = self.object.job_offer.title
        return context
    
    
class WishListView(LoginRequiredMixin, ListView):
    model = JobOffersWishList
    template_name = "wishlist/jobofferswishlist_list.html"
    context_object_name = "wishlist"

    def get_queryset(self):
        # Filtra las ofertas guardadas del candidato actual
        candidate = get_object_or_404(Profile_CV, user=self.request.user)
        return JobOffersWishList.objects.filter(candidate=candidate)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wishlist_count'] = self.get_queryset().count()
        return context


class AddToWishListView(LoginRequiredMixin, CreateView):
    model = JobOffersWishList
    fields = []
    success_url = reverse_lazy('wishlist')  # Cambia esta URL si es necesario

    def form_valid(self, form):
        candidate = get_object_or_404(Profile_CV, user=self.request.user)
        job_offer = get_object_or_404(JobOffer, id=self.kwargs['job_offer_id'])
        if JobOffersWishList.objects.filter(candidate=candidate, job_offer=job_offer).exists():
            messages.warning(self.request, "Esta oferta ya está en tu Wishlist.")
            return redirect(self.success_url)
        form.instance.candidate = candidate
        form.instance.job_offer = job_offer
        return super().form_valid(form)


class RemoveFromWishListView(LoginRequiredMixin, DeleteView):
    model = JobOffersWishList
    template_name = "wishlist/jobofferswishlist_confirm_delete.html"
    success_url = reverse_lazy("wishlist")

    def get_queryset(self):
        # Asegurarse de que solo pueda eliminar elementos de su propia lista
        candidate = get_object_or_404(Profile_CV, user=self.request.user)
        return JobOffersWishList.objects.filter(candidate=candidate)

    