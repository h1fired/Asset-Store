from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django_resized import ResizedImageField
from django.utils import timezone
from django.utils.html import mark_safe

from users.models import CustomUser

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


# Tag Model
class Tag(models.Model):
    name = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name

# Asset Model
class Asset(models.Model):
    TYPES = [
        ('material', 'Material'),
        ('model', 'Model'),
        ('hdri', 'HDRI'),
    ]
    
    name = models.CharField(max_length=128, unique=True, validators=[RegexValidator(r'^[a-zA-Z ]*$', 'Only letters are allowed.')])
    type = models.CharField(max_length=64, choices=TYPES)
    upload_time = models.DateTimeField(editable=False, default=timezone.now)
    preview = ResizedImageField(size=[512, 512], force_format='WEBP', quality=75, upload_to='assets/previews/', blank=False)
    max_resolution = models.CharField(max_length=12, choices=RESOLUTIONS)
    author = models.ForeignKey(CustomUser, related_name='%(app_label)s_%(class)s_assets', on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(Tag, related_name='%(app_label)s_%(class)s_tags', blank=True)
    
    class Meta:
        abstract = True
        
    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="30" height="30" />' % (self.preview))

    def __str__(self):
        return self.name
    
    
    
# Texture Model
class Texture(models.Model):
    TYPES = [
        ('color', 'Color'),
        ('roughness', 'Roughness'),
        ('metallic', 'Metallic'),
        ('specular', 'Specular'),
        ('normal', 'Normal'),
        ('displacement', 'Displacement'),
        ('bump', 'Bump'),
        ('alpha', 'Alpha'),
        ('emission', 'Emission'),
        ('hdri', 'HDRI'),
    ]
    
    type = models.CharField(max_length=64, choices=TYPES)
    texture = models.ImageField(upload_to='assets/textures/')
    resolution = models.CharField(max_length=12, choices=RESOLUTIONS)
    
    class Meta:
        unique_together = ('asset', 'type', 'resolution',)
        abstract = True
        
    def clean(self):
        if self.asset.category == 'hdri':
            if self.type != 'hdri':
                raise ValidationError('Asset category is "HDRI", so you have to use "HDRI" type')
        if self.asset.category != 'hdri':
            if self.type == 'hdri':
                raise ValidationError('Asset category is NOT "HDRI", so you shouldn\'t use "HDRI" type')
        return super().clean()
    

# Model Model
class Model(models.Model):
    TYPES = [
        ('.FBX', '.FBX'),
        ('Blender', 'Blender'),
        ('Cinema4D', 'Cinema4D'),
        ('3ds Max', '3ds Max'),
    ]
    type = models.CharField(max_length=64, choices=TYPES)
    model = models.FileField(upload_to='assets/models/')
    
    class Meta:
        unique_together = ('asset', 'type',)
        abstract = True
    
    def clean(self):
        if self.asset.category != 'model':
            raise ValidationError('Asset category is not "model"')
        return super().clean()