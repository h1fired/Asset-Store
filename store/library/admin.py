from django.contrib import admin
from .models import PublicAsset, PublicModel, PublicTexture, Collection
from .abstractmodels import Tag


class PublicModelInline(admin.TabularInline):
    model=PublicModel

class PublicTextureInline(admin.TabularInline):
    model=PublicTexture

@admin.register(PublicAsset)
class PublicAssetAdmin(admin.ModelAdmin):
    inlines = [
        PublicTextureInline,
        PublicModelInline,
    ]
    
    list_display = ('name', 'image_tag', 'type', 'upload_time', 'author', 'max_resolution', 'subscription', 'author', 'status')
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass