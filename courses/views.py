from django.db.models import Count, Avg
from urllib import request
from django import forms
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models import Prefetch

from courses.models import *
from courses.forms import *
from profile_cv.models import Profile_CV

# Landing page ------------------------------------------------------------------------------

def landing_page(request):
    return render(request, 'landing_page.html')

# Funciones Auxiliares ----------------------------------------------------------------

def group_required(group_name):
    """Decorator to check if a user belongs to a specific group."""
    def check_group(user):
        return user.is_authenticated and user.groups.filter(name=group_name).exists()
    return user_passes_test(check_group)

# List Views ----------------------------------------------------------------------------------

def courses_list_view(request):
    # Obtener todos los cursos activos
    courses = Course.objects.filter(is_active=True)
    # Obtener el tipo de wishlist para cursos
    course_type = WishListType.objects.get(name="Course")

    completed_status = Status.objects.get(name="completed") 
    
     # Asegúrate de que el estado 'completado' sea correcto

    completed_courses = []
    for course in courses:
        # Contar los usuarios que han completado el curso
        completed_users_count = CourseUser.objects.filter(course=course, status=completed_status).count()

        # Contar las veces que el curso ha sido añadido a la wishlist
        course_wishlist_count = WishListUser.objects.filter(type_wish=course_type, id_wish=course.id).count()

        #Contar las reviews que tiene el curso
        course_reviews_count = Review.objects.filter(course=course).count()

        reviews = Review.objects.filter(course=course)
        if reviews.exists():
            average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            
        else:
            average_rating = 0  # Si no hay calificaciones, el promedio es 0

        # Agregar el curso y los resultados de los contadores a la lista
        completed_courses.append({
            'course': course,
            'completed_users_count': completed_users_count,
            'course_wishlist_count': course_wishlist_count,
            'course_reviews_count': course_reviews_count,
            'average_rating': round(average_rating, 1)
        })

    # Pasar los datos al contexto para renderizarlos en el template
    return render(request, 'courses_list.html', {'completed_courses': completed_courses})

def resources_list_view(request):
    resources = Resource.objects.filter(is_active=True, downloadable=True)
    resource_type = WishListType.objects.get(name="Resource")

    resources_list = []
    for resource in resources:
        resource_wishlist_count = WishListUser.objects.filter(type_wish=resource_type, id_wish=resource.pk).count()
        resource_reviews_count = Review.objects.filter(resource=resource).count()

        reviews = Review.objects.filter(resource=resource)
        if reviews.exists():
            average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        else:
            average_rating = 0

        resources_list.append({
            "resource": resource,
            "resource_wishlist_count": resource_wishlist_count,
            "resource_reviews_count": resource_reviews_count,
            "average_rating": round(average_rating, 1)
        })
        
    return render(request, 'resources_list.html', {'resources_list': resources_list})

# TeacherViews ----------------------------------------------------------------
@login_required
@group_required('teacher')
def course_create_or_update_view(request, pk=None):
    
    if pk:
        course = get_object_or_404(Course, pk=pk)

    else:
        pk = None

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course-detail')
        else:
            form = CourseForm(instance=course)
            return render(request, 'course_form.html', {'form': form})

@login_required
@group_required('teacher')
def resource_create_or_update_view(request, pk=None):
    if pk:
        resource = get_object_or_404(Resource, pk=pk)
    else:
        resource = None
    
    if request.method == 'POST':
        form = ResourceForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            return redirect('resource-list', pk=resource.pk)
        else:
            form = ResourceForm(instance=resource)
            return render(request, 'resource_form.html', {'form': form})
        
# def profileteacher_list_view(request):
#     teacher_group = Group.objects.get(name = 'teachers')
#     teacher = User.objects.filter(groups=teacher_group)
#     profile_teacher = ProfileTeacher.objects.filter(user = teacher)
#     return render(request, 'profile_teacher_list.html', {'teachers': teacher})

# VISTA CON TODA LA INFORMACIÓN PARA EL HOME DE OSCAR!!!!!!!!!!!
def course_detail_view(request, pk):
    # Obtener el curso
    course = get_object_or_404(Course, pk=pk)
    
    # Obtener el perfil del profesor
    profile_teacher = get_object_or_404(ProfileTeacher, pk=course.pk)
    
    # Obtener las reseñas del curso
    reviews = Review.objects.filter(course=course)
    
    # Contar las reseñas y calcular la puntuación promedio
    course_reviews_count = reviews.count()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    # Obtener los módulos del curso y prefetch lecciones
    modules = Module.objects.filter(course=course).prefetch_related(
        Prefetch('lesson_set', queryset=Lesson.objects.all())
    )

    reviews_with_profiles = []
    for review in reviews:
        try:
            profile = review.user.profile_cv  # Intentamos acceder al Profile_CV del usuario
            user_image = profile.image.url if profile.image else None  # Verificamos si tiene imagen
        except Profile_CV.DoesNotExist:  # Si no tiene un Profile_CV asociado
            user_image = None  # Establecemos la imagen en None o en una imagen por defecto

        reviews_with_profiles.append({
            'review': review,
            'user_image': user_image
        })

    return render(
        request,
        'course-detail.html',
        {
            'course_info': course,
            'profile_teacher': profile_teacher,
            'course_reviews_count': course_reviews_count,
            'average_rating': average_rating,
            'reviews_with_profiles': reviews_with_profiles,  # Pasamos las reseñas con imágenes a la plantilla
            'modules': modules,
        }
    )


def certificate_create_or_update_view(request, pk=None):
    
    if pk:
        certificate = get_object_or_404(Certificate, pk=pk)
    else:
        pk = None
    
    if request.method == 'POST':
        form = CertificateForm(request.POST, instance=certificate)
        if form.is_valid():
            form.save()
            return redirect('certificate-detail', pk=certificate.pk)
        else:
            form = CertificateForm(instance=certificate)
            return render(request, 'certificate_form.html', {'form': form})
        
def module_create_or_update_view(request, pk=None):
    
    if pk:
        module = get_object_or_404(Module, pk=pk)
    else: 
        pk = None
    
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect('course-detail', pk=module.pk)
        else:
            form = ModuleForm(instance=module)
            return render(request, 'module_form.html', {'form': form})
    

def lesson_create_or_update_view(request, pk=None):
    resources = Resource.objects.all()
    if pk:
        lesson = get_object_or_404(Lesson, pk=pk)
    else: 
        pk = None
    
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('lesson-detail', pk=lesson.pk)
        else:
            form = LessonForm(instance=lesson)
            return render(request, 'lesson_form.html', {'form': form})
        

def review_create_or_update(request, pk=None):
    if pk:
        review = get_object_or_404(Review, pk=pk)
    else:
        pk = None
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('review-detail', pk=review.pk)
        else:
            form = ReviewForm(instance=review)
            return render(request, 'course_review_form.html', {'form': form})
        


   