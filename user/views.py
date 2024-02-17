from django.contrib.auth import authenticate, login, logout
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


def terms(request):
    return render(request, "user/terms.html")


def user_profile(request, username):
    user = User.objects.get(username=username)
    context = {"user": user}
    return render(request, "user/profile.html", context)


# Views for Error Handling
def error400(request, exception):
    return render(request, "error/400.html", {})


def error403(request, exception):
    return render(request, "error/403.html", {})


def error404(request, exception):
    return render(request, "error/404.html", {})


def error500(request):
    return render(request, "error/500.html", {})


def error502(request):
    return render(request, "error/502.html", {})


def error503(request):
    return render(request, "error/503.html", {})
