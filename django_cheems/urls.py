"""
URL configuration for django_cheems project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""from django.contrib import admin
from django.urls import path
from hello import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.menu, name='menu'),
    path('usuarios/', views.index, name='usuarios'),
    path('ordenes/', views.ordenes, name='ordenes'),
    path('historial/', views.historial, name='historial'),
    path('log/', views.log, name='log'),
]"""
from django.urls import path

from hello import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.menu, name='menu'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('ordenes/', views.ordenes, name='ordenes'),
    path('ordenes/nueva/', views.orden_nueva, name='orden_nueva'),
    path('ordenes/<int:pk>/', views.orden_detalle, name='orden_detalle'),
    path('historial/', views.historial, name='historial'),
    path('log/', views.log, name='log'),
]