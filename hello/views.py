from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .decorators import login_requerido, solo_admin
from .models import Log, Profile, Status, User, WorkOrder, WorkOrderHistory
from .services import (
    TRANSICIONES,
    cambiar_estado,
    crear_orden,
    crear_usuario,
    editar_usuario,
)


# Sesión

def login_view(request):
    if request.session.get("user_id"):
        return redirect("menu")

    error = None
    if request.method == "POST":
        account = request.POST.get("account", "").strip()
        password = request.POST.get("password", "")
        usuario = User.objects.filter(account=account).first()
        if usuario and usuario.password and check_password(password, usuario.password):
            request.session["user_id"] = usuario.pk
            return redirect("menu")
        error = "Cuenta o contraseña incorrectos."

    return render(request, "hello/login.html", {"error": error})


@require_POST
def logout_view(request):
    request.session.flush()
    return redirect("login")


@login_requerido
def menu(request):
    opciones = [
        {"titulo": "Órdenes de trabajo", "url": "ordenes", "icono": "📋"},
        {"titulo": "Historial", "url": "historial", "icono": "🕘"},
        {"titulo": "Log", "url": "log", "icono": "📝"},
    ]
    if request.usuario.profile == Profile.ADMINISTRADOR:
        opciones.insert(0, {"titulo": "Usuarios", "url": "usuarios", "icono": "👤"})
    return render(request, "hello/menu.html", {"opciones": opciones})


# Usuarios

@solo_admin
def usuarios(request):
    users = User.objects.order_by("name")
    return render(request, "hello/index.html", {"users": users})


def _validar_usuario(name, account, password, profile, actual=None, editando_a_si_mismo=False):
    errores = []

    if not name:
        errores.append("El nombre es obligatorio.")
    elif len(name) > 60:
        errores.append("El nombre no puede pasar de 60 caracteres.")

    if not account:
        errores.append("La cuenta es obligatoria.")
    elif len(account) > 100:
        errores.append("La cuenta no puede pasar de 100 caracteres.")
    else:
        repetidos = User.objects.filter(account=account)
        if actual:
            repetidos = repetidos.exclude(pk=actual.pk)
        if repetidos.exists():
            errores.append("Ya existe un usuario con esa cuenta.")

    # En alta la contraseña es obligatoria; en edición solo si la quieren cambiar.
    if (actual is None or password) and len(password) < 6:
        errores.append("La contraseña debe tener al menos 6 caracteres.")

    if profile not in Profile.values:
        errores.append("El perfil no es válido.")
    elif editando_a_si_mismo and profile != Profile.ADMINISTRADOR:
        errores.append("No puedes quitarte a ti mismo el perfil de administrador.")

    return errores


def _leer_formulario_usuario(request):
    name = request.POST.get("name", "").strip()
    account = request.POST.get("account", "").strip()
    password = request.POST.get("password", "")
    try:
        profile = int(request.POST.get("profile", ""))
    except ValueError:
        profile = None
    return name, account, password, profile


@solo_admin
def usuario_nuevo(request):
    errores = []
    datos = {"name": "", "account": "", "profile": Profile.OPERADOR}

    if request.method == "POST":
        name, account, password, profile = _leer_formulario_usuario(request)
        datos = {"name": name, "account": account, "profile": profile}
        errores = _validar_usuario(name, account, password, profile)
        if not errores:
            crear_usuario(request.usuario, name, account, password, profile)
            messages.success(request, f"Usuario {account} creado.")
            return redirect("usuarios")

    return render(
        request,
        "hello/usuario_form.html",
        {"errores": errores, "datos": datos, "perfiles": Profile.choices, "editando": False},
    )


@solo_admin
def usuario_editar(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    errores = []
    datos = {"name": usuario.name, "account": usuario.account, "profile": usuario.profile}

    if request.method == "POST":
        name, account, password, profile = _leer_formulario_usuario(request)
        datos = {"name": name, "account": account, "profile": profile}
        errores = _validar_usuario(
            name,
            account,
            password,
            profile,
            actual=usuario,
            editando_a_si_mismo=(usuario.pk == request.usuario.pk),
        )
        if not errores:
            editar_usuario(request.usuario, usuario, name, account, profile, password)
            messages.success(request, f"Usuario {account} actualizado.")
            return redirect("usuarios")

    return render(
        request,
        "hello/usuario_form.html",
        {"errores": errores, "datos": datos, "perfiles": Profile.choices, "editando": True},
    )


#Órdenes

@login_requerido
def ordenes(request):
    orders = WorkOrder.objects.order_by("-id")
    return render(request, "hello/ordenes.html", {"orders": orders})


@login_requerido
def orden_nueva(request):
    errores = []
    title = description = ""

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        if not title:
            errores.append("El título es obligatorio.")
        elif len(title) > 70:
            errores.append("El título no puede pasar de 70 caracteres.")
        if not description:
            errores.append("La descripción es obligatoria.")

        if not errores:
            orden = crear_orden(request.usuario, title, description)
            messages.success(request, f"Orden #{orden.pk} creada.")
            return redirect("orden_detalle", pk=orden.pk)

    return render(
        request,
        "hello/orden_form.html",
        {"errores": errores, "title": title, "description": description},
    )


@login_requerido
def orden_detalle(request, pk):
    orden = get_object_or_404(WorkOrder, pk=pk)

    if request.method == "POST":
        try:
            nuevo = int(request.POST.get("status", ""))
        except ValueError:
            messages.error(request, "Estado inválido.")
        else:
            try:
                cambiar_estado(orden, nuevo, request.usuario)
            except ValueError as e:
                messages.error(request, str(e))
            else:
                messages.success(request, "Estado actualizado.")
        return redirect("orden_detalle", pk=pk)

    permitidos = [(v, Status(v).label) for v in TRANSICIONES.get(orden.status, [])]
    historial = orden.history.select_related("user")
    return render(
        request,
        "hello/orden_detalle.html",
        {"orden": orden, "permitidos": permitidos, "historial": historial},
    )

#Consultas

@login_requerido
def historial(request):
    history = WorkOrderHistory.objects.select_related("user", "work_order")
    return render(request, "hello/historial.html", {"history": history})


@login_requerido
def log(request):
    logs = Log.objects.select_related("user")
    return render(request, "hello/log.html", {"logs": logs})