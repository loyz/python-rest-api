"""
Serializers for translation APIs
"""
from rest_framework import serializers

from core.models import (
    Translation
)

# from bs4 import BeautifulSoup


class TranslationSerializer(serializers.ModelSerializer):
    """Serializer for translations."""

    class Meta:
        model = Translation
        fields = [
            'id', 'content_type', 'translation_input',
            'translation_elements', 'translation_result',
        ]
        read_only_fields = ['id', 'translation_elements', 'translation_result']

    def create(self, validated_data):
        """Create a translation."""
        translation = Translation.objects.create(**validated_data)

        return translation
