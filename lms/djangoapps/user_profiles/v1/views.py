"""
API views for User Profiles.
"""

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from lms.djangoapps.user_profiles.models import UserProfile
from lms.djangoapps.user_profiles.v1.serializers import UserProfileSerializer


class UserProfilePagination(PageNumberPagination):
    """Pagination for user profiles list."""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class UserProfileListView(ListAPIView):
    """
    API endpoint that returns a paginated list of user profiles.

    **Example Request**

        GET /api/user_profiles/v1/

    **Response**

        200 OK with paginated list of user profiles.
    """

    queryset = UserProfile.objects.select_related("user").all().order_by("-created_at")
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = UserProfilePagination
