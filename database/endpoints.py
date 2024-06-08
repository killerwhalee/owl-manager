from django.urls import path

from database.views import ProblemViewSet


urlpatterns = [
    path(
        "",
        ProblemViewSet.as_view(
            {
                "get": "list_problems",
            }
        ),
    ),
    path(
        "<str:problem_id>",
        ProblemViewSet.as_view(
            {
                "get": "retrieve",
            }
        ),
    ),
]
