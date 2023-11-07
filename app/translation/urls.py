"""
URL mappings for the translation app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from translation import views


router = DefaultRouter()
router.register('translation', views.TranslationViewSet)

app_name = 'translation'

urlpatterns = [
    path('', include(router.urls)),
]
