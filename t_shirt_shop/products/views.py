from django.shortcuts import render

from t_shirt_shop.products.models import Products


# Create your views here.


def products_all(request):
    return render(request, template_name='products/products-all.html')


def product_single(request, pk):
    product = Products.objects.get(pk=pk)
    context = {
        'product': product,
    }
    return render(request, template_name='products/product-single.html', context=context)
