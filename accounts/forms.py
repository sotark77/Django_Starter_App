from django import forms
from django.forms.widgets import PasswordInput
from django.contrib.auth.forms import UserCreationForm
from .models import Users
from django.core.exceptions import ValidationError

#-----Login-----
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email Address')
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-400 rounded-md focus:outline-none focus:border-gray-500',
            # 'placeholder': 'Enter your email'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-400 rounded-md focus:outline-none focus:border-gray-500',
            # 'placeholder': 'Enter your password'
        })
    

#----Registration form------
class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    user_name = forms.CharField(required=True)

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-400 rounded-md focus:outline-none focus:border-gray-500'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-400 rounded-md focus:outline-none focus:border-gray-500'}))    
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border border-gray-400 rounded-md focus:outline-none focus:border-gray-500'}))
    user_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-400 rounded-md focus:outline-none focus:border-gray-500'}))
    password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'w-full px-3 py-2 border border-gray-400 rounded-md focus:outline-none focus:border-gray-500'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'w-full px-3 py-2 border border-gray-400 rounded-md focus:outline-none focus:border-gray-500'}))

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'user_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.user_name = self.cleaned_data['user_name']
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user



#---Update user form---
#---Not in use yet---
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['email', 'first_name', 'last_name', 'user_name', 'avatar']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:border-indigo-500'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:border-indigo-500'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:border-indigo-500'
            }),
            'user_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:border-indigo-500'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:border-indigo-500 file:bg-gray-100'
            }),
        }
        error_messages = {
            'email': {
                'invalid': 'Enter a valid email address.',
                'required': 'Email is required.',
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure all fields are required (except avatar which is optional)
        for field in self.fields:
            self.fields[field].required = field != 'avatar'

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Users.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This email is already in use. Please use a different one.")
        if len(email) > 250:
            raise ValidationError("Email address is too long (max 250 characters).")
        return email


