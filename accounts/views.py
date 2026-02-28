from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def Home(request):
    return render(request, 'home.html')

def RegisterView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            
            form.save()
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def LoginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Perform login logic here
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']    
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def LogoutView(request):
    logout(request)
    return redirect('home')
