from django.urls import path
from django.contrib.auth import views as auth_views
from .views import custom_admin_dashboard
from . import permission_views
from . import views
from . import content_type_views
from . import auth_group_views
from .views import CustomPasswordResetView
from . import category_views
from . import document_views
from . import font_views
from . import credit_earn_views
from . import setting_views

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(template_name='customadmin/login.html'), name='login'),  # Custom login
    path('login/', views.login_view, name='admin-login'),
    path('admin-logout/', auth_views.LogoutView.as_view(next_page='/admin/login/'), name='admin-logout'),
    path('register/', views.register, name='admin-register'),
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

    path("password_reset/", views.forgot_password, name="password_reset"),
    path("password_reset/done/", views.mail_send_done, name="password_reset_done"),
    path('reset_admin_password/<uidb64>/<token>/', views.reset_password, name="password_reset_confirm"),
    # path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),


    path('categories/', category_views.category_list, name='category_list'),
    path('categories/create/', category_views.category_create, name='category_create'),
    path('categories/edit/<int:pk>/', category_views.category_edit, name='category_edit'),
    path('categories/delete/<int:pk>/', category_views.category_delete, name='category_delete'),



    path('documents/', document_views.document_list, name='document_list'),
    path('documents/add/', document_views.document_create, name='document_create'),
    path('documents/delete/<int:pk>/', document_views.document_delete, name='document_delete'),
    path('documents/letterhead-setup/<int:document_id>/', document_views.document_lhsetup, name='document_lhsetup'),


    path('fonts/', font_views.font_list, name='font_list'),
    path('fonts/create/', font_views.font_create, name='font_create'),
    path('fonts/edit/<int:pk>/', font_views.font_edit, name='font_edit'),
    path('fonts/delete/<int:pk>/', font_views.font_delete, name='font_delete'),


    path('credit-earn/', credit_earn_views.earn_list, name='earn_list'),
    path('credit-earn/create/', credit_earn_views.earn_create, name='earn_create'),
    path('credit-earn/edit/<int:pk>/', credit_earn_views.earn_edit, name='earn_edit'),
    path('credit-earn/delete/<int:pk>/', credit_earn_views.earn_delete, name='earn_delete'),

    # Usage History
    path('credit-usage/', credit_earn_views.usage_list, name='usage_list'),
    path('credit-usage/create/', credit_earn_views.usage_create, name='usage_create'),
    path('credit-usage/edit/<int:pk>/', credit_earn_views.usage_edit, name='usage_edit'),
    path('credit-usage/delete/<int:pk>/', credit_earn_views.usage_delete, name='usage_delete'),


    path('settings/', setting_views.setting_list, name='setting_list'),
    path('settings/create/', setting_views.setting_create, name='setting_create'),
    path('settings/<int:pk>/edit/', setting_views.setting_edit, name='setting_edit'),
    path('settings/<int:pk>/delete/', setting_views.setting_delete, name='setting_delete'),
]
