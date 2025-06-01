from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from .tokens import account_activation_token
from .forms import PublicUserRegistrationForm, PublicLoginForm
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from .forms import ForgotPasswordForm, ResetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from customadmin.models import CreditEarnHistory, CreditUsesHistory
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from collections import defaultdict
from customadmin.models import Document, Setting, DownloadHistory, DocumentCategory, DocumentMeta, DocumentHeaderFooterImage, Font, Category
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from collections import defaultdict
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
from weasyprint import HTML 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from PIL import Image
from customadmin.forms import UserForm,ProfileEditForm
import io
import json
from google import genai
import markdown
from pdf2image import convert_from_bytes
from django.db.models import Sum

def hello_there(request):
    search_query = request.GET.get('search', '').strip()
    category_filter = request.GET.get('category', 'all')

    try:
        page_number = int(request.GET.get('page', 1))
    except (ValueError, TypeError):
        page_number = 1

    documents = Document.objects.all().order_by('id')

    if search_query:
        documents = documents.filter(title__icontains=search_query)

    if category_filter != 'all':
        category = get_object_or_404(Category, name=category_filter)
        documents = documents.filter(documentcategory__category=category)

    paginator = Paginator(documents, 10)

    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        # If page is out of range (e.g. page < 1 or page > num_pages), deliver first or last page
        if page_number < 1:
            page_obj = paginator.page(1)
        else:
            page_obj = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        page_obj = paginator.page(1)

    # Group default header/footer images by document
    images_by_document = {}
    for img in DocumentHeaderFooterImage.objects.filter(is_default=True):
        doc_id = img.document.id
        images_by_document[doc_id] = {
            'header': getattr(img.header, 'url', '') if hasattr(img, 'header') and img.header else '',
            'footer': getattr(img.footer, 'url', '') if hasattr(img, 'footer') and img.footer else '',
            'body': getattr(img.preview_image, 'url', '') if hasattr(img, 'preview_image') and img.preview_image else ''
        }

    context = {
        'documents': page_obj,
        'categories': Category.objects.all(),
        'images_by_document': images_by_document,
        'search_query': search_query,
        'category_filter': category_filter,
    }

    return render(request, 'docmodify/index.html', context)

@login_required
def letterhead(request, document_id):
    # if not request.user.is_active:
    #     messages.warning(request, 'Please verify your email to access all features.')

     # Fetch the selected document
    document = get_object_or_404(Document, id=document_id)
    
    # Get all documents
    documents = Document.objects.all()
    
    # Reorder the documents list to make the selected document first
    documents = [document] + [doc for doc in documents if doc != document]

    categories = DocumentCategory.objects.filter(document=document)
    metas = DocumentMeta.objects.filter(document=document)
    header_footer_images = DocumentHeaderFooterImage.objects.filter(document=document)
    fonts = Font.objects.all()

    # Group images by document ID
    images_by_document = defaultdict(dict)
    default_images = DocumentHeaderFooterImage.objects.filter(is_default=True)
    for img in default_images:
        doc_id = img.document.id
        images_by_document[doc_id] = {
            'header': img.header.url if img.header else '',
            'footer': img.footer.url if img.footer else '',
            'body': img.preview_image.url if img.preview_image else ''
        }

    context = {
        'document': document,
        'documents': documents,
        'categories': categories,
        'metas': metas,
        'header_footer_images': header_footer_images,
        'fonts': fonts,
        'images_by_document': dict(images_by_document),
    }

    # Check if the request is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return JSON response for AJAX requests
        data = {
            'fonts': [
                {
                    'id': font.id,
                    'name': font.name,
                    'url': font.url,
                }
                for font in fonts
            ],
            'document': {
                'id': document.id,
                'logo': document.logo_path.url if document.logo_path else '',
                'phone': document.phone,
                'email': document.email,
                'location': document.location,
                'letterhead_content': document.letterhead_content,
                # add more fields if needed
            },
            'header_footer_images': [
                {
                    'id': hf.id,
                    'header': hf.header.url if hf.header else None,
                    'footer': hf.footer.url if hf.footer else None,
                    'css': hf.css if hf.css else None,
                    'is_default': hf.is_default,
                }
                for hf in header_footer_images
            ],
        }

        return JsonResponse(data)

    # Render the template for normal requests
    return render(request, 'docmodify/document/letterhead.html', context)

