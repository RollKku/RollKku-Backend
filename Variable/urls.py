from django.urls import path
from . import views

urlpatterns = [
    path('variable', views.variable_list),
]
