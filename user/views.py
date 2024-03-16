from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from user.forms import LoginForm, RegisterForm
from user.models import User


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
