from django.shortcuts import render

from .models import PublicAsset

# Create your views here.
def library(request):
    
    assets = PublicAsset.objects.all()
    
    context = {
        'assets': assets,
    }
    
    return render(request, 'library/public_library.html', context)