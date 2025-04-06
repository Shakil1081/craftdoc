from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PublicUserRegistrationForm, PublicLoginForm

def hello_there(request):
    return render(request, 'docmodify/letterhead_upload.html')


def register(request):
    if request.method == 'POST':
        form = PublicUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            
            # Assign 'user' group to this public user
            user_group, created = Group.objects.get_or_create(name='user')
            user.groups.add(user_group)

            login(request, user)

            return redirect('public_dashboard')
    else:
        form = PublicUserRegistrationForm()

    return render(request, 'docmodify/auth/register.html', {'form': form})


@login_required
def role_based_redirect(request):
    user = request.user
    if user.is_staff or user.is_superuser:
        return redirect('/admin/')  # Admin dashboard
    return redirect('public_dashboard')


@login_required
def public_dashboard(request):
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
                    return redirect('public_dashboard')  # Redirect to public dashboard
                else:
                    messages.error(request, "Account is disabled.")
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = PublicLoginForm()

    return render(request, 'docmodify/auth/login.html', {'form': form})