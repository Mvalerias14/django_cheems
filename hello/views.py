#from django.shortcuts import render
#from .entities.user import User
#from .entities.work_order import WorkOrder
#from .entities.work_order_history import WorkOrderHistory
#from .entities.log import Log


#def menu(request):
#    opciones = [
#        {'titulo': 'Usuarios', 'url': 'usuarios', 'icono': '👤'},
#        {'titulo': 'Órdenes de trabajo', 'url': 'ordenes', 'icono': '📋'},
#        {'titulo': 'Historial', 'url': 'historial', 'icono': '🕘'},
#        {'titulo': 'Log', 'url': 'log', 'icono': '📝'},
#    ]
#    return render(request, 'hello/menu.html', {'opciones': opciones})


#def index(request):
#    users = User.get_all()
#    return render(request, 'hello/index.html', {'users': users})


#def ordenes(request):
#    orders = WorkOrder.get_all()
#    return render(request, 'hello/ordenes.html', {'orders': orders})


#def historial(request):
#    history = WorkOrderHistory.get_all()
#    return render(request, 'hello/historial.html', {'history': history})


#def log(request):
#    logs = Log.get_all()
#    return render(request, 'hello/log.html', {'logs': logs})


from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .decorators import login_requerido
from .models import Log, Status, User, WorkOrder, WorkOrderHistory
from .services import TRANSICIONES, cambiar_estado, crear_orden


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
        {"titulo": "Usuarios", "url": "usuarios", "icono": "👤"},
        {"titulo": "Órdenes de trabajo", "url": "ordenes", "icono": "📋"},
        {"titulo": "Historial", "url": "historial", "icono": "🕘"},
        {"titulo": "Log", "url": "log", "icono": "📝"},
    ]
    return render(request, "hello/menu.html", {"opciones": opciones})


@login_requerido
def usuarios(request):
    users = User.objects.order_by("name")
    return render(request, "hello/index.html", {"users": users})


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
            cambiar_estado(orden, nuevo, request.usuario)
        except ValueError as e:
            messages.error(request, str(e) or "Estado inválido.")
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


@login_requerido
def historial(request):
    history = WorkOrderHistory.objects.select_related("user", "work_order")
    return render(request, "hello/historial.html", {"history": history})


@login_requerido
def log(request):
    logs = Log.objects.select_related("user")
    return render(request, "hello/log.html", {"logs": logs})