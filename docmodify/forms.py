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

