from django.utils import timezone
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Sum
from django.core.paginator import Paginator
from courses.models import *
from courses.forms import *
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Q

# * |--------------------------------------------------------------------------
# * | Landing Page
# * |--------------------------------------------------------------------------

def landing_page(request):
    return render(request, 'landing_page.html')

# * |--------------------------------------------------------------------------
# * | Funciones Auxiliares
# * |--------------------------------------------------------------------------

def group_required(group_name):
    """Decorator to check if a user belongs to a specific group."""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.groups.filter(name=group_name).exists():
                return render(request, 'role_management/access_denied.html', {
                'message': 'You do not have permission to access this page.',
                })
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def create_interaction_matrix():
    users = User.objects.all()
    courses = Course.objects.all()

    # Crear un DataFrame vacío con usuarios como índices y cursos como columnas
    matrix = pd.DataFrame(0, index=[user.id for user in users], columns=[course.id for course in courses])

    wishlist = WishListUser.objects.filter(type_wish__name = 'Course')
    # Llenar la matriz con datos de WishlistUser
    for wish in wishlist: 
        user_id = wish.user.id
        course_id = wish.id_wish
        if course_id in matrix.columns:
            matrix.at[user_id, course_id] = 1

    return matrix

def recommend_courses_for_user(request, interaction_matrix, user_similarity_df):
    # Obtener el ID del usuario actual
    user_id = request.user.id

    # Obtener los cursos ya valorados por el usuario actual
    already_rated = interaction_matrix.loc[user_id]
    already_rated = already_rated[already_rated > 0].index

    # Obtener las similitudes del usuario actual con otros usuarios
    similar_users = user_similarity_df[user_id]

    # Ponderar las interacciones de otros usuarios por la similitud
    weighted_scores = interaction_matrix.T.dot(similar_users)

    # Normalizar por las similitudes totales
    similarity_sums = similar_users.sum()
    recommendations = weighted_scores / similarity_sums

    # Ordenar las recomendaciones en orden descendente
    recommendations_sorted = recommendations.sort_values(ascending=False)

    # Excluir los cursos que el usuario ya ha valorado
    recommendations_sorted = recommendations_sorted.drop(already_rated, errors='ignore')

    recommended_courses = recommendations_sorted.head(2).index.tolist()

    # Devolver los dos mejores cursos recomendados
    return Course.objects.filter(id__in=recommended_courses)

@login_required
def add_userwish_view(request, course_id):
        type_wish = WishListType.objects.get(name='Course')
        
        from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import WishListUser, WishListType

@login_required
def add_userwish_view(request, course_id):
    # Obtener el tipo de lista de deseos "Course"
    type_wish = WishListType.objects.get(name='Course')
    
    # Obtener o crear el objeto de la lista de deseos
    user_wish, created = WishListUser.objects.get_or_create(user=request.user, type_wish=type_wish, id_wish=course_id)

    if not created:  # Si el objeto no fue creado, significa que ya existía en la lista de deseos
        user_wish.delete()  # Eliminar el curso de la lista de deseos

    # Después de añadir o eliminar, redirigir a la lista de cursos
    return redirect('courses:courses-list')

@login_required
def create_or_update_course_review_view(request, course_id, review_id=None):
    course = get_object_or_404(Course, id=course_id)
    # Si existe un course_id, intenta obtener el curso; de lo contrario, crea uno nuevo
    review = None

    if review_id:
        review = get_object_or_404(Review, user= request.user, course=course)
    
    # Usa el formulario de modelo (creación o actualización)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)  # Si `course` es None, creará uno nuevo
        if form.is_valid():
            review = form.save(commit=False)
            # Asociar el curso con el perfil del maestro si es creación
            if not review.id:  
                review.user = request.user
                review.course = course
            review.save()
            messages.success(request, "La review se ha guardado correctamente.")
            return redirect("courses:course-detail", course_id=course.id)  # Redirige a una página de detalles del curso
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = ReviewForm(instance=review)  # Pasa el curso al formulario

    return render(request, "review_create_update.html", {"form": form, "course": course, "review": review})


