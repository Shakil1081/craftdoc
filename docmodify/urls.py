from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

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

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path("password_reset/done/", views.mail_send_done, name="password_reset_mail_done"),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),



    path('letterhead/26', views.letterhead, name='letterhead'),

    path('credit-earn', views.earn_credit, name='earn_credit'),
    path('credit-earn-history', views.credit_earn_history, name='credit_earn_history'),
    path('credit-uses-history', views.credit_uses_history, name='credit_uses_history'),

    path('letterhead/5', views.letterhead, name='letterhead'),
]