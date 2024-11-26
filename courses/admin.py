from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ProfileTeacher)
admin.site.register(Course)
admin.site.register(Status)
admin.site.register(UserCourse)
admin.site.register(Certificate)
admin.site.register(UserCertification)
admin.site.register(Review)
# admin.site.register(Category)
# admin.site.register(Sector)
admin.site.register(Lesson)
admin.site.register(Module)
admin.site.register(Resource)

