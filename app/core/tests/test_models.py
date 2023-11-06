"""
Tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
import json

from core import models


class ModelTests(TestCase):
    """Test Models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@ExaMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that user without email raises error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creation of superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_translation(self):
        """Test creating a translation is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )
        translation = models.Translation.objects.create(
            user=user,
            translation_input='Hello, world!',
            content_type='plain_text',
            translation_output='Hallo, Welt!',
        )

        self.assertEqual(str(translation), translation.translation_input)

        json_data = json.loads(translation.to_json())

        self.assertEqual(json_data['id'], translation.id)
        self.assertEqual(json_data['user'], user.email)
        self.assertEqual(json_data['translation_input'], 'Hello, world!')
        self.assertEqual(json_data['content_type'], 'plain_text')
        self.assertEqual(json_data['translation_output'], 'Hallo, Welt!')