"""
Tests for translation APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Translation

from translation.serializers import TranslationSerializer

import html

import json

TRANSLATIONS_URL = reverse('translation:translation-list')

def create_sample_translation(user, **params):
    """Create and return a sample translation."""
    defaults = {
        'content_type': 'HTML',
        'translation_input': "<h2 class='editor-heading-h2' dir='ltr'><span>hallo1 as headline</span></h2><p class='editor-paragraph' dir='ltr'><br></p><p class='editor-paragraph' dir='ltr'><span>hallo2 as paragraph</span></p><p class='editor-paragraph' dir='ltr'><span>hallo3 as paragraph with </span><b><strong class='editor-text-bold'>bold</strong></b><span> inline</span></p>",
        'translation_elements': [
            "<span>hallo1 as headline</span>",
            "<span>hallo2 as paragraph</span>",
            "<span>hallo3 as paragraph with </span><b><strong class='editor-text-bold'>bold</strong></b><span> inline</span>",
        ],
        'translation_result': '',
    }
    defaults.update(params)

    translation = Translation.objects.create(user=user, **defaults)
    return translation


class TranslationApiTests(TestCase):
    """Test authenticated API requests."""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_create_translation(self):
        """Test creating a translation."""
        payload = {
            'user': self.user.id,
            'content_type': 'plain-text',
            'translation_input': "This string will be translated to German",
            'translation_elements': [],
            'translation_result': "Dieser Text wird ins Deutsche übersetzt",
        }

        # Create translation object from API.
        res = self.client.post(TRANSLATIONS_URL, payload)

        # Assert that the translation was created successfully.
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Retrieve created translation from db.
        translation = Translation.objects.get(id=res.data['id'])

        # Assert that the translation was saved correctly.
        self.assertEqual(translation.translation_input, payload['translation_input'])

    def test_retrieve_translation(self):
        """Test retrieving a translation."""
        # Create a translation object.
        translation = Translation.objects.create(
            user=self.user,
            content_type='plain-text',
            translation_input="This string will be translated to German",
            translation_elements=[],
            translation_result="Dieser Text wird ins Deutsche übersetzt",
        )

        # Retrieve the translation object from API.
        res = self.client.get(f'{TRANSLATIONS_URL}{translation.id}/')

        # Assert that the retrieved translation is correct.
        self.assertEqual(res.data['translation_result'], translation.translation_result)
        # Compare user.
        self.assertEqual(translation.user, self.user)
