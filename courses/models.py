from decimal import Decimal
from django.db import models
from profile_cv.models import HardSkill, Sector, Category

from django.contrib.auth.models import User


class Status(models.Model):
    name = models.CharField(max_length=15)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.status
    
class ProfileTeacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='teachers_images/', null=True, blank=True)
    hardskills = models.ForeignKey(HardSkill, on_delete=models.SET_NULL, null=True, blank=True)
    categoriy = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}'

    
class Course(models.Model):
    profile_teacher = models.ForeignKey(ProfileTeacher, on_delete=models.CASCADE, null=True, related_name='teacher')
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_member = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    image = models.ImageField(upload_to='courses_images/', null=True, blank=True)
    is_free = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return self.title
    
class Certificate(models.Model):

    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    ext_certificate = models.FileField(blank=True, null=True)
    

    def __str__(self):
        return f'{self.name} - {self.code}'
    
class Review(models.Model):
    rating = models.PositiveIntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    comment = models.TextField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    resource = models.ForeignKey('Resource', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.rating} - {self.comment[:50]}...'



class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    

    def __str__(self):
        return self.title

class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.module} - {self.name}'
    
class CourseUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL,null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL,null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)
    current_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True)
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.course}'
    
    def calculate_progress(self):
        # Total de lecciones del curso a través de los módulos
        total_lessons = self.course.module_set.all().prefetch_related('lesson_set').count()
        # Si el curso no tiene lecciones, el progreso es 0
        if total_lessons == 0:
            return 0.0
        # Contamos las lecciones completadas por el usuario
        completed_lessons = self.user.lesson_set.filter(module__course=self.course, completed=True).count()
        # Calculamos el progreso
        progress = (completed_lessons / total_lessons) * 100
        return round(progress, 2)
    
    def save(self, *args, **kwargs):
        # Sobrescribimos el campo progress_percentage con el valor calculado
        self.progress_percentage = self.calculate_progress()
        super().save(*args, **kwargs)  # Llamamos al save original para guardar la instancia


class Resource(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='lesson', blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, unique=True)
    downloadable = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    image = models.ImageField(blank=True, null=True, upload_to='resources_images/')
    link = models.CharField(max_length=50, blank=True, null=True)
    document = models.FileField(blank=True, null=True)
    is_active = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.name} - {self.user.username}"

class WishlistType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class WishlistUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    type_wish = models.ForeignKey(WishlistType,on_delete=models.CASCADE)
    id_wish = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.type_wish.name}"


