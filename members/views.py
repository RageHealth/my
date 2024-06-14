from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import UserLoginForm, MyForm, UserRegistrationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from blog.models import Post

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

def profile_view(request, username):
    user_profile = User.objects.filter(username=username).prefetch_related('profile').first()
    if user_profile is None:
        return redirect('main:index')

    user_posts = Post.objects.filter(author_id=user_profile)
    is_following = request.user.profile.is_following(user_profile.profile) if request.user.is_authenticated else False
    podpiski = user_profile.profile.get_followers().count()
    podpisciki = user_profile.profile.get_following().count()

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile.profile)
        if form.is_valid():
            if user_profile != request.user:
                return redirect('main:index')
            form.save()
        else:
            print(form.errors)
    else:
        form = ProfileForm(instance=user_profile.profile)

    return render(request, 'registration/profile.html', {
        'profile': user_profile.profile,
        'form': form,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'kol': len(user_posts),
        'is_following': is_following,
        'podpiski': podpiski,
        'podpisciki': podpisciki,
        'followers': user_profile.profile.get_followers(),
        'following': user_profile.profile.get_following(),
    })

def logout_view(request):
    logout(request)
    return redirect('main:index')

def my_view(request):
    form = MyForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def follow_view(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.user != profile.user:
        user_profile = request.user.profile
        if user_profile.is_following(profile):
            user_profile.unfollow(profile)
            messages.success(request, 'Unfollow {}'.format(profile.user.username))
        else:
            user_profile.follow(profile)
            messages.success(request, 'Follow {}'.format(profile.user.username))
    return redirect('members:profile', username=profile.user.username)


