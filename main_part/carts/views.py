from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product
from accounts.models import Account, UserProfile
from .models import Cart, CartItem, Carts
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
   

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    
    return redirect('cart')

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')
    
def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    
    cart_item.delete()
    return redirect('cart')


# def cart(request, total=0, quantity=0, cart_items=None,gst=0, grand_total=0):
#     try:
#         cart = Cart.objects.get(cart_id=_cart_id(request))
#         cart_items = CartItem.objects.filter(cart=cart, is_active=True)
#         for cart_item in cart_items:
#             total += (cart_item.product.price * cart_item.quantity)
#             quantity = cart_item.quantity
#         gst = (18 * total)/100
#         grand_total = total + gst 
#     except ObjectDoesNotExist:
#         pass

#     context = {
#         'total': total,
#         'quantity': quantity,
#         'cart_items': cart_items,
#         'gst': gst,
#         'grand_total': grand_total,
        
#     }
#     return render(request, 'store/cart.html', context)

#changed cart functionality from session to database table

# @login_required(login_url='login')
def carts(request):
    if request.user.is_authenticated:
        user = request.user
        cart_items = Carts.objects.filter(user=user).order_by('id')
        total = 0
        grand_total = 0

        for i in cart_items:
            total += i.sub_total()
        tax = (5*total)/100
        grand_total = total+tax
    else:
        try:
            total = 0
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity = cart_item.quantity
            tax = (5 * total)/100
            grand_total = total + tax 
        except ObjectDoesNotExist:
            return render(request, 'store/cart.html')


    context = {
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
        
    }
    return render(request, 'store/cart.html', context)


def addtocart(request, prod_id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=prod_id)
        user = request.user

        if Carts.objects.filter(product=product, user=user).exists():
            cart = Carts.objects.get(user=user, product=product)
            cart.quantity += 1
            cart.save()
            return redirect('carts')
        else:
            Carts.objects.create(product=product, user=user)
            return redirect('carts')
    else:
        product = Product.objects.get(id=prod_id)
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            cart_item.save()
    
    return redirect('carts')

def removefromcart(request, prod_id):
    product = Product.objects.get(id=prod_id)
    user = request.user
    if request.user.is_authenticated:
        cart = Carts.objects.get(user=user, product=product)
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
            return redirect('carts')
        else:  
            Carts.objects.get(user = user, product= product).delete()
            return redirect('carts')
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=prod_id)
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            return redirect('carts')
        else:
            cart_item.delete()
            return redirect('carts')

def deletecartitem(request, prod_id):
    product = Product.objects.get(id=prod_id)
    if request.user.is_authenticated:
        user = request.user
        Carts.objects.get(user = user, product= product).delete()
        return redirect('carts')
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=prod_id)
        cart_item = CartItem.objects.get(product=product, cart=cart)
        
        cart_item.delete()
        return redirect('carts')


@login_required(login_url='login')
def checkout(request):
    if request.user.is_authenticated:
        
        userprofile = UserProfile.objects.get(user=request.user)
        carts = Carts.objects.filter(user=request.user).all()
        total = 0
        grand_total = 0

        for i in carts:
            total += i.sub_total()
        tax = (5*total)/100
        grand_total = total+tax

    context = {
        'carts': carts,
        'grand_total': grand_total,
        'userprofile': userprofile,
        
    }
    return render(request, 'store/checkout.html', context)

