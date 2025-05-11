# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import DocumentForm, DocumentMetaFormSet, DocumentCategoryForm, DocumentHeaderFooterImageFormSet
from collections import defaultdict
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import Document, DocumentCategory, DocumentMeta, DocumentHeaderFooterImage, Font
# views.py
from django.contrib import messages
from django.db import transaction

def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        category_form = DocumentCategoryForm(request.POST)
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
        header_footer_image_formset = DocumentHeaderFooterImageFormSet()

    return render(request, 'customadmin/document/document_form.html', {
        'form': form,
        'category_form': category_form,
        'header_footer_image_formset': header_footer_image_formset,
    })


def document_edit(request, pk):
    document = get_object_or_404(Document, pk=pk)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        category_form = DocumentCategoryForm(request.POST, instance=getattr(document, 'documentcategory', None))
        header_footer_image_formset = DocumentHeaderFooterImageFormSet(request.POST, request.FILES, instance=document)

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

        if not header_footer_image_formset.is_valid():
            is_valid = False
            for form_index, subform in enumerate(header_footer_image_formset.forms):
                for field, errors in subform.errors.items():
                    for error in errors:
                        messages.error(request, f"HeaderFooterImageForm #{form_index + 1} - {field}: {error}")

        if is_valid:
            try:
                with transaction.atomic():
                    document = form.save()

                    category = category_form.save(commit=False)
                    category.document = document
                    category.save()

                    header_footer_image_formset.instance = document
                    header_footer_image_formset.save()

                    messages.success(request, "Document updated successfully.")
                    return redirect('document_list')

            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {str(e)}")

    else:
        form = DocumentForm(instance=document)
        category_form = DocumentCategoryForm(instance=getattr(document, 'documentcategory', None))
        header_footer_image_formset = DocumentHeaderFooterImageFormSet(instance=document)

    return render(request, 'customadmin/document/document_form.html', {
        'form': form,
        'category_form': category_form,
        'header_footer_image_formset': header_footer_image_formset,
        'edit_mode': True,  # Optional: to toggle buttons/labels in the template
        'document_id': document.id,
    })


def document_list(request):
    documents = Document.objects.all()
    return render(request, 'customadmin/document/document_list.html', {'documents': documents})


def document_delete(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    doc.delete()
    return redirect('document_list')


def document_lhsetup(request, document_id):
    # Only fetch the selected document
    document = get_object_or_404(Document, pk=document_id)

    categories = DocumentCategory.objects.filter(document=document)
    metas = DocumentMeta.objects.filter(document=document)
    header_footer_images = DocumentHeaderFooterImage.objects.filter(document=document)
    fonts = Font.objects.all()

    # Group default image (for initial selection)
    default_header_footer = None
    for img in header_footer_images:
        if img.is_default:
            default_header_footer = {
                'header': img.header.url if img.header else '',
                'footer': img.footer.url if img.footer else '',
                'body': img.preview_image.url if img.preview_image else '',
                'css': img.css,
                'id': img.id,
            }
            break

    context = {
        'document': document,
        'categories': categories,
        'metas': metas,
        'header_footer_images': header_footer_images,
        'fonts': fonts,
        'default_header_footer': default_header_footer,
        'default_css': default_header_footer['css'] if default_header_footer else '',
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX request to save selected css
        if request.method == "POST":
            selected_id = request.POST.get('selected_id')
            css = request.POST.get('css')
            save_all_css = request.POST.get('saveAllCss') == 'true'  # <--- added

            if save_all_css:
                # Save CSS for all header/footer images of the document
                try:
                    hf_images = DocumentHeaderFooterImage.objects.filter(document_id=document_id)
                    updated_count = 0
                    for hf_image in hf_images:
                        hf_image.css = css
                        hf_image.save()
                        updated_count += 1

                    return JsonResponse({'success': True, 'updated_count': updated_count})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})

            else:
                # Save CSS for only the selected header/footer image
                try:
                    hf_image = DocumentHeaderFooterImage.objects.get(id=selected_id)
                    hf_image.css = css
                    hf_image.save()
                    return JsonResponse({'success': True})
                except DocumentHeaderFooterImage.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Not found'})

    return render(request, 'customadmin/document/letterhead_setup.html', context)
