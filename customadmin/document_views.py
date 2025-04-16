# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Document
from .forms import DocumentForm, DocumentMetaFormSet, DocumentCategoryForm, DocumentHeaderFooterImageFormSet

# views.py
def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        category_form = DocumentCategoryForm(request.POST)
        formset = DocumentMetaFormSet(request.POST, request.FILES, instance=None)
        header_footer_image_formset = DocumentHeaderFooterImageFormSet(request.POST, request.FILES, instance=None)

        if form.is_valid() and formset.is_valid() and category_form.is_valid() and header_footer_image_formset.is_valid():
            # Save the main Document object
            document = form.save()

            # Save the category object
            category = category_form.save(commit=False)
            category.document = document  # assuming FK is named `document`
            category.save()

            # Save DocumentMeta formset
            formset.instance = document
            formset.save()

            # Save HeaderFooterImage formset
            header_footer_image_formset.instance = document
            header_footer_image_formset.save()

            return redirect('document_list')
        else:
            # Optional: Log form errors
            print("DocumentForm errors:", form.errors)
            print("CategoryForm errors:", category_form.errors)
            print("Meta Formset errors:", formset.errors)
            print("Header/Footer Formset errors:", header_footer_image_formset.errors)
    else:
        form = DocumentForm()
        category_form = DocumentCategoryForm()
        formset = DocumentMetaFormSet()
        header_footer_image_formset = DocumentHeaderFooterImageFormSet()

    return render(request, 'customadmin/document/document_form.html', {
        'form': form,
        'formset': formset,
        'category_form': category_form,
        'header_footer_image_formset': header_footer_image_formset
    })


def document_list(request):
    documents = Document.objects.all()
    return render(request, 'customadmin/document/document_list.html', {'documents': documents})


def document_delete(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    doc.delete()
    return redirect('document_list')
