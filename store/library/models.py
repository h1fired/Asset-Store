from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django_resized import ResizedImageField
from django.utils import timezone
from django.utils.html import mark_safe

from users.models import CustomUser
from .abstractmodels import Asset, Model, Texture

# Choices
RESOLUTIONS = [
    ('1K', '1K'),
    ('2K', '2K'),
    ('4K', '4K'),
    ('8K', '8K'),
]

STATUSES = [
    ('active', 'Active'),
    ('hidden', 'Hidden'),
    ('blocked', 'Blocked'),
    ('review', 'Review'),
]
    
# Public Asset Model
class PublicAsset(Asset):
    subscription = models.BooleanField(default=False)
    status = models.CharField(max_length=64, choices=STATUSES, default='review')
    
class PublicModel(Model):
    asset = models.ForeignKey(PublicAsset, related_name='%(app_label)s_%(class)s_models', on_delete=models.CASCADE)
    
class PublicTexture(Texture):
    asset = models.ForeignKey(PublicAsset, related_name='%(app_label)s_%(class)s_textures', on_delete=models.CASCADE)
    
    
# Asset Collection Model
class Collection(models.Model):
    assets = models.ManyToManyField(PublicAsset, related_name='collection')
    name = models.CharField(max_length=128, unique=True, validators=[RegexValidator(r'^[a-zA-Z ]*$', 'Only letters are allowed.')])