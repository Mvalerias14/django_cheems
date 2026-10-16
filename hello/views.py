from django.shortcuts import render
from .entities.user import User


def menu(request):
    opciones = [
        {'titulo': 'Usuarios', 'url': 'usuarios', 'icono': '👤'},
    ]
    return render(request, 'hello/menu.html', {'opciones': opciones})


def index(request):
    users = User.get_all()
    return render(request, 'hello/index.html', {'users': users})