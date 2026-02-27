"""
Django admin registration for the LTI External Configuration app.

Provides a dedicated admin interface for creating/managing reusable
LTI template configurations (LtiConfiguration records with location=None).
"""
from django.contrib import admin

from .models import ReusableLtiConfiguration
from opaque_keys.edx.django.models import UsageKeyField


PLUGIN_PREFIX = "lti_reusable"


class ReusableLtiConfigurationAdmin(admin.ModelAdmin):
    """
    Admin for managing reusable LTI template configurations.

    Only shows LtiConfiguration records that are templates
    (location=None, config_store=CONFIG_ON_DB).
    """

    list_display = ("reusable_id", "version", "lti_1p3_launch_url", "lti_1p1_launch_url")
    list_filter = ("version",)
    readonly_fields = ("reusable_id_display",)

    fieldsets = (
        ("Template Info", {
            "fields": ("external_id", "reusable_id_display", "version"),
            "description": "Set a slug (e.g. 'my-zoom-tool') to identify this config. "
                           "Copy the Reusable Config ID into the XBlock.",
        }),
        ("LTI 1.1 Configuration", {
            "classes": ("collapse",),
            "fields": (
                "lti_1p1_launch_url",
                "lti_1p1_client_key",
                "lti_1p1_client_secret",
            ),
        }),
        ("LTI 1.3 Configuration", {
            "classes": ("collapse",),
            "fields": (
                "lti_1p3_client_id",
                "lti_1p3_oidc_url",
                "lti_1p3_launch_url",
                "lti_1p3_tool_public_key",
                "lti_1p3_tool_keyset_url",
                "lti_1p3_redirect_uris",
            ),
        }),
        ("LTI Advantage", {
            "classes": ("collapse",),
            "fields": (
                "lti_advantage_ags_mode",
                "lti_advantage_deep_linking_enabled",
                "lti_advantage_deep_linking_launch_url",
                "lti_advantage_enable_nrps",
            ),
        }),
    )

    def get_queryset(self, request):
        """Only show template configs (no location, stored on DB)."""
        return (
            super()
            .get_queryset(request)
            .filter(
                location=UsageKeyField.Empty,
                config_store=ReusableLtiConfiguration.CONFIG_ON_DB,
            )
        )

    def reusable_id(self, obj):
        """The external_config ID to paste into XBlock settings."""
        return f"{PLUGIN_PREFIX}:{obj.external_id}" if obj.external_id else "(set slug first)"

    reusable_id.short_description = "Reusable Config ID (paste in XBlock)"

    def reusable_id_display(self, obj):
        """Read-only display of the reusable ID in the detail view."""
        if obj.external_id:
            return f"{PLUGIN_PREFIX}:{obj.external_id}"
        return "(will be generated on save)"

    reusable_id_display.short_description = "Reusable Config ID"


admin.site.register(ReusableLtiConfiguration, ReusableLtiConfigurationAdmin)
