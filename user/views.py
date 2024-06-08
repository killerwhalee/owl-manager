from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import (
    AuthenticationFailed,
    ValidationError,
)

from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User
from user.forms import LoginForm, RegisterForm
from user.serializer import ProfileSerializer


class UserViewSet(viewsets.ViewSet):
    def get_authenticators(self):
        # Remove authenticator for `get_token`
        if self.action_map.get("post") == "get_token":
            return []
        return super().get_authenticators()

    def get_permissions(self):
        # Allow any request for `get_token`
        if self.action_map.get("post") == "get_token":
            return [AllowAny()]
        return super().get_permissions()

    def get_token(self, request):
        """
        Generate JWT token from access code of the OAuth provider

        """

        # Get data from post request
        user_email = request.data.get("user_email")
        user_password = request.data.get("user_password")

        # Try to login with given user_email and user_token
        try:
            user = User.objects.get(user_email=user_email)

            # Raise exception if password is not correct
            if not user.check_password(user_password):
                raise AuthenticationFailed(
                    detail="Failed to authenticate user with given credentials.",
                )

            # Raise exception if user is not active
            if not user.is_active:
                raise AuthenticationFailed(
                    detail="The account requested is currently inactive.",
                )

        except User.DoesNotExist:
            # Raise exception if user does not exist
            raise AuthenticationFailed(
                detail="Failed to authenticate user with given credentials.",
            )

        # Return access token for user if login has succeeded
        refresh = RefreshToken.for_user(user)

        return Response(
            data={"access": str(refresh.access_token), "refresh": str(refresh)},
            status=status.HTTP_200_OK,
        )
    
    def get_profile(self, request):
        serializer = ProfileSerializer(request.user.profile)

        return Response(serializer.data)

    def update_profile(self, request):
        serializer = ProfileSerializer(
            request.user.profile,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            raise ValidationError(detail=serializer.errors)

        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user_email = form.cleaned_data["user_email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, user_email=user_email, password=password)

            if user is not None:
                login(request, user)
                return redirect("/")

            else:
                form.add_error(None, "Invalid email or password.")

    else:
        form = LoginForm()

    context = {"form": form}
    return render(request, "user/login.html", context)


def user_logout(request):
    logout(request)
    return redirect("/")


def user_signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            # Save User Data
            form.save()

            # Authenticate User
            user_email = form.cleaned_data.get("user_email")
            raw_password = form.cleaned_data.get("password1")
            authenticate(user_email=user_email, password=raw_password)

            return redirect("user:signup-success")

        else:
            print(form.errors)

    else:
        form = RegisterForm()

    context = {"form": form}
    return render(request, "user/signup.html", context)


def user_signup_success(request):
    return render(request, "user/signup-success.html")


@login_required(login_url="user:login")
def user_profile(request):
    user = User.objects.get(id=request.user.id)
    context = {"user": user}

    return render(request, "user/profile.html", context)