@csrf_exempt
@login_required
def save_download_history(request):
    if request.method == 'POST':
        user = request.user
        document_id = request.POST.get('document_id')
        document_hf_id = request.POST.get('document_hf_id')
        logo_file = request.FILES.get('logo_file')  # Handle uploaded file

        # Other fields...
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        location = request.POST.get('location')
        css = request.POST.get('css')
        download_type = request.POST.get('download_type')
        letterhead_content = request.POST.get('letterhead_content')

        try:
            document = Document.objects.get(pk=document_id)            
            document_hf = DocumentHeaderFooterImage.objects.get(pk=document_hf_id)
            
            # Optional: Save logo file to media
            logo_path = None
            if logo_file:
                logo_path = default_storage.save(f'documents/files/{logo_file.name}', logo_file)
            else:
                logo_path = document.logo_path
            
            download_history = DownloadHistory.objects.create(
                user=user,
                document_id=document.pk,
                document_hf=document_hf,
                logo_path=logo_path,
                contact=contact,
                email=email,
                location=location,
                css=css,
                header_path=document_hf.header if document_hf.header else '',
                footer_path=document_hf.footer if document_hf.footer else '',
                download_type=download_type,
                letterhead_content = letterhead_content
            )
            user.use_credit("credit_per_template")
            return JsonResponse({'success': True, 'download_history_id': download_history.pk})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid method'})

