from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import UserForm
from django.contrib import messages
from django.http import JsonResponse
from rolepermissions.decorators import has_permission_decorator
from rolepermissions.checkers import has_permission

@login_required
def custom_admin_dashboard(request):
    return render(request, 'customadmin/index.html')


@login_required
@has_permission_decorator('view_users')
def users_list(request):
    users = User.objects.all()
    return render(request, 'customadmin/user/users_list.html', {'users': users})

@login_required
@has_permission_decorator('add_user')
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully!")
            return redirect('users_list')
    else:
        form = UserForm()

    return render(request, 'customadmin/user/create_user.html', {'form': form})

@login_required
@has_permission_decorator('edit_user')
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully!")
            return redirect('users_list')
    else:
        form = UserForm(instance=user)

    return render(request, 'customadmin/user/edit_user.html', {'form': form, 'user': user})

@login_required
@has_permission_decorator('delete_user')
def delete_user(request, pk):
    if request.method == 'DELETE':
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'status': 'failed'}, status=400)