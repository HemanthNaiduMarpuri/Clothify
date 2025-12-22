from django import forms
from .models import Register, Customer
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django_password_eye.fields import PasswordEye


class RegisterForm(forms.ModelForm):
    password = PasswordEye(label='Password')

    class Meta:
        model = Register
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
        })


class UserLoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'placeholder': 'Username',
            }
        )
    )

    password = PasswordEye(label='Password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
        })


class CustomerProfileEditForm(forms.ModelForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Customer
        fields = ['image', 'contact', 'address']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email

    def save(self, commit=True):
        customer_profile = super().save(commit=False)

        if self.user:
            self.user.username = self.cleaned_data.get('username')
            self.user.email = self.cleaned_data.get('email')
            self.user.save()

        if commit:
            customer_profile.save()
        return customer_profile
