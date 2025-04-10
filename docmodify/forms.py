from django import forms
from customadmin.models import User

class PublicUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'phone', 'password', 'department', 'designation']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Your Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your Phone'}),
            'department': forms.TextInput(attrs={'placeholder': 'Your Department'}),
            'designation': forms.TextInput(attrs={'placeholder': 'Your Designation'}),
        }


class PublicLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

