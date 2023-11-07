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

from deepl import Translator
from app.config import DEEPL_AUTH_KEY

import json


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
    ('plain-text', 'Plain Text'),
    ('html', 'HTML'),
]

translator = Translator(DEEPL_AUTH_KEY)


class Translation(models.Model):
    """Model for translations request & response."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    content_type = models.CharField(max_length=100)
    translation_input = models.TextField(blank=True)
    translation_elements = ArrayField(
        models.CharField(max_length=255),
        blank=True,
        default=list,
        )
    translation_result = models.TextField(blank=True)

    def __str__(self):
        return f"Translation {self.id} Input: {self.translation_input}"

    """save() method is overridden to check if translation_input is present
        and translation_elements is empty. If this condition is true,
        the input is parsed using Beautiful Soup
        and converted to a list of strings using a list comprehension."""
    def save(self, *args, **kwargs):
        if self.content_type == 'plain-text':
            # Translate the input directly if it's a plain text.
            self.translation_result = self.translate_to_german(self.translation_input)
        elif self.translation_input and not self.translation_elements:
            # Otherwise, process the input as HTML.
            self.translation_elements = self.get_soup_content()
            self.translation_elements = (
                self.filter_and_translate_html(self.translation_elements)
                )
            # Set the translation_result field to the joined version of translated elements
            self.translation_result = ' '.join(self.translation_elements)
        super().save(*args, **kwargs)

    def get_soup_content(self):
        soup = BeautifulSoup(self.translation_input, 'html.parser')
        return [str(tag) for tag in soup.find_all()]

    def filter_and_translate_html(self, elements):
        translated_elements = []
        for element in elements:
            soup = BeautifulSoup(element, 'html.parser')
            for tag in soup.find_all():
                if isinstance(tag.string, NavigableString):
                    # Here you should implement the translation logic
                    translated_text = self.translate_to_german(tag.string)
                    print(f"Translated text: {translated_text}")  # Debugging print statement
                    tag.string.replace_with(translated_text)
            translated_elements.append(str(soup))
        return translated_elements

    def translate_to_german(self, text):
        # Implement translation logic here
        translation_output = translator.translate_text(text, target_lang='DE')
        return translation_output

    def to_json(self):
        return json.dumps({
            'id': int(self.id),
            'user': self.user.email,
            'content_type': self.content_type,
            'translation_input': self.translation_input,
            'translation_elements': self.translation_elements,
            'translation_result': self.translation_result,
        })
