from rest_framework import viewsets, status
from rest_framework.response import Response

from Category.models import Category
from .serializers import DecoDetailSerializer, DecoCreateSerializer, DecoListSerializer
from .models import Deco
from User.services import JWTService
from User.models import User


class DecoViewSet(viewsets.ModelViewSet):
    queryset = Deco.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return DecoCreateSerializer
        elif self.action == 'list':
            return DecoListSerializer
        else:
            return DecoDetailSerializer

    def perform_create(self, serializer):
        pk = JWTService.run_auth_process(self.request.headers)
        if len(User.objects.filter(id=pk).values()):
            serializer.save(user=User.objects.get(id=pk))

    def partial_update(self, request, *args, **kwargs):
        pk = JWTService.run_auth_process(self.request.headers)
        if len(User.objects.filter(id=pk).values()):
            if self.get_object().user == User.objects.get(id=pk):
                instance = self.get_object()
                partial = kwargs.pop('partial', False)
                serializer = self.get_serializer(instance, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)

                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        pk = JWTService.run_auth_process(self.request.headers)
        if len(User.objects.filter(id=pk).values()):
            if self.get_object().user == User.objects.get(id=pk):
                instance = self.get_object()
                self.perform_destroy(instance)

                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class SearchViewSet(viewsets.ModelViewSet):
    serializer_class = DecoListSerializer

    def get_queryset(self):
        if 'q' not in self.request.GET:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        search = self.request.GET['q']

        users = User.objects.filter(name__contains=search)
        queryset = Deco.objects.filter(name__contains=search)
        for user in users:
            queryset |= Deco.objects.filter(user_id=user.id)

        return queryset


class FilterViewSet(viewsets.ModelViewSet):
    serializer_class = DecoListSerializer

    def get_queryset(self):
        if 'categories' not in self.request.GET:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        categories_id = self.request.GET.getlist('categories')
        categories = Category.objects.filter(pk__in=categories_id)
        queryset = Deco.objects.filter(categories__in=categories).distinct()

        return queryset


search_list = SearchViewSet.as_view({'get': 'list'})

filter_list = FilterViewSet.as_view({'get': 'list'})

deco_list = DecoViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

deco_detail = DecoViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})
