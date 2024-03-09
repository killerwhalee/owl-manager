from django.urls import path

from tools import views

app_name = "tools"

urlpatterns = [
    path("", views.index, name="index"),
    path("image-cutter", views.image_cutter, name="image-cutter"),
]