# * |--------------------------------------------------------------------------
# * | Course Views
# * |--------------------------------------------------------------------------


def courses_list_view(request):
    # Obtener todos los cursos activos
    courses = Course.objects.filter(is_active=True)

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

    interaction_matrix = create_interaction_matrix()    
    user_similarity = cosine_similarity(interaction_matrix)
    user_similarity_df = pd.DataFrame(user_similarity, index=interaction_matrix.index, columns=interaction_matrix.index)

    # Obtener las recomendaciones para el usuario actual
    recommended_courses = recommend_courses_for_user(request, interaction_matrix, user_similarity_df)



    # Pasar los datos al contexto para renderizarlos en el template
    return render(request, 'courses_list.html', {
    'page_obj': page_obj, 
    'total_courses': courses.count(),
    'recommended_courses': recommended_courses,
    
})

def course_detail_view(request, course_id):
    course = get_object_or_404(
        Course.objects.prefetch_related(
            Prefetch("modules__lessons__resources"),
            Prefetch("certificates"),
            Prefetch("reviews")
        ),
        id=course_id
    )

    # Calcular estadísticas del curso
    total_lessons = course.modules.aggregate(lesson_count=Count('lessons'))['lesson_count'] or 0
    total_resources = course.modules.aggregate(
        resource_count=Count('lessons__resources')
    )['resource_count'] or 0

    average_rating = course.reviews.aggregate(Avg('rating'))['rating__avg']
    total_duration_minutes = course.modules.aggregate(
        total_duration=Sum('lessons__duration')
    )['total_duration'] or 0

    # Formatear duración
    hours = total_duration_minutes // 60
    minutes = total_duration_minutes % 60
    formatted_duration = f"{hours} hours {minutes} minutes"

 # Crear la matriz de interacción y calcular similitudes
    interaction_matrix = create_interaction_matrix()    
    user_similarity = cosine_similarity(interaction_matrix)
    user_similarity_df = pd.DataFrame(user_similarity, index=interaction_matrix.index, columns=interaction_matrix.index)

    # Obtener las recomendaciones para el usuario actual
    recommended_courses = recommend_courses_for_user(request, interaction_matrix, user_similarity_df)
    
    courses = Course.objects.filter(is_active=True)

    for course in courses:
        # Contar los usuarios que han completado el curso
        completed_users_count = course.enrolled_users.filter(status__name="completed").count()

        # Contar las veces que el curso ha sido añadido a la wishlist
        course_wishlist_count = WishListUser.objects.filter(type_wish__name="Course", id_wish=course.id).count()

        #Contar las reviews que tiene el curso
        #course_reviews_count = Review.objects.filter(course=course).count()
        course_reviews_count = course.reviews.all().count()

        #reviews = Review.objects.filter(course=course)
        reviews = course.reviews.select_related('profile_user').all()
        if reviews.exists():
            average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

        else:
            average_rating = 0  # Si no hay calificaciones, el promedio es 0
        


    context = {
        'course': course,
        'total_lessons': total_lessons,
        'total_resources': total_resources,
        'average_rating': average_rating,
        'formatted_duration': formatted_duration,
        'recommended_courses': recommended_courses,
        'course_reviews_count': course_reviews_count,
        'average_rating': average_rating,
        'completed_users_count': completed_users_count,
        'course_wishlist_count': course_wishlist_count,
        'reviews': reviews,
    }
    return render(request, 'course_detail.html', context)

@login_required
def course_user_list_view(request):
    user_courses = CourseUser.objects.filter(user=request.user).select_related('course')

    user_courses_list = []
    for course_user in user_courses:
        total_lessons = Lesson.objects.filter(module__course=course_user.course).count()
        completed_lessons = LessonCompletion.objects.filter(course_user=course_user, finished_at__isnull=False).count()

        if total_lessons > 0:
            progress_percentage = (completed_lessons / total_lessons) * 100
        else:
            progress_percentage = 0

        user_courses_list.append({
            "course": course_user.course,
            "status": course_user.status,
            "progress": progress_percentage,
        })

    return render(request, 'user_course_list.html', {'user_courses_list': user_courses_list})

