from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), min_length=6, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), min_length=6, required=False)

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'phone', 'password', 'confirm_password', 'department', 'designation', 'profile_image']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = getattr(self, 'instance', None)

        if user and user.email != email and User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = getattr(self, 'instance', None)

        if user and user.username != username and User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        return username

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        user = getattr(self, 'instance', None)

        if user and user.phone != phone and User.objects.filter(phone=phone).exists():
            raise ValidationError("Phone number already exists.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError("Passwords do not match.")
            cleaned_data["password"] = make_password(password)
        else:
            # If no new password is provided, retain the existing one
            if self.instance and self.instance.pk:
                cleaned_data["password"] = self.instance.password

        return cleaned_data
