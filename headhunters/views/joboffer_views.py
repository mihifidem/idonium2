

from django.forms import FileField, ImageField, model_to_dict
from django.http import JsonResponse
from datetime import datetime
import json
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from ..models import JobOffer, ManagementCandidates, HeadHunterUser,JobOffersWishList
from ..forms import JobOfferForm
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from profile_cv.models import Category, HardSkill, Profile_CV, Sector, SoftSkill, User_cv, UserCvRelation
from django.contrib.auth.mixins import LoginRequiredMixin



class JobOfferListView(ListView):
    model = JobOffer
    template_name = 'joboffers/joboffer_list.html'
    context_object_name = 'job_offers'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        groups = list(self.request.user.groups.all())        
        
        title = self.request.GET.get('title', None)
        sector = self.request.GET.get('sector', None)
        category = self.request.GET.get('category', None)
        salary_min = self.request.GET.get('salary_min', None)
        salary_max = self.request.GET.get('salary_max', None)
        location = self.request.GET.get('location', None)
        required_hard_skills = self.request.GET.getlist('required_hard_skills', [])
        required_soft_skills = self.request.GET.getlist('required_soft_skills', [])
        required_experience = self.request.GET.get('required_experience', None)
        job_offer_tests = self.request.GET.getlist('job_offer_tests', [])

        # Filtramos dinámicamente basado en los parámetros recibidos
        if title:
            queryset = queryset.filter(title__icontains=title)
        
        if sector:
            queryset = queryset.filter(sector__id=sector)
        
        if category:
            queryset = queryset.filter(category__id=category)
        
        if salary_min:
            queryset = queryset.filter(salary__gte=salary_min)
        
        if salary_max:
            queryset = queryset.filter(salary__lte=salary_max)
        
        if location:
            queryset = queryset.filter(location__icontains=location)

        if required_experience:
            queryset = queryset.filter(required_experience__gte=required_experience)

        if required_hard_skills:
            queryset = queryset.filter(required_hard_skills__id__in=required_hard_skills)
        
        if required_soft_skills:
            queryset = queryset.filter(required_soft_skills__id__in=required_soft_skills)

        if job_offer_tests:
            queryset = queryset.filter(JobOfferTests__id__in=job_offer_tests)

        queryset = queryset.distinct()

        if 'headhunter' in [group.name for group in groups]:
            headhunter = get_object_or_404(HeadHunterUser, user=self.request.user)
            return queryset.filter(headhunter=headhunter)
        else:
            return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = list(self.request.user.groups.all())
        # Añadimos los filtros disponibles al contexto
        context['sectors'] = Sector.objects.all()
        context['categories'] = Category.objects.all()
        context['hard_skills'] = HardSkill.objects.all()
        context['soft_skills'] = SoftSkill.objects.all()
        context['is_headhunter'] = groups[0].name == 'headhunter'
        context['active_filter'] = True
        return context


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
    template_name = "joboffers/jobofferswishlist_list.html"
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
    template_name = "joboffers/jobofferswishlist_confirm_delete.html"
    success_url = reverse_lazy("wishlist")

    def get_queryset(self):
        # Asegurarse de que solo pueda eliminar elementos de su propia lista
        candidate = get_object_or_404(Profile_CV, user=self.request.user)
        return JobOffersWishList.objects.filter(candidate=candidate)