@login_required
def course_user_detail_view(request, course_id):
    course = get_object_or_404(
        Course.objects.prefetch_related(
            Prefetch("modules__lessons__resources"),
            Prefetch("certificates"),
            Prefetch("reviews")
        ),
        id=course_id
    )
    completed_lessons = LessonCompletion.objects.filter(
        course_user__user=request.user, 
        course_user__course=course,
        finished_at__isnull=False
    ).values_list('lesson_id', flat=True)

    return render(request, 'user_course_detail.html', {
        'course': course,
        'completed_lessons': set(completed_lessons),  # Convertir a conjunto para fácil verificación
    })

@login_required
@group_required('teacher')
def course_teacher_list_view(request):
    profile_teacher = getattr(request.user, 'profile_teacher', None)
    context = {
        'user_role': 'teacher',
        'profile_teacher': profile_teacher,
        'teacher_courses': profile_teacher.courses.all()
    }
    return render(request, 'teacher_course_list.html', context)

# Course: ---- Enroll User View ----
@login_required
def course_enroll_user_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Verificar si el usuario ya está inscrito
    if CourseUser.objects.filter(user=request.user, course=course).exists():
        messages.warning(request, "Ya estás inscrito en este curso.")
        return redirect("courses:course-user-detail", course_id=course.id)

    # Obtener el estado "inprogress" (asegúrate de que existe en la base de datos)
    status = get_object_or_404(Status, name="inprogress")

    # Crear la relación CourseUser
    CourseUser.objects.create(user=request.user, course=course, status=status)

    messages.success(request, "Te has inscrito exitosamente en el curso.")
    return redirect("courses:course-user-detail", course_id=course.id)

# Course: ---- Create/Update Views ----
@login_required
@group_required('teacher')
def course_create_or_update_view(request, course_id=None):
    # Si existe un course_id, intenta obtener el curso; de lo contrario, crea uno nuevo
    course = None
    if course_id:
        course = get_object_or_404(Course, id=course_id, profile_teacher=request.user.profile_teacher)
    
    # Usa el formulario de modelo (creación o actualización)
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)  # Si `course` es None, creará uno nuevo
        if form.is_valid():
            course = form.save(commit=False)
            # Asociar el curso con el perfil del maestro si es creación
            if not course.id:  
                course.profile_teacher = request.user.profile_teacher
            course.save()
            messages.success(request, "El curso se ha guardado correctamente.")
            return redirect("courses:teacher-course-detail", course_id=course.id)  # Redirige a una página de detalles del curso
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = CourseForm(instance=course)  # Pasa el curso al formulario

    return render(request, "course_create_update.html", {"form": form, "course": course})

# Course: ---- Delete View ----
@login_required
@group_required('teacher')
def course_delete_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, profile_teacher=request.user.profile_teacher)
    course.delete()
    messages.success(request, "El curso se ha eliminado correctamente.")
    return redirect('teacher_dashboard')

@login_required
@group_required('freemium')
def course_complete_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course_user = CourseUser.objects.filter(user=request.user, course=course).first()

    if not course_user:
        messages.error(request, "No estás inscrito en este curso.")
        return redirect('courses:course-detail', course_id=course_id)

    total_lessons = Lesson.objects.filter(module__course=course).count()
    completed_lessons = LessonCompletion.objects.filter(course_user=course_user, lesson__module__course=course, finished_at__isnull=False).count()

    if total_lessons == completed_lessons:
        course_user.status = Status.objects.get(name="completed")
        course_user.save()
        messages.success(request, "¡Has finalizado el curso!")
    else:
        messages.error(request, "Aún no has completado todas las lecciones de este curso.")

    return redirect('courses:course-user-detail', course_id=course_id)

# * |--------------------------------------------------------------------------
# * | Teacher_Course Views
# * |--------------------------------------------------------------------------

