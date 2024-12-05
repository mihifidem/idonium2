from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # Obtén los grupos del usuario
    user_groups = request.user.groups.all()
    
    # Verifica el grupo del usuario
    user_role = None
    if user_groups.exists():
        user_role = user_groups[0].name  # Obtén el nombre del primer grupo asociado al usuario
    
    context = {}  # Inicializa el contexto

    if user_role == 'member1':
        context = {
            'user_role': user_role,
            'profile_user': getattr(request.user, 'profile_user', None),
        }
        return render(request, 'role_management/dashboard_member.html', context)

    elif user_role == 'teacher':
        context = {
            'user_role': user_role,
            'profile_teacher': getattr(request.user, 'profile_teacher', None),
        }
        return render(request, 'role_management/dashboard_teacher.html', context)

    elif user_role == 'headhunter':
        context = {
            'user_role': user_role,
            'profile_headhunter': getattr(request.user, 'profile_headhunter', None),
        }
        return render(request, 'role_management/dashboard_headhunter.html', context)

    else:
        # Maneja el caso en que no tenga un grupo o no sea reconocido
        context = {
            'user_role': 'unknown',
            'message': 'Role not recognized or user not logged in.',
        }
        return render(request, 'role_management/dashboard_default.html', context)

@login_required
def teacher_dashboard(request):
    # Verifica que el usuario tenga el rol de "teacher"
    user_groups = request.user.groups.all()
    if not user_groups.filter(name="teacher").exists():
        # Si el usuario no es un "teacher", redirige o muestra un mensaje de error
        return render(request, 'role_management/access_denied.html', {
            'message': 'You do not have permission to access this page.',
        })
    
    # Define el contexto para la vista
    context = {
        'user_role': 'teacher',
        'teacher_profile': getattr(request.user, 'profile_teacher', None),
        # Agrega aquí más datos relacionados con el rol de "teacher"
    }
    return render(request, 'role_management/dashboard_teacher.html', context)