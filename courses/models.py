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
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='teachers_images/', null=True, blank=True)
    hardskills = models.ForeignKey(HardSkill, on_delete=models.SET_NULL, null=True, blank=True)
    categoriy = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}'

    
class Course(models.Model):
    profile_teacher = models.ForeignKey(ProfileTeacher, on_delete=models.CASCADE, related_name='teacher')
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    is_member = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    image = models.ImageField(upload_to='courses_images/', null=True, blank=True)
    is_free = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    catergory = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, blank=True, null=True, on_delete=models.CASCADE)
    hardskills = models.ManyToManyField(HardSkill)


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
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    resource = models.ForeignKey('Resource', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # Garantiza que una Review solo pueda estar vinculada a un curso o a un recurso
            models.CheckConstraint(
                check=(
                    models.Q(course__isnull=False, resource__isnull=True) |
                    models.Q(course__isnull=True, resource__isnull=False)
                ),
                name='review_course_or_resource_not_both'
            ),
            # Asegura que un usuario pueda dejar solo una review por curso
            models.UniqueConstraint(
                fields=['user', 'course'],
                name='unique_user_course_review'
            ),
            # Asegura que un usuario pueda dejar solo una review por recurso
            models.UniqueConstraint(
                fields=['user', 'resource'],
                name='unique_user_resource_review'
            )
        ]

    def __str__(self):
        if self.course:
            return f'{self.user.username} - Course: {self.course.title}'
        elif self.resource:
            return f'{self.user.username} - Resource: {self.resource.name}'
        else:
            return f'{self.user.username} - Unlinked Review'


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    is_member = models.BooleanField(default=False)
    duration = models.IntegerField(null=True, blank=True, default=10)
    

    def __str__(self):
        return f'{self.module} - {self.name}'
    
class CourseUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL,null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL,null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
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
    is_free = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

class WishListType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class WishListUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type_wish = models.ForeignKey(WishListType, on_delete=models.CASCADE)
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
    



