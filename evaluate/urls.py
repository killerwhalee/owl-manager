from django.urls import path

from evaluate import views

app_name = "evaluate"

urlpatterns = [
    path("", lambda _: _, name="index"),
]
