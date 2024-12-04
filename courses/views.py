from django.db.models import Count, Avg
from urllib import request
from django import forms
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models import Prefetch, Sum
from django.core.paginator import Paginator
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

    completed_courses = []
    for course in courses:
        # Contar los usuarios que han completado el curso
        completed_users_count = course.enrolled_users.filter(status__name="completed").count()

        # Contar las veces que el curso ha sido añadido a la wishlist
        course_wishlist_count = WishListUser.objects.filter(type_wish__name="Course", id_wish=course.pk).count()

        #Contar las reviews que tiene el curso
        #course_reviews_count = Review.objects.filter(course=course).count()
        course_reviews_count = course.reviews.all().count()

        #reviews = Review.objects.filter(course=course)
        reviews = course.reviews.all()
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

    paginator = Paginator(completed_courses, 9)
    page_number = request.GET.get('page')  # Obtén el número de página actual
    page_obj = paginator.get_page(page_number)
    

    # Pasar los datos al contexto para renderizarlos en el template
    return render(request, 'courses_list.html', {'page_obj': page_obj, 'total_courses': courses.count()})
    

def resources_list_view(request):
    resources = Resource.objects.filter(is_active=True, downloadable=True, lesson=None)
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
    
    # Obtener las reseñas del curso
    reviews = Review.objects.filter(course=course)
    
    # Contar las reseñas y calcular la puntuación promedio
    course_reviews_count = reviews.count()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    # Obtener los módulos del curso y prefetch lecciones
    modules = Module.objects.filter(course=course).prefetch_related(
        Prefetch('lessons', queryset=Lesson.objects.all()))
    
    total_lessons_count = Lesson.objects.filter(module__course=course).count()

    total_duration_minutes = Lesson.objects.filter(module__course=course).aggregate(Sum('duration'))['duration__sum'] or 0

    # Convertir la duración total a horas y minutos
    hours = total_duration_minutes // 60
    minutes = total_duration_minutes % 60
    formatted_duration = f"{hours} hours {minutes} minutes"
    
    total_resources_count = Resource.objects.filter(lesson__module__course=course).count()
    total_users_count = CourseUser.objects.filter(course=course, status__name="active").count()
    

    
    
#     completed_courses = CourseUser.objects.filter(status__name='completed').values('course') \
#     .annotate(num_completions=Count('course')) \
#     .order_by('-num_completions')

# # Verificar si hay resultados
#     if completed_courses.exists():
#         # Obtener el primer curso más completado
#         most_completed_course = completed_courses[0]
#         course_id = most_completed_course['course']
#         completions = most_completed_course['num_completions']
#         # Obtener el curso correspondiente usando el ID del curso
#         course_most_completed = Course.objects.get(pk=course_id)
#     else:
#         # Si no hay cursos completados, asignar valores predeterminados
#         course_most_completed = None
#         completions = 0

#     # Si se ha encontrado un curso más completado, obtener las estadísticas correspondientes
#     if course_most_completed:
#         total_reviews_most_completed = Review.objects.filter(course=course_most_completed).count()
#         average_rating_most_completed = Review.objects.filter(course=course_most_completed).aggregate(Avg('rating'))['rating__avg'] or 0
#         total_wished_most_completed = WishListUser.objects.filter(id_wish=course_most_completed.pk).count()
#     else:
#         total_reviews_most_completed = 0
#         average_rating_most_completed = 0
#         total_wished_most_completed = 0


#     wishlist_courses = WishListUser.objects.filter(type_wish__name="Course") \
#         .values('id_wish') \
#         .annotate(num_wishlist=Count('id_wish')) \
#         .order_by('-num_wishlist')

#     if wishlist_courses.exists():  # Verificar si hay resultados
#         # Obtener el id_wish (id del curso más deseado)
#         most_wished_course = wishlist_courses.first()  # El curso con más wishlist
#         course_id_wishlist = most_wished_course['id_wish']  # El curso con más wishlist
#         wishlist_count = most_wished_course['num_wishlist']  # Cuántos usuarios lo tienen en wishlist
        
#         # Obtener el objeto de curso más deseado
#         course_most_wished = Course.objects.get(pk=course_id_wishlist)
#     else:
#         course_most_wished = None
#         wishlist_count = 0

#     # Obtener el número total de reseñas, puntuación promedio y elementos en la wishlist para el curso más añadido a wishlist
#     if course_most_wished:
#         total_reviews_most_wished = Review.objects.filter(course=course_most_wished).count()
#         average_rating_most_wished = Review.objects.filter(course=course_most_wished).aggregate(Avg('rating'))['rating__avg'] or 0
#         total_wishlist_most_wished = WishListUser.objects.filter(id_wish=course_most_wished.pk).count()
#     else:
#         total_reviews_most_wished = 0
#         average_rating_most_wished = 0
#         total_wishlist_most_wished = 0

    modules_with_index = []
    for module_index, module in enumerate(modules, start=1):  # Índice de módulo comienza en 1
        # Agregamos un atributo "module_index" al módulo
        module.module_index = module_index
        
        # Añadimos índices para las lecciones del módulo
        lessons_with_indices = []
        for lesson_index, lesson in enumerate(module.lessons.all(), start=1):  # Índice de lección comienza en 1
            # Agregamos un atributo "lesson_index" a cada lección
            lesson.lesson_index = lesson_index
            lessons_with_indices.append(lesson)

        # Reemplazamos la relación con la lista de lecciones indexadas
        module.lesson_set_indexed = lessons_with_indices
        modules_with_index.append(module)

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
        'course_detail.html',
        {
            'course_info': course,
            'course_reviews_count': course_reviews_count,
            'average_rating': average_rating,
            'reviews_with_profiles': reviews_with_profiles,  # Pasamos las reseñas con imágenes a la plantilla
            'modules_with_index': modules_with_index,
            'total_lessons_count': total_lessons_count,
            'formatted_duration': formatted_duration,
            'total_resources_count': total_resources_count,
            'total_users_count': total_users_count,
            # 'course_most_completed': course_most_completed,
            # 'completions': completions,
            # 'total_reviews_most_completed': total_reviews_most_completed,
            # 'average_rating_most_completed': average_rating_most_completed,
            # 'total_wished_most_completed': total_wished_most_completed,
            # 'course_most_wished': course_most_wished,
            # 'total_reviews_most_wished': total_reviews_most_wished,
            # 'average_rating_most_wished': average_rating_most_wished,
            # 'total_wished_most_completed': total_wishlist_most_wished,
            # 'wishlist_count': wishlist_count

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
        


   