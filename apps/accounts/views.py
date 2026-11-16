from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .forms import UserRegisterForm,UserLoginForm,PasswordResetForm
from django.contrib.auth.views import LoginView,LogoutView, PasswordResetView
from django.urls import reverse_lazy
from .services import send_otp_email
from .models import Otp

class UserRegisterView(CreateView):
    template_name = 'accounts/user_register.html'
    form_class = UserRegisterForm

    def form_valid(self, form):
        # here we create a user with is_active=False then we verify the. user with an otp
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # here we generate a otp code and store it in database and send an email to user to verify it
        send_otp_email(user)

        self.request.session['pending_user_id'] = user.pk

        return redirect('verify-otp')

class OTPVerifyView:
    pass

class UserLoginView(LoginView):
    template_name = 'accounts/user_loing.html'
    form_class = UserLoginForm

class UserLogoutView(LogoutView):
    next_page = reverse_lazy("landing")

class UserResetPassword(PasswordResetView):
    form_class = PasswordResetForm
