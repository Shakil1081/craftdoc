from django.urls import path
from django.contrib.auth import views as auth_views
from .views import custom_admin_dashboard
from . import permission_views
from . import views
from . import content_type_views
from . import auth_group_views
from . import category_views

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(template_name='customadmin/login.html'), name='login'),  # Custom login
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
     path('verification-sent/', views.verification_sent, name='verification_sent'),
    # path('resend-verification-email/', views.resend_verification_email, name='resend_verification_email'),
    path('', custom_admin_dashboard, name='custom_admin_dashboard'),  
    path('profile/edit/', views.edit_profile, name='profile_edit'),
    path('users/', views.users_list, name='users_list'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/edit/<int:pk>/', views.edit_user, name='edit_user'),
    path('users/delete-user/<int:pk>/', views.delete_user, name='delete_user'),



    path("permission/", permission_views.permission_list, name="permission_list"),
    path("permission/create/", permission_views.permission_create, name="permission_create"),
    path("permission/edit/<int:pk>/", permission_views.permission_update, name="permission_update"),
    path("permission/delete/<int:pk>/", permission_views.permission_delete, name="permission_delete"),
    

    path('content-type/', content_type_views.content_type_list, name='content_type_list'),
    path('content-type/create/', content_type_views.content_type_create, name='content_type_create'),
    path('content-type/edit/<int:id>/', content_type_views.content_type_edit, name='content_type_edit'),
    path('content-type/delete/<int:id>/', content_type_views.content_type_delete, name='content_type_delete'),


    path('group/', auth_group_views.group_list, name='group_list'),
    path('group/create/', auth_group_views.group_create, name='group_create'),
    path('group/edit/<int:group_id>/', auth_group_views.group_edit, name='group_edit'),
    path('groups/view/<int:group_id>/', auth_group_views.group_view, name='group_view'),
    path('group/delete/<int:group_id>/', auth_group_views.group_delete, name='group_delete'),

    
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),


    path('categories/', category_views.category_list, name='category_list'),
    path('categories/create/', category_views.category_create, name='category_create'),
    path('categories/edit/<int:pk>/', category_views.category_edit, name='category_edit'),
    path('categories/delete/<int:pk>/', category_views.category_delete, name='category_delete'),
]
