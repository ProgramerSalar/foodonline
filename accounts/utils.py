
from django.shortcuts import render



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
    
    
    