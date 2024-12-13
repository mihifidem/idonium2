from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse  # Importa reverse para usarlo con nombres de ruta



@login_required
def premium_chat(request):
    # Verifica que el usuario tenga el rol de "teacher"
    user_groups = request.user.groups.all()
    if not user_groups.filter(name="premium").exists():
        # Si el usuario no es un "premium", redirige o muestra un mensaje de error
        return render(request, 'role_management/access_denied.html', {
            'message': 'You do not have permission to access this page.',
        })
    
    # Define el contexto para la vista
    context = {
        'user_role': 'premium',
        'teacher_profile': getattr(request.user, 'profile_user', None),
        # Agrega aquí más datos relacionados con el rol de "teacher"
    }
    return render(request, 'role_management/premium_chat.html', context)


@login_required
def premium_dashboard(request):
    # Verifica que el usuario tenga el rol de "teacher"
    user_groups = request.user.groups.all()
    if not user_groups.filter(name="premium").exists():
        # Si el usuario no es un "premium", redirige o muestra un mensaje de error
        return render(request, 'role_management/access_denied.html', {
            'message': 'You do not have permission to access this page.',
        })
    
    # Define el contexto para la vista
    context = {
        'user_role': 'premium',
        'user_profile': getattr(request.user, 'profile_user', None),
        # Agrega aquí más datos relacionados con el rol de "teacher"
    }
    return render(request, 'role_management/base.html', context)

