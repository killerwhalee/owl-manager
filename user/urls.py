from django.urls import path

from user import views

app_name = "user"

urlpatterns = [
    # Authentication
    path("login", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
    path("signup", views.user_signup, name="signup"),
    path("signup-success", views.user_signup_success, name="signup-success"),
    # User profile
    path("profile/<str:username>", views.user_profile, name="profile"),
]
