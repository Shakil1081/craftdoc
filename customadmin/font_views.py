from django.shortcuts import render, get_object_or_404, redirect
from .models import Font
from .forms import FontForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required


@login_required
@permission_required('auth.view_font', raise_exception=True)
def font_list(request):
    fonts = Font.objects.all()
    return render(request, 'customadmin/font/font_list.html', {'fonts': fonts})


@login_required
@permission_required('auth.add_font', raise_exception=True)
def font_create(request):
    if request.method == 'POST':
        form = FontForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('font_list')
    else:
        form = FontForm()
    return render(request, 'customadmin/font/font_create.html', {'form': form})


@login_required
@permission_required('auth.change_font', raise_exception=True)
def font_edit(request, pk):
    font = get_object_or_404(Font, pk=pk)
    if request.method == 'POST':
        form = FontForm(request.POST, instance=font)
        if form.is_valid():
            form.save()
            return redirect('font_list')
    else:
        form = FontForm(instance=font)
    return render(request, 'customadmin/font/font_edit.html', {'form': form, 'font': font})


@login_required
@permission_required('auth.delete_font', raise_exception=True)
def font_delete(request, pk):
    font = get_object_or_404(Font, pk=pk)
    font.delete()
    return JsonResponse({'status': 'success'})
