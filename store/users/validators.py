import re
from django.core.exceptions import ValidationError
from django.conf import settings

def _get_validators_options(name):
    return next((item for item in settings.AUTH_VALIDATORS_OPTIONS if item["NAME"] == name), None)['OPTIONS']

def validate_password_length(value):
    options = _get_validators_options('MinPasswordLength')
    if len(value) < options['min_length']:
        raise ValidationError(
            'The password must contain at least 8 characters'
        )
        
def validate_password_numeric(value):
    if value.isdigit():
        raise ValidationError(
            'This password is entirely numeric.'
        )
        
def validate_username(value):
    if any(not c.isalnum() for c in value):
        raise ValidationError('Username must contain only letter and decimals')