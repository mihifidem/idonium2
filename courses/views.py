from urllib import request
from django import forms
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from courses.models import *
from courses.forms import *

# Landing page ------------------------------------------------------------------------------

def landing_page(request):
    return render(request, 'landing_page.html')

# List Views ----------------------------------------------------------------------------------

def courses_list_view(request):
    course = Course.objects.filter(is_active = True)
    return render(request, 'course_list.html', {'courses': course})

def profileteacher_list_view(request):
    teacher = ProfileTeacher.objects.all()
    return render(request, 'profile_teacher_list.html', {'teachers': teacher})

def resource_list_view(request):
    resource = Resource.objects.all()
    return render(request, 'resource_list.html', {'resources': resource})

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

# VISTA CON TODA LA INFORMACIÓN PARA EL HOME DE OSCAR!!!!!!!!!!!
def course_detail_view(request, pk):
    course = Course.objects.get(pk=pk)
    module = Module.objects.get(pk=course.pk)
    lesson = Lesson.objects.get(pk=module.pk)
    teacher = ProfileTeacher.objects.get(pk=course.pk)
    resource = Resource.objects.get(pk=lesson.pk)

    return render(request, 'course_detail.html', {'course': course,'module': module, 'lesson': lesson, 'teacher': teacher,'resource': resource})

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


    