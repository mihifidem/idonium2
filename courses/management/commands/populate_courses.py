import random
import datetime
import os
from decimal import Decimal
from faker import Faker
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from courses.models import (
    User, ProfileTeacher, Course, Module, Lesson, Resource, CourseUser, Status, WishListType, WishListUser, LessonCompletion
)

faker = Faker()
COURSES_IMAGE_DIR = "courses_images"
TEACHERS_IMAGE_DIR = "teachers_images"
RESOURCES_IMAGE_DIR = "resources_images"

class Command(BaseCommand):
    help = "Populate the database with fake data"

    def handle(self, *args, **kwargs):
        Group.objects.create(name='teacher')
        Group.objects.create(name='headhunter')
        Group.objects.create(name='freemium')
        Status.objects.create(name='completed', description='Completed')
        Status.objects.create(name='inprogress', description='In Progress')
        WishListType.objects.create(name="Course")
        WishListType.objects.create(name="Resource")
        self.create_users()
        self.create_teachers()
        self.create_courses()
        self.create_modules_and_lessons()
        self.create_resources()
        self.create_course_users()
        self.create_wishlist()
        self.create_lesson_completions()

    def create_users(self):
        for _ in range(10):  # Cambia este número según cuántos usuarios quieras crear
            User.objects.create_user(
                username=faker.user_name(),
                email=faker.email(),
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                password="password123"
            )

    def create_teachers(self):
        users = User.objects.all()
        for user in users:
            profile_teacher, created = ProfileTeacher.objects.get_or_create(user=user)
            if created:
                profile_teacher.image = self.get_random_image(TEACHERS_IMAGE_DIR)
                profile_teacher.hardskills = None
                profile_teacher.category = None
                profile_teacher.sector = None
                profile_teacher.save()

    def create_courses(self):
        teachers = ProfileTeacher.objects.all()
        for teacher in teachers:
            for _ in range(2):  # Cada profesor tiene 2 cursos
                course = Course.objects.create(
                    profile_teacher=teacher,
                    title=faker.unique.sentence(nb_words=4),
                    description=faker.paragraph(),
                    image=self.get_random_image(COURSES_IMAGE_DIR) or "default.jpg",  # Imagen por defecto
                    is_member=random.choice([True, False]),
                    is_active=True,
                    is_free=random.choice([True, False]),
                    price=Decimal(random.uniform(10, 100)).quantize(Decimal("0.00")),
                )
                # Validar atributos obligatorios
                assert course.profile_teacher, "El curso debe tener un profesor asignado"

    def create_modules_and_lessons(self):
        courses = Course.objects.all()
        for course in courses:
            for _ in range(3):  # Cada curso tiene 3 módulos
                module = Module.objects.create(
                    course=course,
                    title=faker.unique.sentence(nb_words=3),
                    description=faker.text(),
                    is_active=True
                )
                for _ in range(5):  # Cada módulo tiene 5 lecciones
                    Lesson.objects.create(
                        module=module,
                        name=faker.unique.sentence(nb_words=2),
                        description=faker.text(),
                        is_member=course.is_member
                    )

    def create_resources(self):
        lessons = Lesson.objects.all()
        for lesson in lessons:
            for _ in range(2):  # Cada lección tiene 2 recursos
                Resource.objects.create(
                    lesson=lesson,
                    name=faker.unique.word(),
                    downloadable=random.choice([True, False]),
                    is_member=lesson.is_member,
                    url=faker.url(),
                    image=self.get_random_image(RESOURCES_IMAGE_DIR),
                    document=None,
                    is_active=True,
                    is_free=random.choice([True, False]),
                    price=Decimal(random.uniform(10, 100)).quantize(Decimal("0.00")),
                )

    def create_course_users(self):
        users = User.objects.all()
        courses = Course.objects.all()
        statuses = Status.objects.all()
        for course in courses:
            for user in random.sample(list(users), 3):  # Cambia a 3 o más usuarios por curso
                CourseUser.objects.create(
                    user=user,
                    course=course,
                    status=random.choice(statuses),
                    start_date=faker.date_time_this_year(),
                    end_date=None,
                    certified=False
                )

    def create_wishlist(self):
        users = User.objects.all()
        wishlisttype = WishListType.objects.all()
        for user in users:
            WishListUser.objects.create(
                user=user,
                type_wish=random.choice(wishlisttype),
                id_wish=random.randint(1, 100)
            )

    def create_lesson_completions(self):
        course_users = CourseUser.objects.all()
        lessons = Lesson.objects.all()
        for course_user in course_users:
            for lesson in lessons:
                LessonCompletion.objects.create(
                    course_user=course_user,
                    lesson=lesson,
                    started_at=faker.date_time_this_year(),
                    finished_at=None
                )

    def get_random_image(self, image_dir):
        """Return a random image file path relative to MEDIA_URL with correct slashes."""
        # Obtener la ruta absoluta utilizando MEDIA_ROOT
        absolute_image_dir = os.path.join(settings.MEDIA_ROOT, image_dir)

        # Verifica que el directorio existe
        if not os.path.exists(absolute_image_dir):
            return None  # Retorna None si no se encuentra el directorio

        # Listar todos los archivos en el directorio
        image_files = [f for f in os.listdir(absolute_image_dir) if os.path.isfile(os.path.join(absolute_image_dir, f))]

        if not image_files:
            return None  # Retorna None si no hay imágenes en el directorio

        # Selecciona una imagen aleatoria
        selected_image = random.choice(image_files)

        # Retorna la ruta relativa con barras normales
        image_path = os.path.join(image_dir, selected_image)

        # Reemplaza las barras invertidas con barras normales (para compatibilidad con Django)
        return image_path.replace("\\", "/")
