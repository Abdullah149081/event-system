from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from users.forms import LoginForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch


def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
            else:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data.get("password1"))
                user.is_active = False
                user.save()

                messages.success(
                    request,
                    f"Account created for {user.username}! Please check your email to activate your account.",
                )
                return redirect("sign_in")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, "auth/signUp.html", {"form": form})


def sign_in(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                login(request, user)
                messages.success(request, "Welcome back!")
                return redirect("/")
            else:
                messages.error(
                    request,
                    "Your account is not activated. Please check your email for the activation link.",
                )
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, "auth/login.html", {"form": form})


def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(
                request,
                "Your account has been activated successfully! You can now log in.",
            )
        else:
            messages.error(request, "Invalid activation link.")
    except User.DoesNotExist:
        messages.error(request, "Invalid activation link.")

    return redirect("sign_in")


@login_required
def sign_out(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("/")
