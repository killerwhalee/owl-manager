from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from user.views import UserViewSet

urlpatterns = [
    path(
        "token",
        UserViewSet.as_view({"post": "get_token"}),
    ),
    path(
        "token/refresh",
        TokenRefreshView.as_view(),
    ),
    path(
        "profile",
        UserViewSet.as_view(
            {
                "get": "get_profile",
                "patch": "update_profile",
            }
        ),
    ),
]
