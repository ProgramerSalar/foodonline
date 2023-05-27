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
    
    

        
    
    
    
def send_verification_email(request, user, mail_subject,email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template,{
        'user':user, 
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user),
    })
    to_email = user.email 
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()
    
    
    