from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import Register_Form


def register(request):
    if request.user.is_authenticated:
        return redirect('Authentication:dashboard')

    form = Register_Form(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Your account is ready.')
        return redirect('Authentication:dashboard')

    return render(request, 'Authentication/register.html', {'form': form})



@login_required
def dashboard(request):
    return render(request, 'Authentication/dashboard.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username= username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You logged in successfully!')
            return redirect('Authentication:dashboard')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'Authentication/login.html')

# @require_POST
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been signed out.')
    return redirect('Authentication:login_view')
