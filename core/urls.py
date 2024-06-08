from django.contrib import admin
from django.urls import path, re_path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # System/Root Application
    path("admin/", admin.site.urls),
    # Home Redirection
    path("", lambda _: redirect("home/")),
    # API Endpoints
    re_path(r"^v1/", include("core.endpoints")),
    # Application Routing
    re_path(r"^home/", include("home.urls")),
    re_path(r"^user/", include("user.urls")),
    re_path(r"^evaluate/", include("evaluate.urls")),
    re_path(r"^tools/", include("tools.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
