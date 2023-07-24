"""
Serializers for tratamientos APIs
"""
from rest_framework import serializers

from core.models import Tratamiento


class TratamientoSerializer(serializers.ModelSerializer):
    """Serializer for tratamientos."""

    class Meta:
        model = Tratamiento
        fields = ['id', 'codigo', 'nombre', 'duracion_minutos', 'familia', 'precio_base']
        read_only_fields = ['id']


class TratamientoDetailSerializer(TratamientoSerializer):
    """Serializer for tratamiento detail view."""

    class Meta(TratamientoSerializer.Meta):
        fields = TratamientoSerializer.Meta.fields + ['descripcion']