from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import UserCreationForm, EditUser
# Create your views here.

def home_view(request, *args, **kwargs):
    return render(request, "home.html", {})

def register_view(request, *args, **kwargs):
	form = UserCreationForm(request.POST)
	if form.is_valid():
		form.save()
		return redirect('login')
	else:
		form = UserCreationForm()
	return render(request, "register.html", {'form' : form})

def edit_user_view(request, *args, **kwargs):
    form = EditUser(data=request.POST, instance = request.user)
    if form.is_valid():
        form.save()
        return redirect('profile')
    return render(request, "edit_user.html", {'form' : form})

def change_password_view(request, *args, **kwargs):
    form = PasswordChangeForm(data = request.POST, user = request.user)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, "change_password.html", {'form' : form})

def profile_view(request, *args, **kwargs):
	return render(request, "profile.html", {})

def login_view(request, *args, **kwargs):
	form = AuthenticationForm(data=request.POST)
	if form.is_valid():
		login(request, form.get_user())
		return redirect('profile')
	else:
		form = AuthenticationForm()
	return render(request, "login.html", {'form' : form})

def logout_view(request, *args, **kwargs):
	logout(request)
	return render(request, "logged_out.html", {})
