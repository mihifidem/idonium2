from django import forms
from django.contrib.auth.models import *
from .models import *

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ResourceCourseForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'image', 'link', 'document']

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'image', 'link', 'document', 'price']

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['name', 'code', 'ext_certificate']
        
class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description', 'is_active']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['name', 'description', 'duration']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
