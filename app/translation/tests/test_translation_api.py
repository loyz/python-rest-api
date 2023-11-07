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
        'translation_elements': {
            "<span>hallo1 as headline</span>",
            "<span>hallo2 as paragraph</span>",
            "<span>hallo3 as paragraph with </span><b><strong class='editor-text-bold'>bold</strong></b><span> inline</span>",
        }
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

    def test_pass_and_retrieve_translation(self):
        """Test to pass and retrieve a translation."""
        payload = {
            'content_type': 'HTML',
            'translation_input': "<h2 class='editor-heading-h2' dir='ltr'><span>hallo1 as headline</span></h2><p class='editor-paragraph' dir='ltr'><br></p><p class='editor-paragraph' dir='ltr'><span>hallo2 as paragraph</span></p><p class='editor-paragraph' dir='ltr'><span>hallo3 as paragraph with </span><b><strong class='editor-text-bold'>bold</strong></b><span> inline</span></p>",
            'translation_elements': {
                "<span>hallo1 als Überschrift</span>",
                "<span>hallo2 als Überschrift</span>",
                "<span>hallo3 als Absatz mit </span><b><strong class='editor-text-bold'>fett</strong></b><span> inline</span>",
                }
            'translation_result': "h2 class='editor-heading-h2' dir='ltr'><span>hallo1 als Überschrift</span></h2><p class='editor-paragraph' dir='ltr'><br></p><p class='editor-paragraph' dir='ltr'><span>hallo2 als Absatz</span></p><p class='editor-paragraph' dir='ltr'><span>hallo3 als Absatz mit </span><b><strong class='editor-text-bold'>fett</strong></b><span> Inline</span></p>"
        }
        """Create translation object from API."""
        res = self.client.post(TRANSLATIONS_URL, payload)
        """Translation created successfuly."""
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        """Retrieve created translation from db."""
        translation_id = res.data['id']
        translation = Translation.objects.get(id=translation_id)
        translation_data = translation.to_json()
        """Compare payload to that of retrieved object."""
        # Deserialize the JSON data into a Python dictionary
        translation_dict = json.loads(translation_data)


        # Loop through the payload dictionary and compare its values with the corresponding values in the translation_dict
        for k, v in payload.items():
            # Get the value from the translation_dict that corresponds to the current key in the payload dictionary
            translation_value = translation_dict.get(k)

            # Compare the values
            if v == translation_value:
                print(f"Value of '{k}' matches: {v}")
            else:
                print(f"Value of '{k}' does not match: expected '{v}', got '{translation_value}'")

        self.assertEqual(translation.user, self.user)

