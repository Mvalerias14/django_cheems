from django.shortcuts import render
from .entities.user import User
from .entities.work_order import WorkOrder
from .entities.work_order_history import WorkOrderHistory
from .entities.log import Log


def menu(request):
    opciones = [
        {'titulo': 'Usuarios', 'url': 'usuarios', 'icono': '👤'},
        {'titulo': 'Órdenes de trabajo', 'url': 'ordenes', 'icono': '📋'},
        {'titulo': 'Historial', 'url': 'historial', 'icono': '🕘'},
        {'titulo': 'Log', 'url': 'log', 'icono': '📝'},
    ]
    return render(request, 'hello/menu.html', {'opciones': opciones})


def index(request):
    users = User.get_all()
    return render(request, 'hello/index.html', {'users': users})


def ordenes(request):
    orders = WorkOrder.get_all()
    return render(request, 'hello/ordenes.html', {'orders': orders})


def historial(request):
    history = WorkOrderHistory.get_all()
    return render(request, 'hello/historial.html', {'history': history})


def log(request):
    logs = Log.get_all()
    return render(request, 'hello/log.html', {'logs': logs})