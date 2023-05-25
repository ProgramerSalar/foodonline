from django.shortcuts import render , redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User , UserProfile
from django.contrib import messages , auth
from vendor.forms import VendorForm
from django.views.decorators.csrf import requires_csrf_token

















# Create your views here.

def registerUser(request):
    if request.method == 'POST':
        # print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            # create the user using the form
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role=User.CUSTOMER
            # user.save()
            
            
            # create the user using create_user method 
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user  = User.objects.create_user(first_name=first_name , last_name=last_name , username=username,email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            
            # messages 
            messages.success(request, 'your account registered successfully')
            
            
            print('User is created')
            return redirect('registerUser')
        
        else:
            print('invalid form')
            print(form.errors)
            
    else:
        
    
        form = UserForm()
    context = {
        'form':form,
    }
    return render(request , 'accounts/registerUser.html' , context)




def registerVendor(request):
    if request.method == 'POST':
        # store the data and create the user 
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid:
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user  = User.objects.create_user(first_name=first_name , last_name=last_name , username=username,email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)  # commit false mins - 
            vendor.user = user 
            user_profile = UserProfile.objects.get(user=user)  # 
            vendor.user_profile = user_profile  # vendor user profile to connect the vendor 
            vendor.save()
            messages.success(request , 'Your account has been registered successfully! please wai for the approval.')
            return redirect('registerVendor')
            
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()
    
    context = {
        'form':form,
        'v_form':v_form,
    }
    
    return render(request , 'accounts/registerVendor.html',context)


@requires_csrf_token
def login(request):
    if request.method == 'POST':
        email = request.POST['email']  # fetch the email address using the post request 
        password = request.POST['password'] # fetch the password using the post request
        
        user = auth.authenticate(email=email ,password=password)   # authenticate the email and password 
        if user is not None:
            auth.login(request ,user)  # allow the user to login 
            messages.success(request , 'You are logged in')
            
        else:
            messages.error(request , 'Invalid login credentials')  # user is not logged in
            return redirect('login')
    return render(request , 'accounts/login.html')





def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out')   # inf mins color is blue 
    return redirect('login')




def dashboard(request):
    return render(request , 'accounts/dashboard.html')