@login_required
@group_required("teacher")
def course_teacher_detail_view(request, course_id):
    profile_teacher = request.user.profile_teacher
    course = get_object_or_404(
        profile_teacher.courses.prefetch_related(
            Prefetch("modules__lessons__resources"),
            Prefetch("certificates"),
            Prefetch("reviews")
        ),
        id=course_id
    )

    return render(request, "teacher_course_detail.html", {"course": course})

# * |--------------------------------------------------------------------------
# * | Module - Lesson - Resource_Course Views
# * |--------------------------------------------------------------------------

@login_required
@group_required('teacher')
def module_create_or_update_view(request, course_id=None, module_id=None):
    # Obtener el curso relacionado al `course_id`
    course = get_object_or_404(Course, id=course_id, profile_teacher=request.user.profile_teacher)

    # Si se pasa un `module_id`, buscamos el módulo para actualizarlo
    module = None
    if module_id:
        module = get_object_or_404(Module, id=module_id, course=course)

    # Si es un formulario POST (creación o actualización)
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            # Si estamos creando, asociamos el módulo al curso
            module = form.save(commit=False)
            module.course = course
            module.save()

            # Mensaje de éxito
            messages.success(request, "El módulo ha sido guardado correctamente.")
            return redirect('courses:teacher-course-detail', course_id=course.id)
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        # Si es GET, creamos el formulario con el módulo actual (si lo hay)
        form = ModuleForm(instance=module)

    return render(request, 'module_create_update.html', {'form': form, 'course': course, 'module': module})

@login_required
@group_required('freemium')
def lesson_detail_view(request, course_id, module_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id, course=course)
    lesson = get_object_or_404(
        Lesson.objects.select_related('module__course').prefetch_related('resources'),
        id=lesson_id, 
        module=module
    )

    course_user = CourseUser.objects.filter(user=request.user, course=course).first()
    if not course_user:
        messages.error(request, "Debes estar inscrito en este curso para acceder a sus lecciones.")
        return redirect('courses:course-detail', course_id=course_id)

    resources = lesson.resources.all()

    # Registrar la lección como iniciada
    lesson_completion, created = LessonCompletion.objects.get_or_create(course_user=course_user, lesson=lesson)
    if created:
        lesson_completion.finished_at = timezone.now()
        lesson_completion.save()

    # Total de lecciones del curso y lecciones completadas
    total_lessons = Lesson.objects.filter(module__course=course).count()
    completed_lessons = LessonCompletion.objects.filter(
        course_user=course_user, finished_at__isnull=False
    ).count()

    # Determinar la siguiente lección no completada
    next_lesson = (
        Lesson.objects.filter(module__course=course)
        .exclude(id__in=LessonCompletion.objects.filter(course_user=course_user, finished_at__isnull=False).values_list('lesson__id', flat=True))
        .order_by('id')
        .first()
    )

    is_last_lesson = next_lesson is None and total_lessons == completed_lessons

    context = {
        'course': course,
        'module': module,
        'lesson': lesson,
        'resources': resources,
        'is_last_lesson': is_last_lesson,  
        'next_lesson': next_lesson,        
    }

    return render(request, 'lesson_detail.html', context)

@login_required
@group_required('teacher')
def lesson_create_or_update_view(request, course_id=None, module_id=None, lesson_id=None):
    # Validar que el curso existe
    course = get_object_or_404(Course, id=course_id, profile_teacher=request.user.profile_teacher)

    # Validar que el módulo pertenece al curso
    module = get_object_or_404(Module, id=module_id, course=course)

    # Si se pasa un `lesson_id`, validar que la lección pertenece al módulo
    lesson = None
    if lesson_id:
        lesson = get_object_or_404(Lesson, id=lesson_id, module=module)

    # Procesamiento del formulario
    if request.method == "POST":
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            # Si estamos creando, asociamos la lección al módulo
            lesson = form.save(commit=False)
            lesson.module = module
            lesson.save()

            # Mensaje de éxito
            messages.success(request, "La lección se ha guardado correctamente.")
            return redirect('courses:teacher-course-detail', course_id=course.id)
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        # Si es GET, presentamos el formulario
        form = LessonForm(instance=lesson)

    return render(request, 'lesson_create_update.html', {'form': form, 'course': course, 'module': module, 'lesson': lesson})

