from typing import Any, Dict
from django import forms

class VerifyForm(forms.Form):
    code = forms.CharField(label='Verification Code', widget=forms.TextInput(attrs={'type':'number'}))
    
    