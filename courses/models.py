from decimal import Decimal
from django.db import models
from profile_cv.models import HardSkill, Sector, Category

from django.contrib.auth.models import User


class Status(models.Model):
    name = models.CharField(max_length=15)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name    
    
class ProfileTeacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
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
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
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
    is_member = models.BooleanField(default=False)
    

    def __str__(self):
        return f'{self.module} - {self.name}'
    
class CourseUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL,null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL,null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)
    lessons = models.ForeignKey('LessonCompletion', on_delete=models.CASCADE, null=True, blank=True)
    certified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.course}'
    

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
        return f"{self.name}"

class WishListType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class WishListUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True)
    type_wish = models.ForeignKey(WishListType,on_delete=models.CASCADE)
    id_wish = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.type_wish.name}"


class LessonCompletion(models.Model):
    course_user = models.ForeignKey(CourseUser, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.course_user.user.username} - {self.lesson.name}"

