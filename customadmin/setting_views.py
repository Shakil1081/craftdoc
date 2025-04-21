from django.shortcuts import render, get_object_or_404, redirect
from .models import Setting
from .forms import SettingForm  # You'll create this form below
from django.core.paginator import Paginator
from django.contrib import messages

# List all settings
def setting_list(request):
    settings = Setting.objects.all().order_by('id')
    paginator = Paginator(settings, 10)  # Show 10 settings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'settings/list.html', {'page_obj': page_obj})

# Create a setting
def setting_create(request):
    if request.method == 'POST':
        form = SettingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Setting Created successfully!")
            return redirect('setting_list')
    else:
        form = SettingForm()
    return render(request, 'settings/form.html', {'form': form, 'title': 'Create Setting'})

# Edit a setting
def setting_edit(request, pk):
    setting = get_object_or_404(Setting, pk=pk)
    if request.method == 'POST':
        form = SettingForm(request.POST, instance=setting)
        if form.is_valid():
            form.save()
            messages.success(request, "Setting Updated successfully!")
            return redirect('setting_list')
    else:
        form = SettingForm(instance=setting)
    return render(request, 'settings/form.html', {'form': form, 'title': 'Edit Setting'})

# Delete a setting
def setting_delete(request, pk):
    setting = get_object_or_404(Setting, pk=pk)
    if request.method == 'POST':
        setting.delete()
        messages.warning(request, "Setting Deleted successfully!")
        return redirect('setting_list')
