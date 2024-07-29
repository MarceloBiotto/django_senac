"""
URL configuration for meuprojeto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.contrib import admin
from django.urls import path,include
from main import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('atualizarUsuario/<int:id>/', views.atualizarUsuario, name='atualizarUsuario'),
    path('apostar/', views.apostar, name='apostar'),
    path('atualizar_usuario/<int:id>/', views.atualizar_usuario, name='atualizar_usuario'),
    path('deletar_usuario/<int:id>/', views.deletar_usuario, name='deletar_usuario'),
]