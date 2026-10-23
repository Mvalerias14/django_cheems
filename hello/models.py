from django.db import models
from django.utils import timezone


class Profile(models.IntegerChoices):
    ADMINISTRADOR = 1, "Administrador"
    OPERADOR = 2, "Operador"


class Status(models.IntegerChoices):
    PENDIENTE = 1, "Pendiente"
    EN_PROCESO = 2, "En proceso"
    TERMINADA = 3, "Terminada"
    CANCELADA = 4, "Cancelada"


class LogModule(models.IntegerChoices):
    USUARIOS = 1, "Usuarios"
    ORDENES = 2, "Órdenes"


class User(models.Model):
    name = models.CharField(max_length=60, null=True, blank=True)
    account = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    profile = models.IntegerField(
        choices=Profile.choices, default=Profile.OPERADOR, null=True, blank=True
    )

    class Meta:
        managed = False
        db_table = "user"

    def __str__(self):
        return self.name or self.account or f"Usuario {self.pk}"


class WorkOrder(models.Model):
    # La columna real se llama "tittle" (con doble t) en la base de datos.
    title = models.CharField(max_length=70, db_column="tittle", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.IntegerField(
        choices=Status.choices, default=Status.PENDIENTE, null=True, blank=True
    )

    class Meta:
        managed = False
        db_table = "work_order"

    def __str__(self):
        return f"#{self.pk} {self.title}"


class WorkOrderHistory(models.Model):
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    user = models.ForeignKey(
        User, models.DO_NOTHING, db_column="id_user", null=True, blank=True
    )
    work_order = models.ForeignKey(
        WorkOrder,
        models.DO_NOTHING,
        db_column="id_work_order",
        related_name="history",
        null=True,
        blank=True,
    )
    module = models.IntegerField(null=True, blank=True)
    action = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "work_order_history"
        ordering = ["-date"]


class Log(models.Model):
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    description = models.CharField(max_length=155, null=True, blank=True)
    user = models.ForeignKey(
        User, models.DO_NOTHING, db_column="id_user", null=True, blank=True
    )
    module = models.IntegerField(choices=LogModule.choices, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "log"
        ordering = ["-date"]