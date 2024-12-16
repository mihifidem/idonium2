from django.urls import path
from .views import home, profile, RegisterView,  backToHome
from django.views.generic import TemplateView

app_name = 'users'  # Este es el espacio de nombres requerido


urlpatterns = [
    path('', home, name='users-home'),
    
    # path('guest_home/', guest_home, name='guest-home'),
    path('register/', RegisterView.as_view(), name='users-register'),

    path('profile/', profile, name='users-profile'),
    path('back_to_home/', backToHome, name='back_to_home'),

]

