from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, FormView
from .forms import UserRegisterForm, UserLoginForm, PasswordResetForm, OTPVerifyForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.urls import reverse_lazy
from .services import send_otp_email
from .models import Otp
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


class UserRegisterView(CreateView):
    template_name = "accounts/user_register.html"
    form_class = UserRegisterForm

    def form_valid(self, form):
        # here we create a user with is_active=False then we verify the. user with an otp
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # here we generate a otp code and store it in database and send an email to user to verify it
        send_otp_email(user)

        self.request.session["pending_user_id"] = user.pk

        return redirect("verify-otp")


class OTPVerifyView(FormView):
    form_class = OTPVerifyForm
    template_name = "accounts/verifyotp.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):

        user_id = self.request.session.get("pending_user_id")

        if not user_id:
            return redirect("landing")

        user = get_object_or_404(
            User,
            pk=user_id,
            is_active=False,
        )

        user_input = form.cleaned_data["otp"]

        with transaction.atomic():

            otp = (
                Otp.objects
                .select_for_update()
                .filter(user=user, is_used=False)
                .order_by("-created_at")
                .first()
            )

            if otp is None:
                form.add_error(
                    "otp",
                    "کد تأییدی برای این حساب پیدا نشد."
                )
                return self.form_invalid(form)

            if otp.is_expired:
                form.add_error(
                    "otp",
                    "کد تأیید منقضی شده است."
                )
                return self.form_invalid(form)

            if otp.attempts >= 5:
                form.add_error(
                    "otp",
                    "تعداد تلاش‌های مجاز به پایان رسیده است."
                )
                return self.form_invalid(form)

            if not check_password(user_input, otp.code_hash):

                otp.attempts += 1

                if otp.attempts >= 5:
                    otp.is_used = True

                otp.save(
                    update_fields=["attempts", "is_used"]
                )

                if otp.is_used:
                    form.add_error(
                        "otp",
                        "تعداد تلاش‌های مجاز به پایان رسیده است."
                    )
                else:
                    form.add_error(
                        "otp",
                        "کد وارد شده صحیح نیست."
                    )

                return self.form_invalid(form)

            otp.is_used = True
            otp.save(update_fields=["is_used"])

            user.is_active = True
            user.save(update_fields=["is_active"])

        self.request.session.pop("pending_user_id", None)

        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = "accounts/user_loing.html"
    form_class = UserLoginForm


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("landing")


class UserResetPassword(PasswordResetView):
    form_class = PasswordResetForm
