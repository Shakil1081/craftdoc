# customadmin/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Category
from .forms import CategoryForm

# View to list categories
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'customadmin/category/category_list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)

            # Ensure category_level is correctly assigned
            if category.parent:
                category.category_level = category.parent.category_level + 1
            else:
                category.category_level = 1

            category.save()
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'customadmin/category/category_create.html', {'form': form})

# View to edit a category
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'customadmin/category/category_edit.html', {'form': form, 'category': category})

# View to delete a category (AJAX)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return JsonResponse({'status': 'success'})
