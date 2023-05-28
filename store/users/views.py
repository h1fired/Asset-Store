from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from .models import CustomUser
from .forms import RegistrationForm, LoginForm, ChangeUsernameForm, ChangePasswordForm, ChangePictureForm
from otp.models import OTPUser


def singup_view(request):
    if request.user.is_authenticated:
        return redirect('mainpage')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_verified = False
            user.save()
            login(request, user)
        
            return redirect('otp_verify')
    else:
        form = RegistrationForm()
    
    context = {
        'signup_form': form,
    }
    
    return render(request, 'users/signup.html', context)


def signin_view(request):
    if request.user.is_authenticated:
        return redirect('mainpage')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.authenticate(request)
            if user:
                login(request, user)
                return redirect('mainpage')
    else:
        form = LoginForm()
        
    context = {
        'signin_form': form,
    }
        
    return render(request, 'users/signin.html', context)

def logout_view(request):
    if request.user.is_authenticated:
        redirect('mainpage')
    logout(request)
    
    return redirect('mainpage')


# user settings
def s_account_view(request):
    if request.user.is_authenticated is not True:
        return redirect('mainpage')
    
    username_form = ChangeUsernameForm(initial={'username': request.user.username})
    password_form = ChangePasswordForm(request.user)
    picture_form = ChangePictureForm(request.user)
    
    if request.method == 'POST':
        if 'f_username' in request.POST:
            username_form = ChangeUsernameForm(request.POST, instance=request.user, initial={'username': request.user.username})
            if username_form.is_valid():
                form_username = username_form.cleaned_data['username']
                if CustomUser.objects.filter(username=form_username).exists() and form_username != request.user.username:
                    raise ValidationError('User with this username already exists')
                else:
                    username_form.save()
                    
        if 'f_password' in request.POST:
            password_form = ChangePasswordForm(request.user, request.POST)
            if password_form.is_valid():
                user_pswd = password_form.save()
                update_session_auth_hash(request, user_pswd)  # Important!
                messages.success(request, 'Your password was successfully updated!')
            else:
                messages.error(request, 'Invalid change password. Try again.')
        
        if 'f_picture' in request.POST:
            picture_form = ChangePictureForm(request.POST, request.FILES, instance=request.user)
            if picture_form.is_valid():
                print(1311)
                picture_form.save()
    
    context = {
        'username_form': username_form,
        'password_form': password_form,
        'picture_form': picture_form,
    }
    
    return render(request, 'users/s_account.html', context)
  