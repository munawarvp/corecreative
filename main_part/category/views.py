from django.shortcuts import render
from store.models import Product

# Create your views here.

def search(request):
    q = request.GET['q']
    products = Product.objects.filter(product_name__icontains=q).order_by('-id')
    product_count = products.count()
    
    context = {
        'products': products,
        'product_count': product_count
    }
    return render(request, 'store/store.html', context)