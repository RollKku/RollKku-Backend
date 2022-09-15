from rest_framework import viewsets
from .serializers import CategorySerializer
from .models import Category


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


category_list = CategoryViewSet.as_view({
    'get': 'list',
})