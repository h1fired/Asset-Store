from django.urls import path, include
from . import views

urlpatterns = [
    path('verify/', views.verify_account_view, name='otp_verify'),
    path('verify/resend', views.resend_otp_view, name='otp_resend'),
]
