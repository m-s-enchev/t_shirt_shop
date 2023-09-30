from django.views.generic import ListView

from t_shirt_shop.products.models import Products


# Create your views here.


class IndexProductListView(ListView):
    model = Products
    template_name = 'common/homepage.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category1_products'] = Products.get_all_products_by_categoryid(1)
        context['category2_products'] = Products.get_all_products_by_categoryid(2)
        context['category3_products'] = Products.get_all_products_by_categoryid(3)
        return context

