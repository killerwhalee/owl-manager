from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # System/Root Application
    path("admin/", admin.site.urls),
    # Home Redirection
    path("", lambda _: redirect("home/")),
    # General Purpose Application
    path("home/", include("home.urls")),
    path("user/", include("user.urls")),
    # User Purpose Application
    path("evaluate/", include("evaluate.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
