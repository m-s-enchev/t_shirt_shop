"""
URL configuration for t_shirt_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from t_shirt_shop.contact_form_messages import views as contact_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('t_shirt_shop.accounts.urls')),
    path('', include('t_shirt_shop.common.urls')),
    path('products/', include('t_shirt_shop.products.urls')),
    path('cart/', include('t_shirt_shop.shopping_cart.urls')),
    path('about-us/', TemplateView.as_view(template_name='common/about-us.html'), name='about_us'),
    path('faq/', TemplateView.as_view(template_name='common/faq.html'), name='faq'),
    path('shipping-info/', TemplateView.as_view(template_name='common/shipping_info.html'), name='shipping_info'),
    path('quality/', TemplateView.as_view(template_name='common/quality.html'), name='quality'),
    path('careers/', TemplateView.as_view(template_name='common/careers.html'), name='careers'),
    path('custom-designs/', TemplateView.as_view(template_name='common/custom-designs.html'), name='custom_designs'),
    path('contact-us/', contact_views.contact_messages, name='contact_us'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

