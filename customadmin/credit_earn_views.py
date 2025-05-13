from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CreditEarnHistory, CreditUsesHistory
from .forms import CreditEarnHistoryForm, CreditUsesHistoryForm
from django.contrib.auth.decorators import login_required, permission_required

# ===== Earn History CRUD =====
@login_required
@permission_required('auth.view_creditearnhistory', raise_exception=True)
def earn_list(request):
    earns = CreditEarnHistory.objects.all()
    return render(request, 'customadmin/credit_earn/earn_list.html', {'earns': earns})

@login_required
@permission_required('auth.delete_conadd_creditearnhistorytenttype', raise_exception=True)
def earn_create(request):
    form = CreditEarnHistoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('earn_list')
    return render(request, 'customadmin/credit_earn/earn_form.html', {'form': form})

@login_required
@permission_required('auth.change_creditearnhistory', raise_exception=True)
def earn_edit(request, pk):
    instance = get_object_or_404(CreditEarnHistory, pk=pk)
    form = CreditEarnHistoryForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('earn_list')
    return render(request, 'customadmin/credit_earn/earn_form.html', {'form': form})

@login_required
@permission_required('auth.delete_creditearnhistory', raise_exception=True)
@csrf_exempt
def earn_delete(request, pk):
    if request.method == 'DELETE':
        item = get_object_or_404(CreditEarnHistory, pk=pk)
        item.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)




# ===== Usage History CRUD =====
@login_required
@permission_required('auth.view_credituseshistory', raise_exception=True)
def usage_list(request):
    usages = CreditUsesHistory.objects.all()
    return render(request, 'customadmin/credit_earn/usage_list.html', {'usages': usages})

@login_required
@permission_required('auth.add_credituseshistory', raise_exception=True)
def usage_create(request):
    form = CreditUsesHistoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('usage_list')
    return render(request, 'customadmin/credit_earn/usage_form.html', {'form': form})

@login_required
@permission_required('auth.change_credituseshistory', raise_exception=True)
def usage_edit(request, pk):
    instance = get_object_or_404(CreditUsesHistory, pk=pk)
    form = CreditUsesHistoryForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('usage_list')
    return render(request, 'customadmin/credit_earn/usage_form.html', {'form': form})

@login_required
@permission_required('auth.delete_credituseshistory', raise_exception=True)
@csrf_exempt
def usage_delete(request, pk):
    if request.method == 'DELETE':
        item = get_object_or_404(CreditUsesHistory, pk=pk)
        item.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
