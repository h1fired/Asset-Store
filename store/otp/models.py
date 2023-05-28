from typing import Iterable, Optional
import pyotp

from django.db import models
from django.utils import timezone
from django.conf import settings
from users.models import CustomUser

class OTPUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=32, default=pyotp.random_base32(length=32))
    
    def verify(self, user_otp, otp):
        return user_otp == otp
    
    
class OTP(models.Model):
    otp_user = models.ForeignKey(OTPUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    
    def is_expired(self):
        return self.created_at + timezone.timedelta(seconds=settings.OTP_AGE) < timezone.now()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.code = pyotp.HOTP(self.otp_user.secret_key).at(self.id)
        super().save(*args, **kwargs)
        