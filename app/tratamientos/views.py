"""
Views for the tratamiento APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tratamiento
from tratamientos import serializers


class TratamientoViewSet(viewsets.ModelViewSet):
    """View for manage tratamiento APIs."""
    serializer_class = serializers.TratamientoDetailSerializer
    queryset = Tratamiento.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.TratamientoSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new treatment."""
        serializer.save()
