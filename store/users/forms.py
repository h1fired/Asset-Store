from django import forms
from django.contrib.auth import authenticate
from django.core.validators import MinLengthValidator
from django.contrib.auth.forms import PasswordChangeForm
from .validators import validate_password_length, validate_password_numeric, validate_username

from .models import CustomUser


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password_length, validate_password_numeric])
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exist.') 
        return email
    
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError("Passwords does not match")
        return confirm_password

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords does not match")
        
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
    
class LoginForm(forms.Form):
    email = forms.EmailField(label='E-Mail', widget=forms.EmailInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if CustomUser.objects.filter(email=email).exists() is not True:
            raise forms.ValidationError('Email does not exist') 
        return email
    
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Email or password was invalid.")
        return self.cleaned_data
    
    def authenticate(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        return user
    
class ChangePictureForm(forms.ModelForm):
    picture = forms.ImageField()
    
    class Meta:
        model = CustomUser
        fields = ('picture',)

class ChangeUsernameForm(forms.ModelForm):
    username = forms.CharField(max_length=128, validators=[validate_username])
    
    class Meta:
        model = CustomUser
        fields = ('username',)

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput, validators=[validate_password_length, validate_password_numeric])
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password1', 'new_password2',)