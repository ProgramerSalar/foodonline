from django.shortcuts import render, get_object_or_404, redirect
from .forms import VendorForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages

# Create your views here.

def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    
    
    profile_form = UserProfileForm(instance=profile)  # when the pass for instance is profile , that is the role for the existence for instance
    vendor_form = VendorForm(instance=vendor)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)  # files to are coming through the post method and use to the profile 
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid(): # profile_form and valid and vendor_form is valid then use to that profile_form is save and vendor_form is save 
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'settings updated.' )  
            return redirect('vprofile')
        
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
            
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
        
        
    
    
    
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor':vendor,
    }
    return render(request, 'vendor/vprofile.html', context)