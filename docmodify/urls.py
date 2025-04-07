from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from . import document_view

urlpatterns = [
    path('', views.hello_there, name='hello_there'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.public_dashboard, name='public_dashboard'),
    path('redirect/', views.role_based_redirect, name='role_based_redirect'),
    path('login/', views.public_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),

    path('create-letterhead/', document_view.createLetterhead, name='create_letterhead'),
    
]
