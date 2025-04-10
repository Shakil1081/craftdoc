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

def hello_there(request):
    return render(request, 'docmodify/letterhead_upload.html')

def register(request):
    if request.method == 'POST':
        form = PublicUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User inactive until email verified
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Assign 'user' group
            user_group, created = Group.objects.get_or_create(name='user')
            user.groups.add(user_group)

            # Send verification email
            token = account_activation_token.make_token(user)
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

            return redirect('verification_mail_sent')
    else:
        form = PublicUserRegistrationForm()

    return render(request, 'docmodify/auth/register.html', {'form': form})

User = get_user_model()  # This gets your custom user model

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)  # Now uses your custom user model
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been verified!')
        return redirect('login')
    else:
        messages.error(request, 'Invalid verification link!')
        return redirect('login')

def verification_sent(request):
    return render(request, 'docmodify/auth/verification_sent.html')

def resend_verification_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                messages.warning(request, 'Account is already verified.')
                return redirect('login')

            token = account_activation_token.make_token(user)
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
    if not request.user.is_active:
        messages.warning(request, 'Please verify your email to access all features.')
    return render(request, 'docmodify/dashboard.html')

def public_login(request):
    if request.method == 'POST':
        form = PublicLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('public_dashboard')
                else:
                    messages.error(request, "Account not verified. Please check your email for verification link.")
                    return redirect('resend_verification')
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = PublicLoginForm()

    return render(request, 'docmodify/auth/login.html', {'form': form})