def download_history_file(request, download_type, id):
    try:
        history = DownloadHistory.objects.get(pk=id)
    except DownloadHistory.DoesNotExist:
        raise Http404("Download history not found.")

    def build_media_url(path):
        if path:
            return request.build_absolute_uri(settings.MEDIA_URL + path)
        return ''

    context = {
        'history': history,
        'logo_url': build_media_url(history.logo_path),
        'header_url': build_media_url(history.header_path),
        'footer_url': build_media_url(history.footer_path),
    }

    html_string = render_to_string('docmodify/pdf/download_document_pdf.html', context)
    pdf_bytes = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    if download_type == 'pdf':
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=download_history_{id}.pdf'
        return response

    elif download_type in ['jpg', 'png']:
        # Convert PDF to image(s)
        images = convert_from_bytes(pdf_bytes)
        image = images[0]  # Use only the first page

        img_bytes = io.BytesIO()
        if download_type == 'jpg':
            image.convert('RGB').save(img_bytes, format='JPEG')
            content_type = 'image/jpeg'
            extension = 'jpg'
        else:
            image.save(img_bytes, format='PNG')
            content_type = 'image/png'
            extension = 'png'

        img_bytes.seek(0)
        response = HttpResponse(img_bytes, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename=download_history_{id}.{extension}'
        return response

    else:
        raise Http404("Invalid download type.")

    history = get_object_or_404(DownloadHistory, pk=id)

    def build_media_url(path):
        if path:
            return request.build_absolute_uri(settings.MEDIA_URL + path)
        return ''

    context = {
        'history': history,
        'logo_url': build_media_url(history.logo_path),
        'header_url': build_media_url(history.header_path),
        'footer_url': build_media_url(history.footer_path),
    }

    return render(request, 'docmodify/pdf/download_document_pdf.html', context)



def register(request):
    if request.method == 'POST':
        form = PublicUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # User inactive until email verified
            user.set_password(form.cleaned_data['password'])
            user.save()
            user.earn_credit("signup_bonus")
            # # Generate and store 150-char token
            # token = user.generate_verification_token()

            # # Assign 'user' group
            # user_group, created = Group.objects.get_or_create(name='user')
            # user.groups.add(user_group)

            # # Send verification email
            # # token = account_activation_token.make_token(user)
            # uid = urlsafe_base64_encode(force_bytes(user.pk))
            # protocol = 'https' if request.is_secure() else 'http'
            # current_site = get_current_site(request)
            # domain = current_site.domain

            # context = {
            #     'user': user,
            #     'protocol': protocol,
            #     'domain': domain,
            #     'uid': uid,
            #     'token': token,
            #     'site_name': 'CraftDOC'
            # }

            # # Render both HTML and plain text versions
            # html_content = render_to_string('docmodify/auth/acc_active_email.html', context)
            # text_content = render_to_string('docmodify/auth/acc_active_email.txt', context)

            # # Send the email
            # email = EmailMultiAlternatives(
            #     subject="Verify Your Email | CraftDOC",
            #     body=text_content,  # Plain text fallback
            #     from_email="noreply@craftdoc.com",
            #     to=[user.email]
            # )
            # email.attach_alternative(html_content, "text/html")  # HTML version
            # email.send()

            # return redirect('verification_mail_sent')
    else:
        form = PublicUserRegistrationForm()

    return render(request, 'docmodify/auth/register.html', {'form': form})

User = get_user_model()  # This gets your custom user model

def verify_email(request, uidb64, token):
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user.is_active:
        messages.warning(request, 'Account is already verified.')
        if user.is_authenticated:
            return redirect('public_dashboard')
        return redirect('login')
        
    verification_status = (
        user is not None and
        user.email_verify_token and  # Token exists
        user.email_verify_token == token
    )

    if verification_status:
        user.verify_email()  # Updates email_verified_at
        messages.success(request, 'Email verified successfully!')
        user.earn_credit("signup_bonus")
        return redirect('login')
    else:
        messages.error(request, 'Invalid or expired verification link')
        return redirect('resend_verification')

def verification_sent(request):
    return render(request, 'docmodify/auth/verification_sent.html')

def resend_verification_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                messages.warning(request, 'Account is already verified.')
                if user.is_authenticated:
                    return redirect('public_dashboard')
                return redirect('login')

            # token = account_activation_token.make_token(user)
            token = user.generate_verification_token()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            protocol = 'https' if request.is_secure() else 'http'
            current_site = get_current_site(request)
            domain = current_site.domain

            context = {
                'user': user,
                'protocol': protocol,
                'domain': domain,
                'uid': uid,
                'token': token,
                'site_name': 'CraftDOC'
            }

            # Render both HTML and plain text versions
            html_content = render_to_string('docmodify/auth/acc_active_email.html', context)
            text_content = render_to_string('docmodify/auth/acc_active_email.txt', context)

            # Send the email
            email = EmailMultiAlternatives(
                subject="Verify Your Email | CraftDOC",
                body=text_content,  # Plain text fallback
                from_email="noreply@craftdoc.com",
                to=[user.email]
            )
            email.attach_alternative(html_content, "text/html")  # HTML version
            email.send()
            
            messages.success(request, 'Verification email sent. Please check your inbox.')
            return redirect('verification_mail_sent')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')
    
    return render(request, 'docmodify/auth/resend_verification.html')

@login_required
def role_based_redirect(request):
    user = request.user
    if user.is_staff or user.is_superuser:
        return redirect('/admin/')
    return redirect('public_dashboard')

@login_required
def public_dashboard(request):
    user = request.user

    total_earned = CreditEarnHistory.objects.filter(user_id=user.id).aggregate(total=Sum('earned_credit'))['total'] or 0
    total_used = CreditUsesHistory.objects.filter(user_id=user.id).aggregate(total=Sum('usage_credit'))['total'] or 0
    total_downloads = DownloadHistory.objects.filter(user_id=user.id).count()

    # Fetch credit earn history
    credit_earn_history = CreditEarnHistory.objects.filter(user_id=user.id).order_by('-created_at')[:5]
    credit_usage_history = CreditUsesHistory.objects.filter(user_id=user.id).order_by('-created_at')[:5]

    context = {
        'total_earned': total_earned,
        'total_used': total_used,
        'total_downloads': total_downloads,
        'credit_earn_history': credit_earn_history,
        'credit_usage_history': credit_usage_history,
    }

    return render(request, 'docmodify/dashboard.html', context)
def public_login(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('public_dashboard')
    
    if request.method == 'POST':    
        User = get_user_model()
        form = PublicLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            next_url = request.POST.get('next')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user is not None:
                if not user.check_password(password):
                    messages.error(request, "Invalid email or password.")
                # elif not user.is_active:
                #     login(request, user)
                #     messages.error(request, "Account not verified. Please enter your email for verification link.")
                #     return redirect('resend_verification')
                else:
                    if not user.is_superuser:                        
                        login(request, user)
                        return redirect(next_url or 'hello_there')
                    else:
                        return redirect('admin-login')
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = PublicLoginForm()

    return render(request, 'docmodify/auth/login.html', {'form': form})

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = user.generate_password_reset_token()
                reset_link = request.build_absolute_uri(
                    f"/reset-password/{uid}/{token}/"
                )
                protocol = 'https' if request.is_secure() else 'http'
                current_site = get_current_site(request)
                domain = current_site.domain

                context = {
                    'user': user,
                    'protocol': protocol,
                    'reset_link': reset_link,
                    'site_name': 'CraftDOC'
                }

                # Render both HTML and plain text versions
                html_content = render_to_string('docmodify/auth/password_reset_mail.html', context)
                text_content = render_to_string('docmodify/auth/password_reset_mail.txt', context)

                # Send the email
                email = EmailMultiAlternatives(
                    subject="Password Reset | CraftDOC",
                    body=text_content,  # Plain text fallback
                    from_email="noreply@craftdoc.com",
                    to=[user.email]
                )
                email.attach_alternative(html_content, "text/html")  # HTML version
                email.send()

                return redirect('password_reset_mail_done')
            except User.DoesNotExist:
                form.add_error('email', 'No user with this email found.')
    else:
        form = ForgotPasswordForm()
    return render(request, 'docmodify/auth/forgot_password.html', {'form': form})

def mail_send_done(request):
    return render(request, 'docmodify/auth/password_reset_done.html')

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user is not None and user.password_reset_token == token:
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['password'])
                # user.password_reset_token = None
                user.save()
                messages.success(request, 'Password reset successfully!')
                return redirect('login')
        else:
            form = ResetPasswordForm()
        return render(request, 'docmodify/auth/reset_password.html', {'form': form})
    else:
        messages.error(request, 'Invalid or expired password reset link.')
        return redirect('forgot_password')

@login_required
def edit_profile(request):
    user = request.user  # Get logged-in user
    
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile_edit')  # Redirect to profile page after saving
    else:
        form = ProfileEditForm(instance=user)

    return render(request, "docmodify/profile_edit.html", {"form": form, "user": user})

def earn_credit(request):
    credit_setting = Setting.objects.filter(key='credit_per_bdt').first()
    return render(request, 'docmodify/credit/earn.html', {
        'credit_setting': credit_setting
    })

def credit_earn_history(request):
    user_credit_history = CreditEarnHistory.objects.filter(user=request.user)
    paginator = Paginator(user_credit_history, 5)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    start_index = (page_obj.number - 1) * paginator.per_page
    return render(request, 'docmodify/credit/earn_history.html', {'page_obj': page_obj, 'start_index': start_index})
   
def credit_uses_history(request):
    user_credit_history = CreditUsesHistory.objects.filter(user=request.user)
    paginator = Paginator(user_credit_history, 5)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    start_index = (page_obj.number - 1) * paginator.per_page
    return render(request, 'docmodify/credit/uses_history.html', {'page_obj': page_obj, 'start_index': start_index})

client = genai.Client(api_key="AIzaSyBUK6zfkpLyp2LgcE9l80NO_I616CYgCfI")  # Configure globally

@csrf_exempt
@require_POST
def generate_ai_response(request):
    try:
        data = json.loads(request.body)
        conversation_history = data.get("conversation", [])

        if not conversation_history:
            return JsonResponse({"success": False, "error": "No conversation history provided"}, status=400)

        # Format the conversation
        prompt_text = ""
        for message in conversation_history:
            prompt_text += f"{message['role']}: {message['text']}\n"

        # Generate response
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt_text,
        )

        markdown_text = response.text
        html_text = markdown.markdown(markdown_text)

        return JsonResponse({"success": True, "html": html_text, "markdown": markdown_text})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)