@login_required
@group_required('teacher')
def resource_course_create_or_update_view(request, course_id=None, module_id=None, lesson_id=None, resource_id=None):
    # Validar que el curso existe
    course = get_object_or_404(Course, id=course_id, profile_teacher=request.user.profile_teacher)

    # Validar que el módulo pertenece al curso
    module = get_object_or_404(Module, id=module_id, course=course)

    # Validar que la lección pertenece al módulo
    lesson = get_object_or_404(Lesson, id=lesson_id, module=module)

    # Si se pasa un `resource_id`, validar que el recurso pertenece a la lección
    resource = None
    if resource_id:
        resource = get_object_or_404(Resource, id=resource_id, lesson=lesson)

    # Procesamiento del formulario
    if request.method == "POST":
        form = ResourceCourseForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            # Si estamos creando, asociamos el recurso a la lección
            resource = form.save(commit=False)
            resource.lesson = lesson
            resource.save()

            # Mensaje de éxito
            messages.success(request, "El recurso se ha guardado correctamente.")
            return redirect('courses:teacher-course-detail', course_id=course.id)
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        # Si es GET, presentamos el formulario
        form = ResourceCourseForm(instance=resource)

    return render(request, 'resource_create_update.html', {
        'form': form, 
        'course': course, 
        'module': module, 
        'lesson': lesson, 
        'resource': resource
    })

@login_required
@group_required('teacher')
def module_delete_view(request, course_id, module_id):
    module = get_object_or_404(Module, id=module_id, course=course_id)
    module.delete()
    messages.success(request, "El módulo se ha eliminado correctamente.")
    return redirect('courses:teacher-course-detail', course_id=course_id)

@login_required
@group_required('teacher')
def lesson_delete_view(request, course_id, module_id, lesson_id):
    lesson = get_object_or_404(
        Lesson, 
        id=lesson_id, 
        module__id=module_id, 
        module__course__id=course_id
    )

    lesson.delete()
    messages.success(request, "La lección se ha eliminado correctamente.")
    return redirect('courses:teacher-course-detail', course_id=course_id)

# * |--------------------------------------------------------------------------
# * | Resource Views
# * |--------------------------------------------------------------------------

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

@login_required
@group_required('teacher')
def resource_course_delete_view(request, course_id, module_id, lesson_id, resource_id):
    resource = get_object_or_404(
        Resource, 
        id=resource_id, 
        lesson__id=lesson_id, 
        lesson__module_id=module_id, 
        lesson__module__course__id=course_id
    )
    
    resource.delete()
    messages.success(request, "El Recurso se ha eliminado correctamente.")
    return redirect('courses:teacher-course-detail', course_id=course_id)

# * |--------------------------------------------------------------------------
# * | Certificate Views
# * |--------------------------------------------------------------------------

@login_required
@group_required("teacher")
def certificate_create_or_update_view(request, course_id=None, certificate_id=None):
    course = get_object_or_404(Course, id=course_id, profile_teacher=request.user.profile_teacher)

    certificate = None
    if certificate_id:
        certificate = get_object_or_404(Certificate, id=certificate_id, course=course)

    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES, instance=certificate)
        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.course = course
            certificate.save()

            messages.success(request, "El certificado ha sido guardado correctamente.")
            return redirect('courses:teacher-course-detail', course_id=course.id)
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = CertificateForm(instance=certificate)

    return render(request, 'certificate_create_update.html', {'form': form, 'course': course, 'certificate': certificate})

@login_required
@group_required('teacher')
def certificate_delete_view(request, course_id, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id, course=course_id)
    certificate.delete()
    messages.success(request, "El Certificado se ha eliminado correctamente.")
    return redirect('courses:teacher-course-detail', course_id=course_id)

# * |--------------------------------------------------------------------------
# * | Review Views
# * |--------------------------------------------------------------------------

# Review: ---- Create/Update Views ----
def review_create_or_update(request, pk=None):
    pass
