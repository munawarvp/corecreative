from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import Product, ReviewRating
from category.models import Category
from .forms import ReviewForm
from carts.models import CartItem, Carts
from carts.views import _cart_id

from django.core.paginator import Paginator

# Create your views here.

def store(request, category_slug=None):
    categories=None
    products=None
    accessory = Category.objects.get(category_name = 'Accessories')

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products_final = Product.objects.filter(category=categories, is_available=True)
        product_count = products_final.count()
        
    else:
        products = Product.objects.filter(is_available=True).exclude(category=accessory)
        product_count = Product.objects.count()
        paginator = Paginator(products, 6)
        page_number = request.GET.get('page')
        products_final = paginator.get_page(page_number)

    context = {
        'products': products_final,
        'product_count':product_count,
    }
    return render(request, 'store/store.html', context)

def accessories(request):
    accessory = Category.objects.get(category_name = 'Accessories')
    products = Product.objects.filter(category = accessory)

    context = {
        'products': products
    }
    return render(request, 'store/accessories.html',context)

def product_detail(request, category_slug, product_slug):

    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        category = single_product.category
        
        realated = Product.objects.filter(category=category).exclude(product_name=single_product.product_name)
        reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
    except Exception as e:
        raise e


    if request.user.is_authenticated:
        carts = Carts.objects.filter(user=request.user, product=single_product).exists()
    else:
        carts = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()

    
        

    context = {
        'single_product':single_product,
        'carts': carts,
        'realated': realated,
        'reviews': reviews
    }
    return render(request, 'store/product.html', context)


def category(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'store/category.html', context)

#search

def search(request):
    q = request.GET['q']
    products = Product.objects.filter(product_name__icontains=q).order_by('-id')
    product_count = products.count()
    
    context = {
        'products': products,
        'product_count': product_count
    }
    return render(request, 'store/store.html', context)

def submit_review(request, product_id):
    product=Product.objects.get(id=product_id)
    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':

        print('posted ok')
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Your review added successfully..!!')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.product_id = product_id 
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Your review added successfully..!!')
                return redirect(url)

    else:
        return redirect('store')