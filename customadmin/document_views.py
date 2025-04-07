# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Document
from .forms import DocumentForm, DocumentMetaFormSet, DocumentCategoryForm

# views.py
def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        category_form = DocumentCategoryForm(request.POST)
        formset = DocumentMetaFormSet(request.POST, instance=None)

        if form.is_valid() and formset.is_valid() and category_form.is_valid():
            # Save the document first
            document = form.save()

            # Now, set the document_id to the category_form and save it
            category = category_form.save(commit=False)
            category.document_id = document  # Correct the assignment to document_id
            category.save()

            # Save the formset (DocumentMeta)
            formset.instance = document
            formset.save()

            return redirect('document_list')
        else:
            # Log form errors
            print(form.errors)
            print(category_form.errors)
            print(formset.errors)
    else:
        form = DocumentForm()
        category_form = DocumentCategoryForm()
        formset = DocumentMetaFormSet()

    return render(request, 'customadmin/document/document_form.html', {
        'form': form,
        'formset': formset,
        'category_form': category_form,
    })

def document_list(request):
    documents = Document.objects.all()
    return render(request, 'customadmin/document/document_list.html', {'documents': documents})


def document_delete(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    doc.delete()
    return redirect('document_list')
