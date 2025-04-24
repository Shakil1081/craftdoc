# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Document
from .forms import DocumentForm, DocumentMetaFormSet, DocumentCategoryForm, DocumentHeaderFooterImageFormSet

# views.py
from django.contrib import messages
from django.db import transaction

def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        category_form = DocumentCategoryForm(request.POST)
        formset = DocumentMetaFormSet(request.POST, request.FILES)
        header_footer_image_formset = DocumentHeaderFooterImageFormSet(request.POST, request.FILES)

        # Check individual validation
        is_valid = True

        if not form.is_valid():
            is_valid = False
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"DocumentForm - {field}: {error}")

        if not category_form.is_valid():
            is_valid = False
            for field, errors in category_form.errors.items():
                for error in errors:
                    messages.error(request, f"CategoryForm - {field}: {error}")

        if not formset.is_valid():
            is_valid = False
            for form_index, subform in enumerate(formset.forms):
                for field, errors in subform.errors.items():
                    for error in errors:
                        messages.error(request, f"MetaForm #{form_index + 1} - {field}: {error}")

        if not header_footer_image_formset.is_valid():
            is_valid = False
            for form_index, subform in enumerate(header_footer_image_formset.forms):
                for field, errors in subform.errors.items():
                    for error in errors:
                        messages.error(request, f"HeaderFooterImageForm #{form_index + 1} - {field}: {error}")

        if is_valid:
            try:
                with transaction.atomic():
                    # Save the main Document object
                    document = form.save()

                    # Save the category object (FK to Document)
                    category = category_form.save(commit=False)
                    category.document = document
                    category.save()

                    # Save DocumentMeta formset (FK to Document)
                    formset.instance = document
                    formset.save()

                    # Save HeaderFooterImage formset (FK to Document)
                    header_footer_image_formset.instance = document
                    header_footer_image_formset.save()

                    messages.success(request, "Document created successfully.")
                    return redirect('document_list')

            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {str(e)}")

    else:
        form = DocumentForm()
        category_form = DocumentCategoryForm()
        formset = DocumentMetaFormSet()
        header_footer_image_formset = DocumentHeaderFooterImageFormSet()

    return render(request, 'customadmin/document/document_form.html', {
        'form': form,
        'category_form': category_form,
        'formset': formset,
        'header_footer_image_formset': header_footer_image_formset,
    })



def document_list(request):
    documents = Document.objects.all()
    return render(request, 'customadmin/document/document_list.html', {'documents': documents})


def document_delete(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    doc.delete()
    return redirect('document_list')
