from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def Home(request):
    return render(request, 'home.html')

def RegisterView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful, You are Logged In')
            return redirect('home')
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
            return redirect('home')

    else:
        form = AuthenticationForm()
        messages.error(request, 'Login failed. Please check your username and password.')

    return render(request, "login.html", {"form": form})

def LogoutView(request):
    logout(request)
    return redirect('home')
