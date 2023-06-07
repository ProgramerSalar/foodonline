from django.shortcuts import render, get_object_or_404
from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.db.models import Prefetch 
from django.http import HttpResponse, JsonResponse
from .models import Cart



# Create your views here.


def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    vendor_count = vendors.count()
    context = {
        'vendors':vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)




def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)

# prefetch the data 
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )

    )
    context = {
        'vendor':vendor,
        'categories':categories,
    }

    return render(request, 'marketplace/vendor_detail.html',context)



# def add_to_cart(request, food_id):
#     if request.user.is_authenticated:
#         if request.is_ajax():
#             # check the food item exists
#             try:
#                 fooditem = FoodItem.objects.get(id=food_id)
#                 # check if the user has already added that food to the cart 
#                 try:
#                     chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)  # user is add to this fooditem otherwise not added to fooditem in cart 
#                     # Increase the Cart qunatity 
#                     chkCart.quantity += 1 
#                     chkCart.save()
#                     return JsonResponse({'status':'failed', 'message':'Incresed the cart quantity'})

#                 except:
#                     chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)  # if food is not added the cart , simply fooditem is added to cart 
#                     return JsonResponse({'status':'failed', 'message':'Added the food in cart'})


#             except:
#                 return JsonResponse({'status':'failed', 'message':'This food does not exist!'})


#         else:

#             return JsonResponse({'status':'failed', 'message':'Invalid request'})
        

#     else:
#         return JsonResponse({'status':'failed', 'message': 'Please login to continue'})









def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        # if request.is_ajax():
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            # Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity'})
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added the food to the cart'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})

    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
