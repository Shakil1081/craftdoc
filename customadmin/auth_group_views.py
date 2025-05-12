from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import Group, Permission
from .forms import GroupForm  
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required

# List View for Groups
@login_required
@permission_required('auth.view_group', raise_exception=True)
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'customadmin/auth_group/group_list.html', {'groups': groups})

# Create View for Group
@login_required
@permission_required('auth.add_group', raise_exception=True)
def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)  # Save group without permissions first
            group.save()
            form.save_m2m()  # Save the many-to-many field (permissions)
            messages.success(request, "Group created successfully with permissions.")
            return redirect('group_list')
    else:
        form = GroupForm()
    
    return render(request, 'customadmin/auth_group/create.html', {'form': form})

# Edit View for Group
@login_required
@permission_required('auth.change_group', raise_exception=True)
def group_edit(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            group = form.save()  # Save the group name update

            # Update permissions
            selected_permissions = request.POST.getlist('permissions')  # Get selected permissions
            group.permissions.set(selected_permissions)  # Update group permissions

            messages.success(request, "Group updated successfully.")
            return redirect('group_list')
    else:
        form = GroupForm(instance=group)

    permissions = Permission.objects.all()  # Fetch all permissions
    selected_permissions = group.permissions.all()  # Get currently assigned permissions

    return render(request, 'customadmin/auth_group/edit.html', {
        'form': form,
        'group': group,
        'permissions': permissions,
        'selected_permissions': selected_permissions
    })

@login_required
@permission_required('auth.view_group', raise_exception=True)
def group_view(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'customadmin/auth_group/view.html', {'group': group})

# Delete View for Group
@login_required
@permission_required('auth.delete_group', raise_exception=True)
def group_delete(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    group.permissions.clear()

    group.delete()
    messages.success(request, "Group deleted successfully.")

    return JsonResponse({"success": True})

