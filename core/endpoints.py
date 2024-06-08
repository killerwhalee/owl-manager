from django.urls import path, include


urlpatterns = [
    path("database/", include("database.endpoints")),
    path("user/", include("user.endpoints")),
]
