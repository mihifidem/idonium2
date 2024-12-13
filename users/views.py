from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from blog.models import Post
from courses.models import Course
from gaming.models import DuckyCoin
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm

from django.contrib.auth import logout
from django.shortcuts import redirect
from .menus import MENU_ITEMS
from django.urls import reverse


def dynamic_menu_view(request):
    user_role = request.user.groups.first().name if request.user.groups.exists() else None
    menu = MENU_ITEMS.get(user_role, MENU_ITEMS['guest'])
    return render(request, 'users/home.html', {'menu': menu})


# def profilecv_menu_view(request):
#     user_groups = request.user.groups.all()
    
#     # Verifica el grupo del usuario
#     user_role = None
#     if user_groups.exists():
#         user_role = user_groups[0].name  # Obtén el nombre del primer grupo asociado al usuario
#     context = {}  # Inicializa el contexto

#     if user_role == 'premium':
#         menu = MENU_ITEMS['premium']

#     context = {
#         'menu': menu,
#     }
#     return render(request, 'role_management/subitem_profilecv.html', context)

def custom_logout(request):
    logout(request)
    return redirect('users:users-home')  # Redirige al home o cualquier otra página.


# def custom_404_view(request, exception):
#     return render(request, 'users/404.html', status=404)
def pre_404_view(request):
    # Lógica personalizada antes del 404
    context = {
        'message': '¡Algo salió mal!',
        'suggestions': ['Inicio', 'Contáctanos', 'Buscar otra página'],
    }
    return render(request, 'users/404.html', context, status=404)


def custom_404_view(request, exception=None):
    menu = MENU_ITEMS.get('guest', [])  # Mostrar menú de invitados
    context = {
        'message': '¡Algo salió mal!',
        'suggestions': ['Inicio', 'Contáctanos', 'Buscar otra página'],
        'menu': menu,
    }
    return render(request, 'users/404.html', context, status=404)

def guest_home(request):
    user_groups = request.user.groups.all()
    user_role = user_groups[0].name if user_groups.exists() else None
    # menu = MENU_ITEMS.get(user_role, MENU_ITEMS['guest'])
    menu = MENU_ITEMS['guest']
    print(menu)
    latest_post = Post.objects.filter(status=1).order_by('-created_on').first()
    posts3MaxLike = Post.objects.filter(status=1).order_by('-likes')[:3]
    courses = Course.objects.all()

    user_duckycoins = getattr(request.user.duckycoins, 'balance', 0) if request.user.is_authenticated else None

    current_path = request.path  # Captura la URL actual
    return render(request, 'users/home.html', {
        'latest_post': latest_post,
        'posts3MaxLike': posts3MaxLike,
        'courses': courses,
        'user_duckycoins': user_duckycoins,
        'menu_items': menu,
        'current_path': current_path,  # Pasa la URL actual al contexto
    })

def home(request):
    user_groups = request.user.groups.all()
    user_role = user_groups[0].name if user_groups.exists() else None
    menu = MENU_ITEMS.get(user_role, MENU_ITEMS['guest'])

    latest_post = Post.objects.filter(status=1).order_by('-created_on').first()
    posts3MaxLike = Post.objects.filter(status=1).order_by('-likes')[:3]
    courses = Course.objects.all()

    user_duckycoins = getattr(request.user.duckycoins, 'balance', 0) if request.user.is_authenticated else None

    current_path = request.path  # Captura la URL actual
    return render(request, 'users/home.html', {
        'latest_post': latest_post,
        'posts3MaxLike': posts3MaxLike,
        'courses': courses,
        'user_duckycoins': user_duckycoins,
        'menu': menu,
        'current_path': current_path,  # Pasa la URL actual al contexto
    })

    


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})
