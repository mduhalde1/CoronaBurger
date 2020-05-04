from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, IntegerField, RelatedField
from api.models import Ingrediente, Hamburguesa


class HamburguesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hamburguesa
        fields = ['id','nombre', 'precio', 'descripcion', 'imagen', 'ingredientes']
        extra_kwargs = {'id': {'read_only': True, 'required': True}}

class HamburguesaSimplifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hamburguesa
        fields = ['nombre', 'precio', 'descripcion', 'imagen']

class IngredienteSerializer(serializers.ModelSerializer):
    hamburguesas = HamburguesaSerializer()
    class Meta:
        model = Ingrediente
        fields = ['id', 'nombre', 'descripcion', 'hamburguesas']
        extra_kwargs = {'id': {'read_only': True, 'required': True}}


class IngredienteSimplifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = ['id', 'nombre', 'descripcion']
        extra_kwargs = {'id': {'read_only': True, 'required': True}}
        
