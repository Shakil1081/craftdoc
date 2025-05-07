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
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from collections import defaultdict
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.core.files.storage import default_storage

def hello_there(request):
    # Get the search term from the GET request
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', 'all')

    # Fetch documents, categories, and header/footer images
    documents = Document.objects.all().order_by('id')

    # Filter documents by search query
    if search_query:
        documents = documents.filter(title=search_query)

    # Handle category filtering
    if category_filter != 'all':
        # Fetch category object based on category filter
        category = Category.objects.get(name=category_filter)
        # Filter documents by this category
        documents = documents.filter(documentcategory__category=category)

    # Pagination
    paginator = Paginator(documents, 10)  # Show 10 documents per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get the first document (or any other document as needed)
    document = Document.objects.first()  
    categories = Category.objects.all()
    
    # Group images by document ID
    images_by_document = defaultdict(dict)
    for img in DocumentHeaderFooterImage.objects.filter(is_default=True):
        doc_id = img.document.id
        images_by_document[doc_id] = {
            'header': img.header.url if img.header else '',
            'footer': img.footer.url if img.footer else '',
            'body': img.preview_image.url if img.preview_image else ''
        }

    # Prepare context data for the template
    context = {
        'documents': page_obj,
        'categories': categories,
        'images_by_document': dict(images_by_document),
        'search_query': search_query,
        'category_filter': category_filter,
    }

    # Render the template with context
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
                download_type=download_type
            )
            user.use_credit("credit_per_template")
            return JsonResponse({'success': True, 'download_history_id': download_history.pk})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid method'})

def register(request):
    if request.method == 'POST':
        form = PublicUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User inactive until email verified
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
    # if not request.user.is_active:
    #     messages.warning(request, 'Please verify your email to access all features.')
    return render(request, 'docmodify/dashboard.html')

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
    
def earn_credit(request):
    credit_setting = Setting.objects.filter(key='credit_per_bdt').first()
    return render(request, 'docmodify/credit/earn.html', {
        'credit_setting': credit_setting
    })

def credit_earn_history(request):
    user_credit_history = CreditEarnHistory.objects.filter(user=request.user)
    paginator = Paginator(user_credit_history, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'docmodify/credit/earn_history.html', {'page_obj': page_obj})

def credit_uses_history(request):
    user_credit_history = CreditUsesHistory.objects.filter(user=request.user)
    paginator = Paginator(user_credit_history, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'docmodify/credit/uses_history.html', {'page_obj': page_obj})