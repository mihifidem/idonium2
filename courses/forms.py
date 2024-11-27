from django import forms
from django.contrib.auth.models import *
from .models import *

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'profile_teacher']

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'lesson', '']

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['course', 'date_issued']
        
class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['course', 'title', 'description']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['module', 'name', 'description']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
