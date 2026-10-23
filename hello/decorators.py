from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from .models import Profile, User


def login_requerido(vista):
    """Protege una vista: si no hay sesión válida, manda al login."""

    @wraps(vista)
    def envoltura(request, *args, **kwargs):
        user_id = request.session.get("user_id")
        usuario = User.objects.filter(pk=user_id).first() if user_id else None
        if usuario is None:
            request.session.flush()
            return redirect("login")
        request.usuario = usuario  # disponible en la vista y en las plantillas
        return vista(request, *args, **kwargs)

    return envoltura


def solo_admin(vista):
    """Además de tener sesión, exige el perfil Administrador."""

    @login_requerido
    @wraps(vista)
    def envoltura(request, *args, **kwargs):
        if request.usuario.profile != Profile.ADMINISTRADOR:
            messages.error(request, "No tienes permiso para esta sección.")
            return redirect("menu")
        return vista(request, *args, **kwargs)

    return envoltura