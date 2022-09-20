from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('deco', views.deco_list),
    path('deco/search', views.search_list),
    path('deco/filter', views.filter_list),
    path('deco/<int:pk>', views.deco_detail),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
