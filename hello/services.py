from django.contrib.auth.hashers import make_password
from django.db import transaction

from .models import Log, LogModule, Status, User, WorkOrder, WorkOrderHistory

# Cambios de estado permitidos: estado actual -> estados a los que puede pasar.
TRANSICIONES = {
    Status.PENDIENTE: [Status.EN_PROCESO, Status.CANCELADA],
    Status.EN_PROCESO: [Status.TERMINADA, Status.CANCELADA],
    Status.TERMINADA: [],
    Status.CANCELADA: [],
}


def registrar_log(usuario, modulo, descripcion):
    Log.objects.create(user=usuario, module=modulo, description=descripcion[:155])


@transaction.atomic
def crear_orden(usuario, title, description):
    orden = WorkOrder.objects.create(
        title=title, description=description, status=Status.PENDIENTE
    )
    WorkOrderHistory.objects.create(
        work_order=orden,
        user=usuario,
        module=LogModule.ORDENES,
        action="Orden creada con estado Pendiente",
    )
    registrar_log(usuario, LogModule.ORDENES, f"Creó la orden #{orden.pk}: {title}")
    return orden


@transaction.atomic
def cambiar_estado(orden, nuevo_estado, usuario):
    permitidos = TRANSICIONES.get(orden.status, [])
    if nuevo_estado not in permitidos:
        raise ValueError("Ese cambio de estado no está permitido.")

    anterior = Status(orden.status).label
    nuevo = Status(nuevo_estado).label

    orden.status = nuevo_estado
    orden.save(update_fields=["status"])

    accion = f"Cambió el estado de {anterior} a {nuevo}"
    WorkOrderHistory.objects.create(
        work_order=orden, user=usuario, module=LogModule.ORDENES, action=accion
    )
    registrar_log(usuario, LogModule.ORDENES, f"Orden #{orden.pk}: {accion}")


@transaction.atomic
def crear_usuario(actor, name, account, password, profile):
    usuario = User.objects.create(
        name=name,
        account=account,
        password=make_password(password),
        profile=profile,
    )
    registrar_log(actor, LogModule.USUARIOS, f"Creó el usuario {account}")
    return usuario


@transaction.atomic
def editar_usuario(actor, usuario, name, account, profile, password=None):
    usuario.name = name
    usuario.account = account
    usuario.profile = profile
    if password:
        usuario.password = make_password(password)
    usuario.save()
    detalle = " (cambió la contraseña)" if password else ""
    registrar_log(actor, LogModule.USUARIOS, f"Editó el usuario {account}{detalle}")
    return usuario