from django.core.mail import EmailMessage
from django.shortcuts import render , redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from .models import User
from django.contrib import messages






def detectUser(user):
    if user.role == 1:
        redirectURl = 'vendorDashboard'
        return redirectURl
    elif user.role == 2:
        redirectURl = 'custDashboard'
        return redirectURl
        
    elif user.role == None and user.is_superadmin:
        redirectURl = '/admin'
        return redirectURl
    
    
def activate(request , uidb64 , token):
    # activate the user by setting the is_active status to True 
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
        
    except(TypeError, ValueError , OverflowError, User.DoesNotExist):
        user=None
        
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active=True
        user.save()
        messages.success(request, 'your account has been activated!')
        return redirect('myAccount')
    
    else:
        messages.error(request , 'Invalid activation link')
        return redirect('myAccount')
        
    
    
    
def send_verification_email(request, user):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    mail_subject = 'Please activate your account!'
    message = render_to_string('accounts/emails/account_verification_email.html',{
        'user':user, 
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user),
    })
    to_email = user.email 
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()
    
    
    
    
