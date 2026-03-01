from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
import jwt
from django.utils import timezone
from datetime import datetime, timedelta, timezone as dt_timezone
from django.conf import settings
from accounts.models import User, PasswordReset
from functools import wraps
# Create your views here.

JWT_COOKIE_NAME = "access_token"

def _build_jwt_token(user):
    payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.now(dt_timezone.utc) + timedelta(hours=1),
        "iat": datetime.now(dt_timezone.utc),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

def _decode_jwt_token(token):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

def jwt_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.COOKIES.get(JWT_COOKIE_NAME)

        if not token:
            messages.error(request, "Please login to continue")
            return redirect("login")

        try:
            payload = _decode_jwt_token(token)
            request.jwt_user = User.objects.get(id=payload["user_id"])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            messages.error(request, "Session expired. Please login again")
            response = redirect("login")
            response.delete_cookie(JWT_COOKIE_NAME)
            return response

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def RegisterView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful, You are Logged In')
            response = redirect('home')
            response.set_cookie(JWT_COOKIE_NAME, _build_jwt_token(user))
            return response
    else:
        form = RegisterForm()
        messages.error(request, 'Registration failed. Please correct the errors below.')

    return render(request, 'register.html', {'form': form})

def LoginView(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful')

            response = redirect('home')
            response.set_cookie(JWT_COOKIE_NAME, _build_jwt_token(user))
            return response
        

    else:
        form = AuthenticationForm()
        messages.error(request, 'Login failed. Please check your username and password.')

    return render(request, "login.html", {"form": form})

@jwt_login_required
def LogoutView(request):
    response = redirect('login')
    response.delete_cookie(JWT_COOKIE_NAME)
    return response

from django.urls import reverse
from django.core.mail import EmailMessage

def ForgotPassword(request):

    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)

            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url = reverse(
                "reset-password", kwargs={"reset_id": new_password_reset.reset_id}
            )

            full_password_reset_url = (
                f"{request.scheme}://{request.get_host()}{password_reset_url}"
            )
            email_body = (
                f"Reset your password using the link below:\n\n\n{full_password_reset_url}"
            )
            email_message = EmailMessage(
                "Password Reset Request",
                email_body,
                settings.EMAIL_HOST_USER, 
                [email],
            )
            email_message.fail_silently = True
            email_message.send()
            return redirect("password-reset-sent", reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect("forgot-password")

    return render(request, "forgotpassword.html")

def PasswordResetSent(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, "resetpasswordsend.html")

    messages.error(request, "Invalid reset id")
    return redirect("forgot-password")


def ResetPassword(request, reset_id):
    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == "POST":
            password = request.POST.get("password")
            confirm_password = request.POST.get("password1")

            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, "Passwords do not match")

            if len(password) < 5:
                passwords_have_error = True
                messages.error(request, "Password must be at least 5 characters long")

            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                passwords_have_error = True
                
                messages.error(request, "Reset link has expired")

                password_reset_id.delete()

            if not passwords_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()

                password_reset_id.delete()
                messages.success(request, "Password reset. Proceed to login")
                return redirect("login")

            return redirect("reset-password", reset_id=reset_id)

    except PasswordReset.DoesNotExist:
        
        messages.error(request, "Invalid reset id")
        return redirect("forgot-password")

    return render(request, "resetpassword.html")