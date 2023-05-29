from django.shortcuts import render, get_object_or_404
from .forms import VendorForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor


# Create your views here.

def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    
    
    profile_form = UserProfileForm(instance=profile)  # when the pass for instance is profile , that is the role for the existence for instance
    vendor_form = VendorForm(instance=vendor)
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor':vendor,
    }
    return render(request, 'vendor/vprofile.html', context)