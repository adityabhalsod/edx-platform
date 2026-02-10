"""
Django Admin registration for User Profiles.
"""

from django.contrib import admin

from cms.djangoapps.user_profiles.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin for UserProfile model."""

    list_display = ("user", "city", "country", "phone_number", "created_at")
    search_fields = ("user__username", "user__email", "city", "country")
    list_filter = ("country",)
    raw_id_fields = ("user",)
