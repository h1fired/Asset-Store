from django.test import TestCase
from library.models import Collection, PublicAsset, PublicModel, PublicTexture
from users.models import CustomUser

from django.templatetags.static import static

# Create your tests here.
class AssetTest(TestCase):
    def setUp(self):
        user = CustomUser(email='testuser1@test.ts', password='testuser1')
        user.save()
    
    def test_assets_processing(self):
        user = CustomUser.objects.get(email='testuser1@test.ts')
        
        pc_asset = PublicAsset.objects.create(name='Test Asset', type='material', preview=static('red_apple.png'), max_resolution='2K', author=user)
        texture = PublicTexture.objects.create(asset=pc_asset, type='Color', texture=static('red_apple.png'), resolution='1K')
        model = PublicModel.objects.create(asset=pc_asset, type='Blender', model=static('red_apple.png'))
        collection = Collection.objects.create(name='Collection1')
        collection.assets.add(pc_asset)
        
        
        