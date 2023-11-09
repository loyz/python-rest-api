"""
Tests for translation APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from core.models import Translation

# from translation.serializers import TranslationSerializer

# import html

# import json

TRANSLATIONS_URL = reverse('translation:translation-list')


def create_sample_translation(user, **params):
    """Create and return a sample translation."""
    defaults = {
        'content_type': 'HTML',
        'translation_input': "<h2 class='editor-heading-h2' dir='ltr'> \
         <span>hallo1 as headline</span></h2>  \
         <p class='editor-paragraph' dir='ltr'><br></p>  \
         <p class='editor-paragraph' dir='ltr'><span>hallo2 as paragraph  \
         </span></p><p class='editor-paragraph' dir='ltr'><span>hallo3 as  \
         paragraph with </span><b><strong class='editor-text-bold'>bold \
         </strong></b><span> inline</span></p>",
        'translation_elements': [
            "<span>hallo1 as headline</span>",
            "<span>hallo2 as paragraph</span>",
            "<span>hallo3 as paragraph with </span> \
            <b><strong class='editor-text-bold'>bold</strong> \
            </b><span> inline</span>",
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
        self.user = get_user_model().objects.create_superuser(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)
        # Create a token for the test user.
        self.token = Token.objects.create(user=self.user)
        # Include the token in the Authorization header.
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_translation(self):
        """Test creating a translation."""
        payload = {
            'user': self.user.id,
            'content_type': 'plain_text',
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
        self.assertEqual(
            translation.translation_input, payload['translation_input']
            )

    def test_retrieve_translation(self):
        """Test retrieving a translation."""
        # Create a translation object.
        translation = Translation.objects.create(
            user=self.user,
            content_type='plain_text',
            translation_input="This string will be translated to German",
            translation_elements=[],
            translation_result="Dieser Text wird ins Deutsche übersetzt",
        )

        # Retrieve the translation object from API.
        res = self.client.get(f'{TRANSLATIONS_URL}{translation.id}/')
        print(translation.translation_result) # print statement for debugging
        # Assert that the retrieved translation is correct.
        self.assertEqual(
            res.data['translation_result'], translation.translation_result.text
            )
        # Compare user.
        self.assertEqual(translation.user, self.user)

    def test_actual_translation_plain_text(self):
        """Test actual translation from English to German."""
        # Define the input and expected output.
        input_text = "This string will be translated to German"
        expected_output = "Diese Zeichenfolge wird ins Deutsche übersetzt"

        # Prepare the payload.
        payload = {
            'user': self.user.id,
            'content_type': 'plain_text',
            'translation_input': input_text,
        }

        # Create translation object from API.
        res = self.client.post(TRANSLATIONS_URL, payload)

        # Check that the request was successful.
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Check that the returned translation matches the expected output.
        # print(res.data) # @debug
        self.assertEqual(res.data['translation_result'], expected_output)

    # def test_actual_translation_html(self):
    #     """Test actual translation from English to German for input containing HTML."""
    #     # Define the input and expected output.
    #     input_text = "<h1 class='translation'>Translation</h1><p class='paragraph'>This string will be translated to German</p>"
    #     expected_output = '<h1 class="translation">Übersetzung</h1> <p class="paragraph">Dieser Text wird ins Deutsche übersetzt</p>'

    #     # Prepare the payload.
    #     payload = {
    #         'user': self.user.id,
    #         'content_type': 'html',
    #         'translation_input': input_text,
    #     }

    #     # Mock the `translate_to_german` method.
    #     with patch('core.models.Translation.translate_to_german', \
    #     return_value=expected_output) as mock_translate:
    #         # Create translation object from API.
    #         res = self.client.post(TRANSLATIONS_URL, payload)

    #     # Check that the request was successful.
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    #     # Check that the returned translation matches the expected output.
    #     print(res.data)
    #     self.assertEqual(res.data['translation_result'], expected_output)

    # def test_translation_admin_endpoint(self):
    #     # Create a Translation instance
    #     translation = Translation.objects.create(
    #         user=self.user,
    #         content_type='plain_text',
    #         translation_input="This string will be translated to German",
    #         translation_elements=[],
    #         translation_result="Dieser Text wird ins Deutsche übersetzt",
    #     )
    #     # Call the save method to perform the translation
    #     translation.save()

    #     # Send a GET request to the API endpoint
    #     response = self.client.get('/api/user/me/')
    #     # self.client.get(f'/admin/core/translation/{translation.id}/change/')

    #     # Check that the response status code is 200 (OK)
    #     # Test failing because user isn't staff?
    #     # self.assertEqual(response.status_code, 200)

    #     # Check that the response data contains the correct translation
    #     # self.assertContains(response, 'Diese Zeichenfolge wird ins Deutsche übersetzt')
