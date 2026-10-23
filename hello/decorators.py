from functools import wraps

from django.shortcuts import redirect

from .models import User


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