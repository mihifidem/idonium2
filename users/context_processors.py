# context_processors.py
from .menus import MENU_ITEMS

def menu_items(request):
    if request.user.is_authenticated:
        # Obtén el grupo del usuario
        group = request.user.groups.first()
        role = group.name if group else 'guest'
    else:
        role = 'guest'
    
    return {'menu_items': MENU_ITEMS.get(role, [])}
