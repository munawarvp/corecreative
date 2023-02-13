from django.shortcuts import render, redirect
from store.models import Product
from category.models import Category
from accounts.models import Account
from orders.models import Order, OrderProduct

from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os

# Create your views here.


@login_required(login_url='login')
def admin_panel(request):
    category_count = Category.objects.count()
    product_count = Product.objects.count()
    orders_count = Order.objects.count()

    context = {
        'category_count': category_count,
        'product_count': product_count,
        'orders_count': orders_count,
    }
    return render(request, 'admin panel/admin_panel.html', context)


def user_list(request):
    users = Account.objects.all().filter(is_admin=False)

    context = {
        'users': users
    }
    return render(request, 'admin panel/users_list.html', context)

def block_user(request, user_id):
    user = Account.objects.get(pk=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
    else:
        user.is_active = True
        user.save()
    return redirect('user_list')


# category functions

@login_required(login_url='login')
def category_page(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }
    return render(request, 'admin panel/category_page.html', context)

def add_category(request):
    if request.method == 'POST':
        if Category.objects.filter(category_name = request.POST['category_name']).exists():
            messages.error(request, 'This Category is already added...!')
            return redirect('add_category')
        else:
            
            values = Category(
                category_name = request.POST['category_name'],
                slug = request.POST['slug'],
                description = request.POST['description'],
                cat_image = request.FILES['cat_image']
            )
            values.save()
            return redirect('category_page')

    return render(request, 'admin panel/add_category.html')

def edit_category(request, cat_id):
    single_category = Category.objects.get(id=cat_id)

    if request.method == 'POST':
        if len(request.FILES) != 0:
            if len(single_category.cat_image) > 0:
                os.remove(single_category.cat_image.path)
            single_category.cat_image = request.FILES['cat_image']
            single_category.save()

        value=Category.objects.filter(id=cat_id).update(
            category_name = request.POST['category_name'],
            slug = request.POST['slug'],
            description = request.POST['description']   
        )
        return redirect('category_page')
    context = {
        'single_category': single_category
    }
    return render(request, 'admin panel/edit_category.html', context)

def delete_category(request, cat_id):
    Category.objects.get(id=cat_id).delete()
    return redirect('category_page')


# product functions

@login_required(login_url='login')
def product_page(request):
    products = Product.objects.all()

    context = {
        'products': products
    }
    return render(request, 'admin panel/product_page.html', context)

def product_view(request, prod_id):
    single_product = Product.objects.get(id=prod_id)

    context = {
        'single_product': single_product
    }
    return render(request, 'admin panel/product_view.html', context)

def add_product(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        if Product.objects.filter(product_name = request.POST['product_name']).exists():
            messages.error(request, 'This Product is already added...!')
            return redirect('add_product')
        else:
            category_id = request.POST['category']
            Product.objects.create(
                product_name = request.POST['product_name'],
                slug = request.POST['slug'],
                price = request.POST['price'],
                stock = request.POST['stock'],
                category = Category.objects.get(id=category_id),
                description = request.POST['description'],
                image = request.FILES['product_image']
            )
            # values = Product(
            #     product_name = request.POST['product_name'],
            #     slug = request.POST['slug'],
            #     price = request.POST['price'],
            #     stock = request.POST['stock'],
            #     category = Category.objects.get(id=category_id),
                
            #     description = request.POST['description'],
            #     image = request.FILES['product_image']
            # )
            # values.save()
            return redirect('product_page')

    context = {
        'categories': categories
    }
    return render(request, 'admin panel/add_product.html', context)

def edit_product(request, prod_id):
    categories = Category.objects.all()
    product = Product.objects.get(id=prod_id)

    if request.method == 'POST':
        category_id = request.POST['category']
        if len(request.FILES) != 0:
            if len(product.image) > 0:
                os.remove(product.image.path)
            product.image = request.FILES['product_image']
            product.save()
        
        values = Product.objects.filter(id=prod_id).update(
            product_name = request.POST['product_name'],
            slug = request.POST['slug'],
            price = request.POST['price'],
            stock = request.POST['stock'],
            category = Category.objects.get(id=category_id),
            description = request.POST['description'],
        )

        return redirect('product_page')

    context = {
        'product': product,
        'categories': categories
    }
    return render(request, 'admin panel/edit_product.html', context)

def delete_product(request, prod_id):
    Product.objects.get(id=prod_id).delete()
    return redirect('product_page')


#orders

@login_required(login_url='login')
def order_page(request):

    orders = Order.objects.filter(is_ordered = True).all()

    context = {
        'orders': orders
    }
    return render(request, 'admin panel/orders.html', context)


def order_view(request, order_id):
    single_order = Order.objects.get(id=order_id)
    
    order_products = OrderProduct.objects.filter(order=single_order)
    context = {
        'single_order': single_order,
        'order_products': order_products,
    }
    return render(request, 'admin panel/order_view.html', context)



#search

def search(request):
    q = request.GET['q']
    products = Product.objects.filter(product_name__icontains=q).order_by('-id')
    context = {
        'products': products
    }
    return render(request, 'admin panel/product_page.html', context)