from django.shortcuts import render
from django.views.generic import CreateView
from .forms import UserCreationForm,UserLoginForm
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy

class UserRegisterView(CreateView):
    template_name = 'accounts/user_register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('home')

class UserLoginView(LoginView):
    template_name = 'accounts/user_loing.html'
    form_class = UserLoginForm

class UserLogoutView(LogoutView):
    next_page = reverse_lazy("landing")
