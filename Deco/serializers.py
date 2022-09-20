from rest_framework import serializers
from .models import Deco
from User.models import User
from Category.serializers import CategorySerializer
from Category.models import Category
from Variable.serializers import VariableSerializer
from Variable.models import Variable


class DecoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deco
        fields = ['id', 'name', 'thumbnail']
        read_only_fields = ('id',)


class DecoDetailSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True, allow_null=False)
    variables = VariableSerializer(many=True, allow_null=False)

    def get_user_name(self, obj):
        user = User.objects.get(id=obj.user_id)
        return user.name

    class Meta:
        model = Deco
        fields = ['id', 'name', 'thumbnail', 'css', 'user_name', 'categories', 'variables']
        read_only_fields = ('id',)


class DecoCreateSerializer(serializers.ModelSerializer):
    categories = serializers.CharField()
    variables = serializers.CharField()

    def create(self, validated_data):
        deco = Deco.objects.create(name=validated_data['name'],
                                   thumbnail=validated_data['thumbnail'],
                                   css=validated_data['css'],
                                   user=validated_data['user'])
        categories_id = list(map(int, validated_data.pop('categories').split(',')))
        deco.categories.set(Category.objects.filter(pk__in=categories_id))
        variables_id = list(map(int, validated_data.pop('variables').split(',')))
        deco.variables.set(Variable.objects.filter(pk__in=variables_id))
        deco.save()

        return deco

    class Meta:
        model = Deco
        fields = ['id', 'name', 'thumbnail', 'css', 'categories', 'variables']
        read_only_fields = ('id',)
