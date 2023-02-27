from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product
from wishlist.models import Wishlist, Wishlist_item, Wishlists

from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def _wishlist_id(request):
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    return wishlist

def wishlist(request, total=0, quantity=0, wishlist_item=None):
    if request.user.is_authenticated:
        wishlist_items = Wishlists.objects.filter(user=request.user)
        
    else:
        try:
            wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
            wishlist_items = Wishlist_item.objects.filter(wishlist=wishlist, is_active=True)
        except ObjectDoesNotExist:
            return render(request, 'store/wishlist.html')

    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'store/wishlist.html', context)

def add_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        if Wishlists.objects.filter(product=product_id, user=request.user).exists():
            wishlist_item = Wishlists.objects.get(product=product_id, user=request.user)
            wishlist_item.quantity += 1
            wishlist_item.save()
            return redirect('wishlist')
        else:
            Wishlists.objects.create(user=request.user, product = product)
            return redirect('wishlist')
    else:
        try:
            wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
        except Wishlist.DoesNotExist:
            wishlist = Wishlist.objects.create(
                wishlist_id = _wishlist_id(request)
            )
        wishlist.save()
    
        try:
            wishlist_item = Wishlist_item.objects.get(product=product, wishlist=wishlist)
            wishlist_item.quantity += 1
        except Wishlist_item.DoesNotExist:
            wishlist_item = Wishlist_item.objects.create(
                product = product,
                quantity = 1,
                wishlist = wishlist,
            )
            wishlist_item.save()
        return redirect('wishlist')

def deletewishlist(request,product_id):
    
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        user = request.user
        Wishlists.objects.get(user = user, product= product).delete()
        return redirect('wishlist')
    else:
        wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = Wishlist_item.objects.get(product=product, wishlist=wishlist)
        
        cart_item.delete()
        return redirect('wishlist')