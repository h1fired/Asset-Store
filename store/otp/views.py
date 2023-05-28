from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from .models import OTPUser, OTP
from .forms import VerifyForm
from users.models import CustomUser


def verify_account_view(request):
    # Redirect if user is verified
    if request.user.is_verified:
        return redirect('mainpage')
    
    # Create OTP User if not exists
    if OTPUser.objects.filter(user=request.user).exists():
        otp_user = OTPUser.objects.get(user=request.user)
    else:
        otp_user = OTPUser(user=request.user)
        otp_user.save()
        
    # Generate OTP
    if OTP.objects.filter(otp_user=otp_user).exists() is not True or OTP.objects.filter(otp_user=otp_user).last().is_expired():
        otp = OTP(otp_user=otp_user)
        otp.save()
        print('GEN_OTP: ' + str(otp.code))
        email = EmailMessage(
            subject='Confirmation code',
            body=f'Your confirmation code is {otp.code}',
            to=[request.user.email]
        )
        email.send()
        
        
    # User Verifing 
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid(): 
            form_otp = form.cleaned_data['code']
            print('FORM_OTP: ' + str(form_otp))
            last_otp = OTP.objects.filter(otp_user=otp_user).last()
            
            if otp_user.verify(form_otp, last_otp.code) and last_otp.is_expired() is not True:
                print('VERIFIED!')
                user = request.user
                user.is_verified = True
                user.save()
                
                last_otp.delete()
                messages.success(request, 'Your account succesfully activated!')
                
                return redirect('mainpage')
            else:
                messages.error(request, 'OTP is invalid or expired. Please try again or resend.')
            
    else:
        form = VerifyForm()
        
    context = {
        'verify_form': form,
    }
    
    return render(request, 'users/verify.html', context)

def resend_otp_view(request):
    otp_user = OTPUser.objects.get(user=request.user)
    otp = OTP(otp_user=otp_user)
    otp.save()
    print('NEWGEN_OTP: ' + str(otp.code))
    
    return redirect('otp_verify')  
        