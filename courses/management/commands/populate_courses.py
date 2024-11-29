import random
from decimal import Decimal
from faker import Faker
import datetime
from django.core.management.base import BaseCommand
from courses.models import (  # Cambia `courses` por el nombre de tu aplicación
    User, ProfileTeacher, Course, Module, Lesson, Resource, CourseUser, Status, WishlistType, WishlistUser, LessonCompletion
)

faker = Faker()

class Command(BaseCommand):
    help = "Populate the database with fake data"

    def handle(self, *args, **kwargs):
        Status.objects.create(name='completed', description='Completed')
        self.create_users()
        self.create_teachers()
        self.create_status()
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
                profile_teacher.image = None  # Puedes asignar valores predeterminados
                profile_teacher.hardskills = None
                profile_teacher.categoriy = None
                profile_teacher.sector = None
                profile_teacher.save()

    def create_status(self):
        for _ in range(3):  # Ejemplo de 3 estados
            Status.objects.create(
                name=faker.word(),
                description=faker.sentence()
            )

    def create_courses(self):
        teachers = ProfileTeacher.objects.all()
        for teacher in teachers:
            for _ in range(2):  # Cada profesor tiene 2 cursos
                Course.objects.create(
                    profile_teacher=teacher,
                    title=faker.unique.sentence(nb_words=4),
                    description=faker.paragraph(),
                    is_member=random.choice([True, False]),
                    is_active=True,
                    image=None,
                    is_free=random.choice([True, False]),
                    price=Decimal(random.uniform(10, 100)).quantize(Decimal("0.00")),
                )

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
                    image=None,
                    link=faker.url(),
                    document=None,
                    is_active=True
                )

    def create_course_users(self):
        users = User.objects.all()
        courses = Course.objects.all()
        statuses = Status.objects.all()
        for user in users:
            for course in random.sample(list(courses), 2):  # Cada usuario se inscribe en 2 cursos
                CourseUser.objects.create(
                    user=user,
                    course=course,
                    status=random.choice(statuses),
                    start_date=faker.date_time_this_year(),
                    end_date=None,
                    current_lesson=None,  # Agregado si necesitas este campo
                    progress_percentage=Decimal(random.uniform(0, 100)).quantize(Decimal("0.00")),  # Agregado si necesitas este campo
                    certified=False
                )

    def create_wishlist(self):
        users = User.objects.all()
        for user in users:
            WishlistUser.objects.create(
                user=user,
                type_wish=WishlistType.objects.create(name=faker.word()),
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
