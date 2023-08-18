from django.shortcuts import render, redirect

from t_shirt_shop.accounts.forms import ViewUserInfo, ViewProfileInfo, ViewAnonymousUserInfo
from t_shirt_shop.accounts.models import ShopUserModel, UserProfileModel, AnonymousUserData
from t_shirt_shop.orders.models import Orders
from t_shirt_shop.products.models import Products
from t_shirt_shop.shopping_cart.forms import AddToCartForm, ViewCartForm
from t_shirt_shop.shopping_cart.models import ShoppingCartItems, ShoppingCart, AnonymousShoppingCart


# Add items to shopping cart from products-all, homepage or product-single templates
def get_cart(request, user, session_key):
    if user.is_authenticated:
        cart, _ = ShoppingCart.objects.get_or_create(user=user)
    else:
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
    return cart


def update_cart_item(cart, product, quantity):
    cart_item, created = ShoppingCartItems.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()


def add_to_shopping_cart(request, pk):
    product = Products.objects.get(pk=pk)
    user = request.user
    session_key = request.session.session_key

    cart = get_cart(request, user, session_key)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data.get('quantity')
            update_cart_item(cart, product, quantity)
        else:
            update_cart_item(cart, product, quantity=1)
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


# View and update shopping cart
def get_cart_and_items(user, session_key):
    if user.is_authenticated:
        cart, _ = ShoppingCart.objects.get_or_create(user=user)
    else:
        try:
            anonymous_cart = AnonymousShoppingCart.objects.get(session_key=session_key)
            cart = anonymous_cart.cart
        except AnonymousShoppingCart.DoesNotExist:
            cart = None
    if cart:
        cart_items = cart.shoppingcartitems_set.all()
        total_price = sum(item.total_price() for item in cart_items)
    else:
        cart_items = []
        total_price = 0
    return cart, cart_items, total_price


def update_cart_items(cart_items, form_data):
    for cart_item in cart_items:
        quantity = form_data.get(f'item_{cart_item.id}_quantity')
        cart_item.quantity = quantity
        cart_item.save()


def shopping_cart_view(request):
    user = request.user
    session_key = request.session.session_key

    cart, cart_items, total_price = get_cart_and_items(user, session_key)

    if request.method == 'POST':
        form = ViewCartForm(cart_items, request.POST)
        if form.is_valid():
            update_cart_items(cart_items, form.cleaned_data)
            return redirect('view_cart')
    else:
        initial_data = {f'item_{item.id}_quantity': item.quantity for item in cart_items}
        form = ViewCartForm(cart_items, initial=initial_data)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form
    }
    return render(request, 'shopping_cart/view_cart.html', context)


# Shipping details and finalizing order
def create_order_for_authenticated_user(request, profile_instance, session_key):
    order = Orders.objects.create(
        user=request.user,
        email=request.user.email,
        first_name=request.user.first_name,
        last_name=request.user.last_name,
        address=profile_instance.address,
        phone_number=profile_instance.phone_number
    )
    order.create_order_items_from_cart(session_key=session_key)
    ShoppingCartItems.objects.filter(cart__user=request.user).delete()


def create_order_for_anonymous_user(anonymous_instance, form_anonymous, session_key):
    order = Orders.objects.create(
        anonymous_user_data=anonymous_instance,
        email=form_anonymous.cleaned_data['email'],
        first_name=form_anonymous.cleaned_data['first_name'],
        last_name=form_anonymous.cleaned_data['last_name'],
        address=form_anonymous.cleaned_data['address'],
        phone_number=form_anonymous.cleaned_data['phone_number']
    )
    order.create_order_items_from_cart(session_key=session_key)
    ShoppingCartItems.objects.filter(cart__session_carts__session_key=session_key).delete()


def shipping_details_view(request):
    form_user = None
    form_profile = None
    form_anonymous = None
    session_key = request.session.session_key

    if request.user.is_authenticated:
        user_instance = ShopUserModel.objects.get(id=request.user.id)
        profile_instance = UserProfileModel.objects.get(user=request.user)
        form_user = ViewUserInfo(request.POST or None, instance=user_instance)
        form_profile = ViewProfileInfo(request.POST or None, instance=profile_instance)

        if request.method == 'POST':
            if form_user.is_valid() and form_profile.is_valid():
                form_user.save()
                form_profile.save()

                create_order_for_authenticated_user(request, profile_instance, session_key)
                return redirect('homepage')

    else:
        anonymous_instance, _ = AnonymousUserData.objects.get_or_create(session_key=session_key)
        form_anonymous = ViewAnonymousUserInfo(request.POST or None, instance=anonymous_instance)
        if request.method == 'POST':
            if form_anonymous.is_valid():
                form_anonymous.save()

                create_order_for_anonymous_user(anonymous_instance, form_anonymous, session_key)
                return redirect('homepage')
            else:
                print(form_anonymous.errors)

    context = {
        'form_user': form_user,
        'form_profile': form_profile,
        'form_anonymous': form_anonymous,
    }

    return render(request, template_name='shopping_cart/shipping-details.html', context=context)

