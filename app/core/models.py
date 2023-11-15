"""
Database Models.
"""
from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
    Permission,
    )

from bs4 import BeautifulSoup, NavigableString

import json

from deepl import Translator
# from app.config import DEEPL_AUTH_KEY
import os
# Get the value of DEEPL_AUTH_KEY from the environment variable
DEEPL_AUTH_KEY = os.environ.get('DEEPL_AUTH_KEY')

# If DEEPL_AUTH_KEY is empty, fallback to the value from app/config.py
if not DEEPL_AUTH_KEY:
    from app import config
    DEEPL_AUTH_KEY = config.DEEPL_AUTH_KEY


class UserManager(BaseUserManager):
    """Manager for Users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name="core_user_groups",
        # other arguments...
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name="core_user_permissions",
        # other arguments...
    )


CONTENT_TYPE_CHOICES = [
    ('plain_text', 'Plain Text'),
    ('html', 'HTML'),
]

translator = Translator(DEEPL_AUTH_KEY)


class Translation(models.Model):
    """Model for translations request & response."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    content_type = \
        models.CharField(max_length=100, choices=CONTENT_TYPE_CHOICES)
    translation_input = models.TextField(blank=True)
    translation_elements = ArrayField(
        models.CharField(max_length=255),
        blank=True,
        default=list,
        )
    translation_result = models.TextField(blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._translator = None

    def __str__(self):
        return f"Translation {self.id} Input: {self.translation_input}"

    def translate_input(self):
        if self.content_type == 'plain_text':
            # Translate the input directly if it's a plain text.
            self.translation_result = self.translate_to_german(self.translation_input)
        elif self.translation_input:
            # Otherwise, process the input as HTML.
            soup = self.translate_html()
            self.translation_result = str(soup)
            # print(soup)
            return self.translation_result

    def translate_html(self, tags=None):
        """Translate HTML tags."""
        soup = BeautifulSoup(self.translation_input, 'html.parser')
        if tags is None:
            tags = soup.find_all(True)  # Find all tags
        for tag in tags:
            if isinstance(tag, NavigableString):
                # Translate the NavigableString object
                translated_text = self.translate_to_german(str(tag))
                # print(translated_text)
                tag.parent.string.replace_with(str(translated_text))
            elif tag.contents:
                # If the tag has children, handle them recursively
                self.translate_html(tag.contents)

        self.translation_result = str(soup)

        return self.translation_result

    def get_soup_content(self):
        """Get BeautifulSoup object from input."""
        return BeautifulSoup(self.translation_input, 'html.parser')

    def translate_to_german(self, text):
        if not self._translator:
            auth_key = DEEPL_AUTH_KEY
            if not auth_key:
                raise ValueError("DEEPL_AUTH_KEY must be set.")
            self._translator = Translator(auth_key)
        # print(text)
        translation_output = self._translator.translate_text(text, target_lang='DE')
        return translation_output

    def save(self, *args, **kwargs):
        # Call translate_input method before saving the object.
        self.translate_input()
        super().save(*args, **kwargs)

    def to_json(self):
        return json.dumps({
            'id': int(self.id),
            'user': self.user.email,
            'content_type': self.content_type,
            'translation_input': self.translation_input,
            'translation_elements': self.translation_elements,
            'translation_result': self.translation_result,
        })
