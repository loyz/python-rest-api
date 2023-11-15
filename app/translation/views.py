"""
Views for the translation APIs
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from rest_framework import (
    viewsets,
    mixins,
    status,
)
# from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Translation
)
from translation import serializers


class TranslationViewSet(viewsets.ModelViewSet):
    """View for manage translation APIs."""
    serializer_class = serializers.TranslationSerializer
    queryset = Translation.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve translations for authenticated user."""
        queryset = self.queryset

        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.TranslationSerializer
        elif self.action == 'upload_image':
            return serializers.TranslationImageSerializer

        return self.serializer_class

    def create(self, request, *args, **kwargs):
            """Create a new translation."""
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Call translate_input() method before saving the object.
            translation = serializer.save(user=request.user)
            # translation.translate_input()
            # translation.save()

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Filter by items assigned to translations.',
            ),
        ]
    )
)
class BaseTranslationAttrViewSet(mixins.DestroyModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.ListModelMixin,
                                 viewsets.GenericViewSet):
    """Base viewset for translation attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(Translation__isnull=False)

        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()
