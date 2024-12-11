from django.contrib import admin

from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users.views import custom_logout,CustomLoginView, ResetPasswordView, ChangePasswordView

from users.forms import LoginForm
from test_management.views import chatbot_response

# from django.contrib.sitemaps.views import sitemap
import debug_toolbar
from django.conf.urls import handler404
#from users.views import custom_404_view

#handler404 = 'users.views.custom_404_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('chatbot/', include('test_management.urls')),

    path('', include('users.urls')),

    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='users/login.html',
                                           authentication_form=LoginForm), name='login'),

#     path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
     path('logout/', custom_logout, name='logout'),

    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    path('password-change/', ChangePasswordView.as_view(), name='password_change'),

    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
    path('quiz/', include('test_management.urls')),


    path("blog/", include("blog.urls"), name="blog-urls"),
    path("summernote/", include("django_summernote.urls")),
    path('__debug__/', include(debug_toolbar.urls)),
#     path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
