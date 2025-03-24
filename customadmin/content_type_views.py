from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from .forms import ContentTypeForm

# List ContentTypes
def content_type_list(request):
    content_types = ContentType.objects.all()
    return render(request, 'customadmin/content_type/list.html', {'content_types': content_types})

# Create ContentType
def content_type_create(request):
    if request.method == 'POST':
        form = ContentTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('content_type_list')
    else:
        form = ContentTypeForm()
    return render(request, 'customadmin/content_type/create.html', {'form': form})

# Edit ContentType
def content_type_edit(request, id):
    content_type = get_object_or_404(ContentType, id=id)
    if request.method == 'POST':
        form = ContentTypeForm(request.POST, instance=content_type)
        if form.is_valid():
            form.save()
            return redirect('content_type_list')
    else:
        form = ContentTypeForm(instance=content_type)
    return render(request, 'customadmin/content_type/edit.html', {'form': form, 'content_type': content_type})

# Delete ContentType
def content_type_delete(request, id):
    content_type = get_object_or_404(ContentType, id=id)
    content_type.delete()
    return redirect('content_type_list')
