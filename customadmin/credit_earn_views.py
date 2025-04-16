from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CreditEarnHistory, CreditUsesHistory
from .forms import CreditEarnHistoryForm, CreditUsesHistoryForm

# ===== Earn History CRUD =====
def earn_list(request):
    earns = CreditEarnHistory.objects.all()
    return render(request, 'customadmin/credit_earn/earn_list.html', {'earns': earns})

def earn_create(request):
    form = CreditEarnHistoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('earn_list')
    return render(request, 'customadmin/credit_earn/earn_form.html', {'form': form})

def earn_edit(request, pk):
    instance = get_object_or_404(CreditEarnHistory, pk=pk)
    form = CreditEarnHistoryForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('earn_list')
    return render(request, 'customadmin/credit_earn/earn_form.html', {'form': form})

@csrf_exempt
def earn_delete(request, pk):
    if request.method == 'DELETE':
        item = get_object_or_404(CreditEarnHistory, pk=pk)
        item.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)




# ===== Usage History CRUD =====
def usage_list(request):
    usages = CreditUsesHistory.objects.all()
    return render(request, 'customadmin/credit_earn/usage_list.html', {'usages': usages})

def usage_create(request):
    form = CreditUsesHistoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('usage_list')
    return render(request, 'customadmin/credit_earn/usage_form.html', {'form': form})

def usage_edit(request, pk):
    instance = get_object_or_404(CreditUsesHistory, pk=pk)
    form = CreditUsesHistoryForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('usage_list')
    return render(request, 'customadmin/credit_earn/usage_form.html', {'form': form})

@csrf_exempt
def usage_delete(request, pk):
    if request.method == 'DELETE':
        item = get_object_or_404(CreditUsesHistory, pk=pk)
        item.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
