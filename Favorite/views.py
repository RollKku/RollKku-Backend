from rest_framework import viewsets, status
from rest_framework.response import Response

from User.models import User
from User.services import JWTService
from .serializers import FavoriteSerializer
from .models import Favorite
from Deco.models import Deco
from Deco.serializers import DecoListSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = DecoListSerializer

    def get_queryset(self):
        pk = JWTService.run_auth_process(self.request.headers)
        if len(User.objects.filter(id=pk).values()):
            user = User.objects.get(id=pk)
            favorites = Favorite.objects.filter(user_id=user)
            queryset = Deco.objects.filter(id__in=[favorite.deco.id for favorite in favorites])
            return queryset
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        deco_pk = self.kwargs.get('pk')
        user_pk = JWTService.run_auth_process(self.request.headers)

        if not deco_pk or len(User.objects.filter(id=user_pk).values()):
            user = User.objects.get(id=user_pk)
            deco = Deco.objects.get(pk=deco_pk)

            if len(Favorite.objects.filter(user=user).filter(deco=deco).values()):
                Favorite.objects.get(user=user, deco=deco).delete()
            else:
                Favorite.objects.create(user=user, deco=deco)

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


get_favorites = FavoriteViewSet.as_view({
    'get': 'list',
})

set_favorite = FavoriteViewSet.as_view({
    'post': 'create'
})