from django.urls import path,include
from .views import home, profile, RegisterView, guest_home
handler404 = 'your_app.views.custom_404_view'

urlpatterns = [
    path('', home, name='users-home'),
    
    path('guest_home/', guest_home, name='guest-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
]
