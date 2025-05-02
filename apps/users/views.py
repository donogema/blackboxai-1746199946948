from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, UserLoginForm, CustomUserChangeForm
from .models import CustomUser

def login_view(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')
        
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('users:dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('users:login')

@login_required
@user_passes_test(lambda u: u.is_super_admin())
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}!')
            return redirect('users:user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def dashboard(request):
    context = {
        'user': request.user,
    }
    return render(request, 'users/dashboard.html', context)

@login_required
@user_passes_test(lambda u: u.is_admin())
def user_list(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'users/user_list.html', {'users': users})

@login_required
@user_passes_test(lambda u: u.is_admin())
def edit_user(request, pk):
    user = CustomUser.objects.get(pk=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account updated for {user.username}!')
            return redirect('users:user_list')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'users/edit_user.html', {'form': form, 'user': user})

@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('users:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})
