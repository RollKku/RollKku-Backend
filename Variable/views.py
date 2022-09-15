from rest_framework import viewsets
from .serializers import VariableSerializer
from .models import Variable


class VariableViewSet(viewsets.ModelViewSet):
    queryset = Variable.objects.all()
    serializer_class = VariableSerializer


variable_list = VariableViewSet.as_view({
    'get': 'list'
})