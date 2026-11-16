from django.urls import path
from .views import UserRegisterView,UserLoginView,UserLogoutView,OTPVerifyView

urlpatterns = [
    path('register/',UserRegisterView.as_view(),name='register'),
    path('verify_otp/',OTPVerifyView.as_view(),name='verify-otp'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
]
