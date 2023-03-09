from django.shortcuts import render,redirect
from django.http import JsonResponse
from store.models import Product
from category.models import Category
from django.db.models import Q


def home(request):
    if 'term' in request.GET:
        qs = Product.objects.filter(product_name__icontains=request.GET.get('term'))
        products = list()
        for product in qs:
            products.append(product.product_name)
        return JsonResponse(products, safe=False)
    accessory = Category.objects.get(category_name = 'Accessories')
    products = Product.objects.filter(is_available=True).exclude(category=accessory)
    accessories = Product.objects.filter(category = accessory)

    context = {
        'products': products,
        'accessories': accessories
    }
    return render(request, 'index.html', context)

def search(request):
    q = request.GET['q']
    if q:
        products = Product.objects.order_by('-created_date').filter(Q(product_name__icontains=q) | Q(description__icontains=q))
        
        product_count = products.count()
        context = {
            'products': products,
            'product_count': product_count,
        }
    return render(request, 'store/store.html', context)


def page404(request, exception):
    return render(request, 'page404.html')