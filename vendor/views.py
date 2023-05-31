from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from menu.forms import CategoryForm
from .forms import VendorForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category, FoodItem


def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
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


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor)
    context = {
        'categories': categories
        
    }
    return render(request, 'vendor/menu_builder.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category= get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)
    context = {
        'fooditems':fooditems,
        'category':category,
    }
    return render(request, 'vendor/fooditems_by_category.html', context)


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False) # this forms is 
            category.vendor = get_vendor(request)   
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category has been added successfully!')
            return redirect('menu_builder')
        
    else:
        form = CategoryForm()
        

    context = {
        'form':form,
    }
    return render(request , 'vendor/add_category.html',context)