from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .forms import SignUpForm, LoginForm

def login_signup(request):
    if request.method == 'POST':
        if 'signup' in request.POST:
            signup_form = SignUpForm(request.POST)
            login_form = LoginForm()
            if signup_form.is_valid():
                signup_form.save()
                username = signup_form.cleaned_data.get('username')
                raw_password = signup_form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('dashboard')  # Change 'dashboard' to your target route
        else:
            login_form = LoginForm(request, data=request.POST)
            signup_form = SignUpForm()
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('dashboard')  # Change 'dashboard' to your target route
    else:
        signup_form = SignUpForm()
        login_form = LoginForm()

    return render(request, 'accounts/login_signup.html', {
        'signup_form': signup_form,
        'login_form': login_form
    })

