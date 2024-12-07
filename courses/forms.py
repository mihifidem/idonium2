from django import forms
from django.contrib.auth.models import *
from .models import *

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'lesson']

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['course', 'name', 'code']
        
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
