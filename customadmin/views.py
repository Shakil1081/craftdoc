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
from django.contrib.auth import login, authenticate
from django.utils.timezone import now 


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
                    messages.error(request, 'Please verify your email before logging in.')
                    return redirect('verification_sent')  # Redirect to verification page
                else:
                    login(request, user)
                    return redirect('custom_admin_dashboard')  # Redirect to the dashboard after successful login
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


# class CustomPasswordResetView(PasswordResetView):
#     template_name = 'registration/password_reset_form.html'  # Your custom form template
#     email_template_name = 'registration/password_reset_email.html'  # Your custom email template
#     # subject_template_name = 'registration/password_reset_subject.txt'  # Optional: Custom subject template
#     success_url = reverse_lazy('password_reset_done')

#     def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
#         """
#         Override the send_mail method to customize the email sending process.
#         """
#         subject = "Reset Your Password | CraftDOC"  # Custom subject
#         email = render_to_string(email_template_name, context)  # Render the HTML email template

#         # Create the email message
#         msg = EmailMessage(
#             subject,
#             email,
#             from_email,
#             [to_email],
#         )
#         msg.content_subtype = "html"  # Set the content subtype to HTML
#         msg.send()

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
