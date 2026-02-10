"""
Models for the User Profiles app.
"""

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UserProfile(models.Model):
    """
    Extended user profile with additional personal information.

    .. no_pii:
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="extended_profile",
    )
    bio = models.TextField(blank=True, default="")
    avatar_url = models.URLField(max_length=500, blank=True, default="")
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, default="")
    city = models.CharField(max_length=100, blank=True, default="")
    country = models.CharField(max_length=100, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "user_profiles"
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"Profile for {self.user.username}"
