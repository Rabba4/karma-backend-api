"""
Tests for tratamientos APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tratamiento

from tratamientos.serializers import (
    TratamientoSerializer,
    TratamientoDetailSerializer,
)

import logging
logger = logging.getLogger("django")


TRATAMIENTOS_URL = reverse('tratamientos:tratamiento-list')

def detail_url(tratamiento_id):
    """Create and return a tratamiento detail URL."""
    return reverse('tratamientos:tratamiento-detail', args=[tratamiento_id])

def create_tratamiento(codigo, nombre, descripcion, duracion_minutos, familia, precio_base, **params):
    """Create and return a sample tratamiento."""
    defaults = {
        'codigo': codigo,
        'nombre': nombre,
        'descripcion': descripcion,
        'duracion_minutos': duracion_minutos,
        'familia': familia,
        'precio_base': Decimal(precio_base)
    }
    defaults.update(params)

    tratamiento = Tratamiento.objects.create(**defaults)
    return tratamiento

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicTratmientoAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(TRATAMIENTOS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTratamientoAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='testpass123')
        self.client.force_authenticate(self.user)

    def test_retrieve_tratamientos(self):
        """Test retieving a list of tratamientos."""
        create_tratamiento(
            codigo='INDIBA30',
            nombre='INDIBA 30 MINUTOS',
            descripcion='Sesión de masaje con Indiba de duración 30 minutos.',
            duracion_minutos=30,
            familia='IN',
            precio_base='47.50'
        )

        create_tratamiento(
            codigo='INDIBA60',
            nombre='INDIBA 60 MINUTOS',
            descripcion='Sesión de masaje con Indiba de duración 60 minutos.',
            duracion_minutos=60,
            familia='IN',
            precio_base='90'
        )

        res = self.client.get(TRATAMIENTOS_URL)

        tratamientos = Tratamiento.objects.all().order_by('-id')
        serializer = TratamientoSerializer(tratamientos, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_tratamiento_detail(self):
        """Test get tratamiento detail."""
        tratamiento = create_tratamiento(
            codigo='INDIBA30',
            nombre='INDIBA 30 MINUTOS',
            descripcion='Sesión de masaje con Indiba de duración 30 minutos.',
            duracion_minutos=30,
            familia='IN',
            precio_base='47.50'
        )

        url = detail_url(tratamiento.id)
        res = self.client.get(url)

        serializer = TratamientoDetailSerializer(tratamiento)
        self.assertEqual(res.data, serializer.data)

    def test_create_tratamiento(self):
        """Test creating a tratamiento."""
        payload = {
            'codigo': 'INDIBA30',
            'nombre': 'INDIBA 30 MINUTOS',
            'descripcion': 'Tratamiento de indiba de duración 30 minutos.',
            'duracion_minutos': 30,
            'familia': 'IN',
            'precio_base': Decimal('47.50'),
        }
        res = self.client.post(TRATAMIENTOS_URL, payload) #/api/tratamientos/tratamiento

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        tratamiento = Tratamiento.objects.get(id=res.data['id'])
        for key, value in payload.items():
            self.assertEqual(getattr(tratamiento, key), value)

    def test_partial_update(self):
        """Test partial update of a treatment."""
        descripcion_original = 'Sesión de Indiba de 30 minutos.'
        tratamiento = create_tratamiento(
            codigo='INDIBA30',
            nombre='INDIBA 30 MINUTOS',
            descripcion=descripcion_original,
            duracion_minutos=30,
            familia='IN',
            precio_base=Decimal('47.50')
        )

        payload = {'precio_base': Decimal('50')}
        url = detail_url(tratamiento.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tratamiento.refresh_from_db()
        self.assertEqual(tratamiento.precio_base, payload['precio_base'])
        self.assertEqual(tratamiento.descripcion, descripcion_original)

    def test_full_update(self):
        """Test full update of treatment."""
        tratamiento = create_tratamiento(
            codigo='INDIBA30',
            nombre='INDIBA 30 MINUTOS',
            descripcion='Sesión de Indiba de 30 minutos.',
            duracion_minutos=30,
            familia='IN',
            precio_base=Decimal('47.50')
        )

        payload  = {
            'codigo': 'INDIBA40',
            'nombre': 'INDIBA 40 MIN',
            'descripcion': 'Sesión de masaje con Indiba de 40 minutos de duración.',
            'duracion_minutos': 40,
            'familia': 'IN',
            'precio_base': Decimal('57.50')
        }
        url = detail_url(tratamiento.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tratamiento.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(tratamiento, k), v)

    def test_delete_treatment(self):
        """Test deleting a treatment successfull."""
        tratamiento = create_tratamiento(
            codigo='INDIBA30',
            nombre='INDIBA 30 MINUTOS',
            descripcion='Sesión de Indiba de 30 minutos.',
            duracion_minutos=30,
            familia='IN',
            precio_base=Decimal('47.50')
        )

        url = detail_url(tratamiento.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tratamiento.objects.filter(id=tratamiento.id).exists())
