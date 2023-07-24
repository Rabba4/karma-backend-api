"""
URL mappings for the tratamiento app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from tratamientos import views


router = DefaultRouter()
router.register('tratamientos', views.TratamientoViewSet)

app_name = 'tratamientos'

urlpatterns = [
    path('', include(router.urls)),
]

