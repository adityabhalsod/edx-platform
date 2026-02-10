"""URLs for User Profiles API."""

from django.urls import path

from cms.djangoapps.user_profiles.v1.views import UserProfileListView

urlpatterns = [
    path("v1/", UserProfileListView.as_view(), name="user-profile-list"),
]
