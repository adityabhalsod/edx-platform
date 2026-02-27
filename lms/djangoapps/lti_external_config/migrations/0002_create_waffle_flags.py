"""
Data migration to create waffle flags for the LTI external config feature.

Creates:
- lti_consumer.enable_external_config_filter (enables "Reusable Configuration" in XBlock)
- lti_consumer.enable_external_multiple_launch_urls (enables "Database Configuration" in XBlock)
"""
from django.db import migrations


def create_waffle_flags(apps, schema_editor):
    """Create the waffle flags needed for LTI external configuration."""
    Flag = apps.get_model("waffle", "Flag")

    for flag_name in [
        "lti_consumer.enable_external_config_filter",
        "lti_consumer.enable_external_multiple_launch_urls",
    ]:
        Flag.objects.get_or_create(
            name=flag_name,
            defaults={
                "everyone": True,
                "note": "Auto-created by lti_external_config app",
            },
        )


def remove_waffle_flags(apps, schema_editor):
    """Remove the waffle flags (reverse migration)."""
    Flag = apps.get_model("waffle", "Flag")
    Flag.objects.filter(
        name__in=[
            "lti_consumer.enable_external_config_filter",
            "lti_consumer.enable_external_multiple_launch_urls",
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("lti_external_config", "0001_initial"),
        ("waffle", "0004_update_everyone_nullbooleanfield"),
    ]

    operations = [
        migrations.RunPython(create_waffle_flags, remove_waffle_flags),
    ]
