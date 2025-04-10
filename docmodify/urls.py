from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import CustomPasswordResetView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.hello_there, name='hello_there'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.public_dashboard, name='public_dashboard'),
    path('redirect/', views.role_based_redirect, name='role_based_redirect'),
    path('login/', views.public_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    
    # Email verification URLs
    path('verify-email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    path('verification-sent/', views.verification_sent, name='verification_mail_sent'),
    path('resend-verification/', views.resend_verification_email, name='resend_verification'),
]