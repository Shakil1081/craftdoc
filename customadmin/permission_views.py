from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Permission, ContentType
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.http import JsonResponse

@login_required
@permission_required('auth.view_permission', raise_exception=True)
def permission_list(request):
    """ List all permissions """
    permissions = Permission.objects.all()
    return render(request, "customadmin/permission/list.html", {"permissions": permissions})

@login_required
@permission_required('auth.add_permission', raise_exception=True)
def permission_create(request):
    """ Create a new permission """
    content_types = ContentType.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        codename = request.POST.get('codename')
        content_type_id = request.POST.get('content_type')
        content_type = ContentType.objects.get(id=content_type_id)

        # Create the permission
        Permission.objects.create(name=name, codename=codename, content_type=content_type)
        return redirect(reverse("permission_list"))

    return render(request, "customadmin/permission/create.html", {"content_types": content_types})

@login_required
@permission_required('auth.change_permission', raise_exception=True)
def permission_update(request, pk):
    """ Update an existing permission """
    permission = get_object_or_404(Permission, pk=pk)
    content_types = ContentType.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        codename = request.POST.get('codename')
        content_type_id = request.POST.get('content_type')
        content_type = ContentType.objects.get(id=content_type_id)

        permission.name = name
        permission.codename = codename
        permission.content_type = content_type
        permission.save()

        return redirect(reverse("permission_list"))

    return render(request, "customadmin/permission/edit.html", {"permission": permission, "content_types": content_types})

@login_required
@permission_required('auth.delete_permission', raise_exception=True)
def permission_delete(request, pk):
    permission = get_object_or_404(Permission, pk=pk)
    
    if request.method == 'DELETE':
        permission.delete()
        return JsonResponse({'status': 'success'}, status=200)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

