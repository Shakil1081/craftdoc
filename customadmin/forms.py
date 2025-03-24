from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission, ContentType
from django.contrib.auth.models import Group
from .models import Category

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), min_length=6, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), min_length=6, required=False)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    # Additional fields
    organization = forms.CharField(max_length=255, required=False)
    profession = forms.CharField(max_length=255, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    city = forms.CharField(max_length=255, required=False)
    facebook_link = forms.URLField(required=False)
    x_link = forms.URLField(required=False)
    instagram_link = forms.URLField(required=False)
    linkedin_link = forms.URLField(required=False)
    youtube_link = forms.URLField(required=False)

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'phone', 'password', 'confirm_password', 'department', 'designation', 'profile_image', 'groups', 'organization', 'profession', 'address', 'city', 'facebook_link', 'x_link', 'instagram_link', 'linkedin_link', 'youtube_link']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['profile_image'].required = False

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



class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ["name", "codename", "content_type"]

    content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.all(),
        label="Content Type"
    )



class ContentTypeForm(forms.ModelForm):
    class Meta:
        model = ContentType
        fields = ['app_label', 'model']  # Fields you want to allow editing

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    # Additional fields
    organization = forms.CharField(max_length=255, required=False)
    profession = forms.CharField(max_length=255, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    city = forms.CharField(max_length=255, required=False)
    facebook_link = forms.URLField(required=False)
    x_link = forms.URLField(required=False)
    instagram_link = forms.URLField(required=False)
    linkedin_link = forms.URLField(required=False)
    youtube_link = forms.URLField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'name', 'organization', 'profession', 'address', 'city', 'facebook_link', 'x_link', 'instagram_link', 'linkedin_link', 'youtube_link']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError("Passwords do not match")
        
        return cleaned_data
    

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'short_name', 'parent', 'category_level']
        widgets = {
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'category_level': forms.NumberInput(attrs={'class': 'form-control'}),
        }