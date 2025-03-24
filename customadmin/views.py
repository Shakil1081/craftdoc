from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import UserForm
from django.contrib import messages
from django.http import JsonResponse
from rolepermissions.decorators import has_permission_decorator
# from rolepermissions.checkers import has_permission
from django.contrib.auth.models import Permission, Group
from django.core.exceptions import PermissionDenied

@login_required
def custom_admin_dashboard(request):
    return render(request, 'customadmin/index.html')


@login_required
def users_list(request):
    # Check if the user has the required permission
    if not request.user.has_perm('customadmin.view_user'):
        raise PermissionDenied  # Return a 403 Forbidden error if they lack permission

    users = User.objects.filter(is_superuser=False)
    return render(request, 'customadmin/user/users_list.html', {'users': users})


@login_required
def create_user(request):
    if not request.user.has_perm('customadmin.add_user'):
        raise PermissionDenied 

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # Assign selected groups to user
            selected_groups = request.POST.getlist('groups')  # List of selected group IDs
            user.groups.set(Group.objects.filter(id__in=selected_groups))

            # After assigning groups, ensure the user has the necessary permissions from the groups
            for group in user.groups.all():
                for perm in group.permissions.all():
                    user.user_permissions.add(perm)

            user.save()
            messages.success(request, "User created successfully!")
            return redirect('users_list')
    else:
        form = UserForm()
        groups = Group.objects.all()  # Fetch all groups to display in the form

    return render(request, 'customadmin/user/create_user.html', {'form': form, 'groups': groups})


@login_required
def edit_user(request, pk):
    if not request.user.has_perm('customadmin.edit_user'):
        raise PermissionDenied 
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # Ensure password is not reset if left empty
            if not form.cleaned_data.get('password'):
                form.cleaned_data.pop('password', None)

            form.save()
            messages.success(request, "User updated successfully!")
            return redirect('users_list')
    else:
        form = UserForm(instance=user)

    return render(request, 'customadmin/user/edit_user.html', {'form': form, 'user': user})

@login_required
def delete_user(request, pk):
    if not request.user.has_perm('customadmin.delete_user'):
        raise PermissionDenied 
    if request.method == 'DELETE':
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'status': 'failed'}, status=400)