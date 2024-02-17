from django.urls import path
from django.contrib.auth import views as auth_views

from user import views

app_name = "user"

urlpatterns = [
    # Login/Logout
    path("login", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
    # Signup
    path("signup", views.user_signup, name="signup"),
    path("terms", views.terms, name="terms"),
    path("signup-success", views.user_signup_success, name="signup-success"),
    # User profile
    path("profile/<str:username>", views.user_profile, name="profile"),
]
