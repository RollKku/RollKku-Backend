from django.urls import path
from . import views

urlpatterns = [
    path('deco/<int:pk>/favorite', views.set_favorite),
    path('user/favorite', views.get_favorites),
]
