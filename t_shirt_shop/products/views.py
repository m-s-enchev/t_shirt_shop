from django.shortcuts import render
from django.views.generic import ListView

from t_shirt_shop.common.views import IndexProductListView
from t_shirt_shop.products.models import Products


# Create your views here.


class ProductListView(ListView):
    model = Products
    template_name = 'products/products-all.html'
    context_object_name = 'products'
    paginate_by = 9


class ProductListViewWomen(ListView):
    template_name = 'products/products-women.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        return Products.get_all_products_by_categoryid(1)


class ProductListViewMen(ListView):
    template_name = 'products/products-men.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        return Products.get_all_products_by_categoryid(2)


class ProductListViewKids(ListView):
    template_name = 'products/products-kids.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        return Products.get_all_products_by_categoryid(3)


def product_single(request, pk):
    product = Products.objects.get(pk=pk)
    context = {
        'product': product,
    }
    return render(request, template_name='products/product-single.html', context=context)