class ApplyDirectToOffer(View):
    def __get_user_profile(self, id_candidato):
        return Profile_CV.objects.get(user=id_candidato)

    def __get_offer(self, id_oferta):
        return JobOffer.objects.get(pk=id_oferta)

    def post(self, request, *args, **kwargs):
        id_candidato = self.__get_user_profile(self.request.user.id)
        body = json.loads(request.body)
        id_oferta = body.get('id_oferta')
        offer = self.__get_offer(id_oferta)
        
        # Obtenemos la oferta en la tabla ManagementCandidates que tenga el mismo id del candidato y de oferta
        current_offer_apply = ManagementCandidates.objects.filter(job_offer=id_oferta, candidate=id_candidato).first()
        
        if current_offer_apply:
            # Si existe, actualizamos la bandera 'applied_directly'
            current_offer_apply.applied_directly = True
            current_offer_apply.save()
        else:
            # Si no existe, creamos un nuevo registro en ManagementCandidates
            management_candidate = ManagementCandidates.objects.create(
                job_offer=offer, 
                candidate=id_candidato,
                is_selected_by_headhunter=False,
                applied_directly=True,
                application_date=datetime.now()
            )

        # Devolvemos la respuesta con los datos actualizados o creados
        return JsonResponse({
            'job_offer': current_offer_apply.job_offer.title if current_offer_apply else management_candidate.job_offer.title,
            'candidate': current_offer_apply.candidate.user.username if current_offer_apply else management_candidate.candidate.user.username,
            'is_selected_by_headhunter': current_offer_apply.is_selected_by_headhunter if current_offer_apply else management_candidate.is_selected_by_headhunter,
            'applied_directly': current_offer_apply.applied_directly if current_offer_apply else management_candidate.applied_directly,
            'application_date': current_offer_apply.application_date if current_offer_apply else management_candidate.application_date,
        })
    
class MyOffers(ListView):
    model = JobOffer
    template_name = 'joboffers/joboffer_list.html'
    context_object_name = 'job_offers'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_filter'] = False
        return context
    
    def get_queryset(self):
        super().get_queryset()
        management_candidates = ManagementCandidates.objects.filter(candidate__user=self.request.user)
        print(JobOffer.objects.filter(id__in=management_candidates.values('job_offer')))
        return JobOffer.objects.filter(id__in=management_candidates.values('job_offer'))

from django.http import JsonResponse
from django.forms import model_to_dict
from django.db.models import ImageField, FileField, ForeignKey, ManyToManyField, OneToOneField

from django.http import JsonResponse
from django.forms import model_to_dict
from django.db.models import ImageField, FileField, ForeignKey, ManyToManyField, OneToOneField

from django.db import models

class RecomendationOffers(ListView):

    def serialize_model(self, instance):
        """
        Serializa un modelo excluyendo los campos no serializables (por ejemplo, ImageField, FileField).
        Si un campo es una relación (ForeignKey, ManyToMany), lo serializa recursivamente.
        """
        # Asegurarnos de que estamos trabajando con una instancia del modelo
        if not instance:
            return {}

        # Convertir el modelo a un diccionario
        for object in instance:
        data = model_to_dict(instance)

        for field in instance._meta.get_fields():
            field_name = field.name

            # Si el campo es un ImageField o FileField, lo excluimos
            if isinstance(field, (ImageField, FileField)):
                if field_name in data:
                    del data[field_name]

            # Si el campo es una relación (ForeignKey, OneToOneField), serializamos recursivamente
            elif isinstance(field, (ForeignKey, OneToOneField)):
                if field_name in data and data[field_name] is not None:
                    related_instance = data[field_name]
                    # Verificamos que `related_instance` sea una instancia de un modelo
                    if isinstance(related_instance, models.Model):
                        data[field_name] = self.serialize_model(related_instance)

            # Si el campo es una relación ManyToManyField
            elif isinstance(field, ManyToManyField):
                if field_name in data:
                    # En este caso, la relación ManyToMany devuelve un queryset
                    related_instances = data[field_name]
                    data[field_name] = [self.serialize_model(related_instance) for related_instance in related_instances]

        return data

    def profile_to_json(self, request):
        # Obtener el primer perfil
        profile = User_cv.objects.all()

        # Serializar el perfil
        serialized_profile = self.serialize_model(profile)

        return serialized_profile  # Retorna el diccionario, no un JsonResponse

    def get(self, request, *args, **kwargs):
        # Obtener los datos serializados del perfil
        data = self.profile_to_json(request)

        # Devolver la respuesta en formato JSON
        return JsonResponse({"response": data})  # Este es el JsonResponse final
