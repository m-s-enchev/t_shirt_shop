from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect

from t_shirt_shop.accounts.forms import ViewUserInfo, ViewProfileInfo, ViewAnonymousUserInfo
from t_shirt_shop.accounts.models import ShopUserModel, UserProfileModel, AnonymousUserData
from t_shirt_shop.orders.models import Orders
from t_shirt_shop.products.models import Products
from t_shirt_shop.shopping_cart.forms import AddToCartForm, ViewCartForm
from t_shirt_shop.shopping_cart.models import ShoppingCartItems, ShoppingCart, AnonymousShoppingCart


# Create your views here.

def add_to_shopping_cart(request, pk):
    product = Products.objects.get(pk=pk)
    user = request.user

    if user.is_authenticated:
        cart, _ = ShoppingCart.objects.get_or_create(user=user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key

        try:
            anonymous_cart = AnonymousShoppingCart.objects.get(session_key=session_key)
            cart = anonymous_cart.cart
        except AnonymousShoppingCart.DoesNotExist:
            cart = ShoppingCart()
            cart.save()
            anonymous_cart = AnonymousShoppingCart(cart=cart, session_key=session_key)
            anonymous_cart.save()

    cart_item, created = ShoppingCartItems.objects.get_or_create(cart=cart, product=product)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()
    else:
        form = AddToCartForm()

    context = {
        'product': product,
        'form': form
    }

    redirect_url = request.META.get('HTTP_REFERER')
    if not redirect_url or redirect_url == request.build_absolute_uri():
        redirect_url = 'product_single'

    return redirect(redirect_url, pk=pk, context=context)


def shopping_cart_view(request):
    user = request.user

    if user.is_authenticated:
        cart, _ = ShoppingCart.objects.get_or_create(user=user)
        cart_items = cart.shoppingcartitems_set.all()
    else:
        user = AnonymousUser()
        session_key = request.session.session_key
        try:
            anonymous_cart = AnonymousShoppingCart.objects.get(session_key=session_key)
            cart = anonymous_cart.cart
            cart_items = cart.shoppingcartitems_set.all()
        except AnonymousShoppingCart.DoesNotExist:
            cart_items = []

    total_price = 0

    if request.method == 'POST':
        form = ViewCartForm(cart_items, request.POST)
        if form.is_valid():
            for cart_item in cart_items:
                quantity = form.cleaned_data.get(f'item_{cart_item.id}_quantity')
                cart_item.quantity = quantity
                cart_item.save()

        return redirect('view_cart')
    else:
        form = ViewCartForm(cart_items, initial={f'item_{item.id}_quantity': item.quantity for item in cart_items})
        total_price = sum(item.total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form
    }
    return render(request, 'shopping_cart/view_cart.html', context)


# def remove_from_shopping_cart(request, cart_item_id):
#     cart_item = get_object_or_404(CartItem, pk=cart_item_id, user=request.user)
#     cart_item.delete()
#     return redirect('view_cart')


def shipping_details_view(request):
    form_user = None
    form_profile = None
    form_anonymous = None
    session_key = request.session.session_key

    if request.user.is_authenticated:
        user_instance = ShopUserModel.objects.get(id=request.user.id)
        profile_instance = UserProfileModel.objects.get(user=request.user)
        form_user = ViewUserInfo(instance=user_instance)
        form_profile = ViewProfileInfo(instance=profile_instance)
    else:
        anonymous_instance, _ = AnonymousUserData.objects.get_or_create(session_key=session_key)
        form_anonymous = ViewAnonymousUserInfo(instance=anonymous_instance)

    if request.method == 'POST':

        if request.user.is_authenticated:
            user_instance = ShopUserModel.objects.get(id=request.user.id)
            profile_instance = UserProfileModel.objects.get(user=request.user)
            user = request.user

            form_user = ViewUserInfo(request.POST, instance=user_instance)
            form_profile = ViewProfileInfo(request.POST, instance=profile_instance)

            if form_user.is_valid() and form_profile.is_valid():
                form_user.save()
                form_profile.save()

                order = Orders.objects.create(user=user)
                order.create_order_items_from_cart(session_key=session_key)
                ShoppingCartItems.objects.filter(cart__user=user).delete()
                return redirect('homepage')
        else:
            form_anonymous = ViewAnonymousUserInfo(request.POST, instance=anonymous_instance)

            if form_anonymous.is_valid():
                form_anonymous.save()

                order = Orders.objects.create(anonymous_user_data=anonymous_instance)
                order.create_order_items_from_cart(session_key=session_key)
                ShoppingCartItems.objects.filter(cart__session_carts__session_key=session_key).delete()
                return redirect('homepage')

    context = {
        'form_user': form_user,
        'form_profile': form_profile,
        'form_anonymous': form_anonymous,
    }

    return render(request, template_name='shopping_cart/shipping-details.html', context=context)



