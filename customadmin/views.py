from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import UserForm,ProfileEditForm
from django.contrib import messages
from django.http import JsonResponse
from rolepermissions.decorators import has_permission_decorator
# from rolepermissions.checkers import has_permission
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import PermissionDenied
from .forms import UserRegistrationForm
from .forms import ResetPasswordForm, ForgotPasswordForm
from django.contrib.auth import login, authenticate
from django.utils.timezone import now 
from django.utils.encoding import force_bytes, force_str
from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create the user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.email_verified_at = None  # Set email_verified_at to None (not verified)
            user.save()

            # here implement email sent while register

            # Redirect to the verification page after successful registration
            return redirect('verification_sent')
    else:
        form = UserRegistrationForm()

    return render(request, 'customadmin/register.html', {'form': form})

# Login view for checking email verification
def login_view(request):
    if request.user.is_authenticated and request.user.is_active and request.user.is_superuser:
        return redirect('custom_admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if the user is an admin (superuser)
            if user.is_superuser:
                login(request, user)
                return redirect('custom_admin_dashboard')  # Redirect to the dashboard after successful login
            else:
                # Check if the user's email is verified for non-admin users
                if user.email_verified_at is None:
                    login(request, user)
                    messages.error(request, 'Please verify your email before logging in.')
                    return redirect('verification_sent')  # Redirect to verification page
                else:
                    if request.user.is_superuser:
                        login(request, user)
                        return redirect('custom_admin_dashboard')
                    else:
                        return redirect('login') 
        else:
            messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'customadmin/login.html')


def verification_sent(request):
    return render(request, 'customadmin/verification_sent.html')

@login_required
def custom_admin_dashboard(request):
    return render(request, 'customadmin/index.html')


@login_required
def users_list(request):
    # Check if the user has the required permission
    if not request.user.has_perm('customadmin.view_user'):
        raise PermissionDenied  # Return a 403 Forbidden error if they lack permission

    users = User.objects.filter(is_superuser=False)
    return render(request, 'customadmin/user/users_list.html', {'users': users})


@login_required
def create_user(request):
    if not request.user.has_perm('customadmin.add_user'):
        raise PermissionDenied 

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_verified_at = now()
            user.save()

            # Assign selected groups
            selected_groups = request.POST.getlist('groups')
            user.groups.set(Group.objects.filter(id__in=selected_groups))

            # Assign permissions from groups
            for group in user.groups.all():
                for perm in group.permissions.all():
                    user.user_permissions.add(perm)

            messages.success(request, "User created successfully!")
            return redirect('users_list')
    else:
        form = UserForm()

    return render(request, 'customadmin/user/create_user.html', {'form': form})



@login_required
def edit_user(request, pk):
    if not request.user.has_perm('customadmin.edit_user'):
        raise PermissionDenied 
    
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # Ensure password is not reset if left empty
            if not form.cleaned_data.get('password'):
                form.cleaned_data.pop('password', None)

            # Keep the existing profile image if none is uploaded
            if not request.FILES.get('profile_image'):
                form.instance.profile_image = user.profile_image

            form.save()
            messages.success(request, "User updated successfully!")
            return redirect('users_list')
    else:
        form = UserForm(instance=user)

    return render(request, 'customadmin/user/edit_user.html', {'form': form, 'user': user})


@login_required
def delete_user(request, pk):
    if not request.user.has_perm('customadmin.delete_user'):
        raise PermissionDenied 
    if request.method == 'DELETE':
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'status': 'failed'}, status=400)

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'  # Your custom form template
    # email_template_name = 'registration/password_reset_email.html'  # Plain text email template (optional)
    html_email_template_name = 'registration/password_reset_email.html'  # Your custom HTML email template
    # subject_template_name = 'registration/password_reset_subject.txt'  # Custom subject template
    success_url = reverse_lazy('password_reset_done')

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        """
        Override the send_mail method to send both plain text and HTML emails.
        """
        subject = render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())  # Remove any line breaks
        body = render_to_string(email_template_name, context)  # Plain text email (optional)

        # Render the HTML email template
        html_email = render_to_string(html_email_template_name, context)

        # Create the email message
        msg = EmailMultiAlternatives(subject, body, from_email, [to_email])
        msg.attach_alternative(html_email, "text/html")  # Attach the HTML version
        msg.send()



@login_required
def edit_profile(request):
    user = request.user  # Get logged-in user
    
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile_edit')  # Redirect to profile page after saving
    else:
        form = ProfileEditForm(instance=user)

    return render(request, "customadmin/profile_edit.html", {"form": form, "user": user})
from django.urls import reverse


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
                    reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
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
                html_content = render_to_string('registration/password_reset_email.html', context)
                text_content = render_to_string('registration/password_reset_mail.txt', context)

                # Send the email
                email = EmailMultiAlternatives(
                    subject="Password Reset | CraftDOC",
                    body=text_content,  # Plain text fallback
                    from_email="noreply@craftdoc.com",
                    to=[user.email]
                )
                email.attach_alternative(html_content, "text/html")  # HTML version
                email.send()

                return redirect('password_reset_done')
            except User.DoesNotExist:
                form.add_error('email', 'No user with this email found.')
    else:
        form = ResetPasswordForm()
    return render(request, 'registration/password_reset_form.html', {'form': form})

def mail_send_done(request):
    return render(request, 'registration/password_reset_done.html')

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
                messages.error(request, 'There was an error with your submission. Please try again.')
        else:
            form = ResetPasswordForm()
        return render(request, 'registration/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'Invalid or expired password reset link.')
        return redirect('password_reset')


