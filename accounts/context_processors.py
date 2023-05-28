from vendor.models import Vendor




def get_vendor(request):
    try:
        vendor = Vendor.object.get(user=request.user)
    except:
        vendor = None 
        
    return dict(vendor=vendor)



