from django.urls import path

from evaluate import views

app_name = "evaluate"

urlpatterns = [
    path("", views.eval_request, name="request"),
]
