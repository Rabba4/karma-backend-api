"""
Test for models.
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def  test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_tratamiento(self):
        """Test creando un tratamiento is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        tratamiento = models.Tratamiento.objects.create(
            codigo='1234',
            nombre='tratamiento ejemplo',
            descripcion='Tratamiento de test para probar su creación',
            duracion_minutos=90,
            familia='1',
            precio_base=Decimal('47.50')
        )

        self.assertEqual(str(tratamiento), tratamiento.nombre)

    def test_create_family(self):
        """Test creating a tag is successful."""
        user = create_user()
        family = models.Family.objects.create(codigo='Family1', nombre='Family 1', ultimo_nivel=False)

        self.assertEqual(str(family), family.nombre)
