"""
Models for the LTI External Configuration app.

Provides a proxy model over the existing LtiConfiguration from
xblock-lti-consumer, used purely for admin separation and query filtering.
No new database tables are created.
"""
import re

from django.db import models

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from lti_consumer.models import LtiConfiguration
from opaque_keys.edx.django.models import UsageKeyField


SLUG_REGEX = re.compile(r'^[a-zA-Z0-9][-a-zA-Z0-9_]*$')


class ReusableLtiConfiguration(LtiConfiguration):
    """
    Proxy model for managing reusable LTI template configurations.

    These are LtiConfiguration records where:
    - location is NULL (not tied to any specific XBlock)
    - config_store is CONFIG_ON_DB

    Other XBlocks reference them via CONFIG_EXTERNAL with
    external_id = "lti_reusable:<config_id_uuid>"

    No new database table is created.
    """

    class Meta:
        proxy = True
        app_label = "lti_external_config"
        verbose_name = "Reusable LTI Configuration"
        verbose_name_plural = "Reusable LTI Configurations"

    def clean(self):
        """
        Validate the slug (stored in external_id) and skip the parent's
        consumer-creation validation for template configs.
        """
        # Validate slug is present and well-formed
        if not self.external_id or not SLUG_REGEX.match(self.external_id):
            raise ValidationError({
                "external_id": _(
                    "Slug is required and must contain only letters, numbers, hyphens, "
                    "and underscores (e.g. 'my-zoom-tool')."
                ),
            })

        # Check slug uniqueness among template configs
        qs = LtiConfiguration.objects.filter(
            location=UsageKeyField.Empty,
            config_store=self.CONFIG_ON_DB,
            external_id=self.external_id,
        )
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError({
                "external_id": _("A reusable config with this slug already exists."),
            })

        # Validate LTI 1.3 has either a public key or keyset URL
        if self.version == self.LTI_1P3 and self.config_store == self.CONFIG_ON_DB:
            if self.lti_1p3_tool_public_key == "" and self.lti_1p3_tool_keyset_url == "":
                raise ValidationError({
                    "lti_1p3_tool_keyset_url": _(
                        "LTI 1.3 requires either a Tool Public Key or a Tool Keyset URL."
                    ),
                })

    def save(self, *args, **kwargs):
        """Force config_store and location for template configs."""
        self.config_store = self.CONFIG_ON_DB
        self.location = None
        # Skip sync_configurations (parent's save calls it, but it's irrelevant for templates)
        # Call grandparent save directly
        models.Model.save(self, *args, **kwargs)

    def __str__(self):
        slug = self.external_id or "no-slug"
        return f"Reusable LTI: {slug}"
