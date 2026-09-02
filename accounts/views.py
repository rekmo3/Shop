from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from main.models import Category


def login_view(request):
    if request.user.is_authenticated:
        return redirect('main:product_list')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('main:product_list')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('main:product_list')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:product_list')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('main:product_list')


@login_required
def profile_view(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'accounts/profile.html', context)