"""
App configuration for lti_external_config.

On ready(), configures OPEN_EDX_FILTERS_CONFIG to wire the pipeline step
so that no Tutor plugin is needed.
"""
from django.apps import AppConfig
from django.conf import settings


class LtiExternalConfigConfig(AppConfig):
    """
    Application configuration for the LTI External Configuration app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "lms.djangoapps.lti_external_config"
    verbose_name = "LTI External Configuration"
    plugin_app = {}

    def ready(self):
        """
        Configure OPEN_EDX_FILTERS_CONFIG to wire the pipeline step.

        This runs at Django startup and replaces the settings configuration
        that was previously done by the Tutor plugin.
        """
        filter_name = "org.openedx.xblock.lti_consumer.configuration.listed.v1"
        step_name = "lms.djangoapps.lti_external_config.pipelines.GetLtiConfigurations"

        if not hasattr(settings, "OPEN_EDX_FILTERS_CONFIG"):
            settings.OPEN_EDX_FILTERS_CONFIG = {}

        if filter_name not in settings.OPEN_EDX_FILTERS_CONFIG:
            settings.OPEN_EDX_FILTERS_CONFIG[filter_name] = {
                "fail_silently": False,
                "pipeline": [],
            }

        pipeline = settings.OPEN_EDX_FILTERS_CONFIG[filter_name]["pipeline"]
        if step_name not in pipeline:
            pipeline.append(step_name)
