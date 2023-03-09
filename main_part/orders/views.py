from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from carts.models import Carts
from store.models import Product
from orders.models import Order, Payment, OrderProduct
from accounts.models import UserProfile
from .forms import OrderForm
import datetime
import json


# Create your views here.

def place_order(request):
    cart_items = Carts.objects.filter(user=request.user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    total = 0
    grand_total = 0

    for i in cart_items:
        total += i.sub_total()
    tax = (5*total)/100
    grand_total = total+tax
        
    
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            
            payement = request.POST['payment']
            if payement == 'cod':
                data.user = request.user
                data.first_name = form.cleaned_data['first_name']
                data.last_name = form.cleaned_data['last_name']
                data.email = form.cleaned_data['email']
                data.address_line = form.cleaned_data['address_line']
                data.city = form.cleaned_data['city']
                data.country = form.cleaned_data['country']
                data.phone = form.cleaned_data['phone']
                data.zipcode = form.cleaned_data['zipcode']
                data.order_total = grand_total
                data.save()
                #order_number has to generate

                yr = int(datetime.date.today().strftime('%Y'))
                dt = int(datetime.date.today().strftime('%d'))
                mt = int(datetime.date.today().strftime('%m'))
                d = datetime.date(yr,mt,dt)
                current_date = d.strftime("%Y%m%d")
                order_number = current_date + str(data.id)
                data.order_number=order_number
                
                payment = Payment(
                    user = request.user,
                    payment_id = "None",
                    payment_method = "COD",
                    amount_paid = grand_total,
                    status = "None",
                )
                payment.save()

                data.payment = payment
                data.is_ordered = True
                
                data.save()
                #add order product to the model from cart
                cart_items = Carts.objects.filter(user=request.user)

                for item in cart_items:
                    orderproduct = OrderProduct()
                    orderproduct.order_id = data.id
                    orderproduct.payment = payment
                    orderproduct.user_id = request.user.id
                    orderproduct.product_id = item.product_id
                    orderproduct.quantity = item.quantity
                    orderproduct.product_price = item.product.price
                    orderproduct.ordered = True
                    orderproduct.save()

                    #reduce the quantity after placing order
                    # ths should be inside the loop
                    product = Product.objects.get(id=item.product_id)
                    product.stock -= item.quantity
                    product.save()
                
                #remove the cartItem with respect to that user
                Carts.objects.filter(user=request.user).delete()

                order = Order.objects.get(user=request.user, is_ordered=True, order_number=order_number)
                ordered_product = OrderProduct.objects.filter(order_id=order.id)
                subtotal = 0
                tax = 0
                for i in ordered_product:
                    subtotal += i.product_price * i.quantity
                tax = (5*subtotal)/100
                

                context = {

                    'order': order,
                    'ordered_product': ordered_product,
                    'subtotal': subtotal,
                    'tax': tax,
                    'cart_items': cart_items,
                    'grand_total': grand_total,
                }
                return render(request, 'orders/cod_ordercomplete.html', context)
            else:
                data.user = request.user 
                data.first_name = form.cleaned_data['first_name']
                data.last_name = form.cleaned_data['last_name']
                data.email = form.cleaned_data['email']
                data.address_line = form.cleaned_data['address_line']
                data.city = form.cleaned_data['city']
                data.country = form.cleaned_data['country']
                data.phone = form.cleaned_data['phone']
                data.zipcode = form.cleaned_data['zipcode']
                data.order_total = grand_total
                data.save()
                print('ok')
                #order_number has to generate

                yr = int(datetime.date.today().strftime('%Y'))
                dt = int(datetime.date.today().strftime('%d'))
                mt = int(datetime.date.today().strftime('%m'))
                d = datetime.date(yr,mt,dt)
                current_date = d.strftime("%Y%m%d")
                order_number = current_date + str(data.id)
                data.order_number=order_number
                data.save()

                order_details = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)

            context = {

                'order_details': order_details,
                'cart_items': cart_items,
                'grand_total': grand_total,
            }

            return render(request, 'orders/paymentpage.html',context)
        else:
            messages.error(request, 'You must fill the fields...!')
            return redirect('checkout')


def payment(request):
    
    #updating payment of a order
    body = json.loads(request.body)
    print(body)
    order = Order.objects.get(user = request.user,is_ordered=False, order_number=body['orderID'])
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    #add order product to the model from cart
    cart_items = Carts.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        #reduce the quantity after placing order
        # ths should be inside the loop
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()


    #remove the cartItem with respect to that user
    Carts.objects.filter(user=request.user).delete()

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }

    return JsonResponse(data)

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_product = OrderProduct.objects.filter(order_id=order.id)
        subtotal = 0
        tax = 0
        for i in ordered_product:
            subtotal += i.product_price * i.quantity
        tax = (5*subtotal)/100
        payment = Payment.objects.get(payment_id=transID)
    

        context = {
            'order': order,
            'ordered_product': ordered_product,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'subtotal': subtotal,
            'tax': tax

            
        }
        return render(request, 'orders/ordercomplete.html', context)
    
    except(Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
    

def cod_ordercomplete(request):
    return render(request, 'orders/cod_ordercomplete.html')

def cancel_order(request, order_id):
    canceling_order = Order.objects.get(order_number=order_id)
    canceling_order.status = 'Canceled'
    canceling_order.save()
    print(canceling_order.status)
    return redirect('my_orders')