"""
OpenEdx Filters pipeline step for LTI reusable configurations.

Reads from existing LtiConfiguration records (with location=None,
config_store=CONFIG_ON_DB) and serves them via the
org.openedx.xblock.lti_consumer.configuration.listed.v1 filter.

No new model is needed — this reuses the xblock-lti-consumer's own
LtiConfiguration model.
"""
import logging
from typing import Dict

from openedx_filters import PipelineStep

from lti_consumer.models import LtiConfiguration
from opaque_keys.edx.django.models import UsageKeyField


log = logging.getLogger(__name__)

PLUGIN_PREFIX = "lti_reusable"


def _serialize_config(config_obj):
    """
    Serialize a LtiConfiguration object into the dict format expected
    by the LTI consumer's CONFIG_EXTERNAL code paths.

    Uses the property-based accessors for private key / key ID / public JWK
    so that auto-generation of keys is triggered if needed.
    """
    data = {
        "version": config_obj.version,
        # LTI 1.1
        "lti_1p1_launch_url": config_obj.lti_1p1_launch_url,
        "lti_1p1_client_key": config_obj.lti_1p1_client_key,
        "lti_1p1_client_secret": config_obj.lti_1p1_client_secret,
        # LTI 1.3
        "lti_1p3_client_id": config_obj.lti_1p3_client_id,
        "lti_1p3_oidc_url": config_obj.lti_1p3_oidc_url,
        "lti_1p3_launch_url": config_obj.lti_1p3_launch_url,
        "lti_1p3_tool_public_key": config_obj.lti_1p3_tool_public_key,
        "lti_1p3_tool_keyset_url": config_obj.lti_1p3_tool_keyset_url,
        "lti_1p3_redirect_uris": config_obj.lti_1p3_redirect_uris,
        # Use properties (not internal fields) for private key / key ID / JWK
        # These properties auto-generate keys if missing.
        "lti_1p3_private_key": config_obj.lti_1p3_private_key,
        "lti_1p3_private_key_id": config_obj.lti_1p3_private_key_id,
        "lti_1p3_public_jwk": config_obj.lti_1p3_public_jwk,
        # LTI Advantage
        "lti_advantage_ags_mode": config_obj.lti_advantage_ags_mode,
        "lti_advantage_deep_linking_enabled": config_obj.lti_advantage_deep_linking_enabled,
        "lti_advantage_deep_linking_launch_url": config_obj.lti_advantage_deep_linking_launch_url,
        "lti_advantage_enable_nrps": config_obj.lti_advantage_enable_nrps,
    }
    return data


def _get_template_configs():
    """
    Return a queryset of all LtiConfiguration records that are
    reusable templates (location=None, config_store=CONFIG_ON_DB).
    """
    return LtiConfiguration.objects.filter(
        location=UsageKeyField.Empty,
        config_store=LtiConfiguration.CONFIG_ON_DB,
    )


class GetLtiConfigurations(PipelineStep):
    """
    Pipeline step that serves reusable LTI configurations from the
    existing LtiConfiguration model (xblock-lti-consumer).

    Registered with the filter:
        org.openedx.xblock.lti_consumer.configuration.listed.v1

    Config IDs use the format: "lti_reusable:<slug>"
    Example: "lti_reusable:my-zoom-tool"

    Example OPEN_EDX_FILTERS_CONFIG:

        OPEN_EDX_FILTERS_CONFIG = {
            "org.openedx.xblock.lti_consumer.configuration.listed.v1": {
                "fail_silently": False,
                "pipeline": [
                    "lms.djangoapps.lti_external_config.pipelines.GetLtiConfigurations"
                ]
            }
        }
    """

    def run_filter(
        self, context: Dict, config_id: str, configurations: Dict, *args, **kwargs
    ):  # pylint: disable=arguments-differ, unused-argument
        """
        Execute the filter pipeline step.

        Arguments:
            context (dict): Context dictionary from the LTI Consumer XBlock.
            config_id (str): If provided, fetch only this specific configuration.
                Format: "lti_reusable:<slug>"
            configurations (dict): Accumulated configs from other pipeline steps.

        Returns:
            dict: Updated configurations, config_id, and context.
        """
        config = {}

        if config_id:
            # Extract the slug from the config_id (format: "prefix:slug")
            try:
                _slug = config_id.split(":", 1)[1]
            except IndexError:
                _slug = config_id

            try:
                config_obj = _get_template_configs().get(external_id=_slug)
                config = {
                    f"{PLUGIN_PREFIX}:{config_obj.external_id}": _serialize_config(config_obj)
                }
            except LtiConfiguration.DoesNotExist:
                log.warning("Reusable LTI config not found: %s", config_id)
                config = {}
        else:
            # Return all available template configurations.
            for obj in _get_template_configs().exclude(external_id__isnull=True).exclude(external_id=""):
                config[f"{PLUGIN_PREFIX}:{obj.external_id}"] = _serialize_config(obj)

        configurations.update(config)
        return {
            "configurations": configurations,
            "config_id": config_id,
            "context": context,
        }
