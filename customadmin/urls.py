from django.urls import path
from django.contrib.auth import views as auth_views
from .views import custom_admin_dashboard
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='customadmin/login.html'), name='login'),  # Custom login
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', custom_admin_dashboard, name='custom_admin_dashboard'),  # Custom dashboard
    path('users/', views.users_list, name='users_list'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/edit/<int:pk>/', views.edit_user, name='edit_user'),
    path('users/delete-user/<int:pk>/', views.delete_user, name='delete_user'),
]
