from django.urls import path

from . import views


urlpatterns = [
    path('create', views.createUser),
    path('auth', views.login),
    path('refresh', views.refresh)
]