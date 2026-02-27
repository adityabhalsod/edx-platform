"""
LTI External Configuration app.

Provides reusable LTI tool configurations by repurposing
the existing LtiConfiguration model (xblock-lti-consumer)
as templates via a proxy model and openedx-filters pipeline.
"""
default_app_config = "lms.djangoapps.lti_external_config.apps.LtiExternalConfigConfig"
