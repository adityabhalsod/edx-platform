"""
User Profiles Application Configuration.
"""

from django.apps import AppConfig
from edx_django_utils.plugins import PluginURLs

from openedx.core.djangoapps.plugins.constants import ProjectType


class UserProfilesConfig(AppConfig):
    """
    Application Configuration for User Profiles.
    """

    name = "lms.djangoapps.user_profiles"
    verbose_name = "User Profiles"

    plugin_app = {
        PluginURLs.CONFIG: {
            ProjectType.LMS: {
                PluginURLs.NAMESPACE: "user_profiles",
                PluginURLs.REGEX: r"^api/user_profiles/",
                PluginURLs.RELATIVE_PATH: "urls",
            }
        },
    }
