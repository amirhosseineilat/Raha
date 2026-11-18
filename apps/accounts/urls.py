from django.urls import path
from .views import (
    UserRegisterView, UserLoginView, UserLogoutView, OTPVerifyView,
    UserResetPassword, RahaPasswordResetDoneView,
    RahaPasswordResetConfirmView, RahaPasswordResetCompleteView,
    UserProfileView, RahaPasswordChangeView,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("verify_otp/", OTPVerifyView.as_view(), name="verify-otp"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("password-change/", RahaPasswordChangeView.as_view(), name="password_change"),
    path("password-reset/", UserResetPassword.as_view(), name="password_reset"),
    path("password-reset/done/", RahaPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password-reset/<uidb64>/<token>/", RahaPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password-reset/complete/", RahaPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
