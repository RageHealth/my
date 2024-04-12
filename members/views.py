from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import UserLoginForm
from .forms import UserRegistrationForm

from .models import Profile
from .forms import ProfileForm

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:index') 
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('members:login')  
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})

def user_profile(request, username):
    user_profile = User.objects.filter(username=username).prefetch_related('profile').first()
    if user_profile is None:
        return redirect('main:index')
    # prefetch_related() це метод, який дозволяє здійснити запит до бази даних, щоб отримати всі дані про профіль користувача
    # тобто виконується всьо один запит до бази даних, а не два окремих

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile.profile)
        if form.is_valid():
            if user_profile != request.user:
                return redirect('main:index')
            form.save()
    else:
        form = ProfileForm(instance=user_profile.profile)
    
    return render(request, 'registration/profile.html', {'profile': user_profile.profile, 'form': form, 'user_profile': user_profile})


def logout_view(request):
    logout(request)
    return redirect('main:index')