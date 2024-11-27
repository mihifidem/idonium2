from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ProfileTeacher)
admin.site.register(Course)
admin.site.register(Status)
<<<<<<< HEAD
admin.site.register(CourseUser)
admin.site.register(Certificate)
# admin.site.register(UserCertification)
=======
admin.site.register(UserCourse)
admin.site.register(Certificate)
admin.site.register(UserCertification)
>>>>>>> a6d56fa2fe3c147789943413c56471ebbf6e0a58
admin.site.register(Review)
# admin.site.register(Category)
# admin.site.register(Sector)
admin.site.register(Lesson)
admin.site.register(Module)
admin.site.register(Resource)

