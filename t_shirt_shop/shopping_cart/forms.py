from django import forms

from t_shirt_shop.shopping_cart.models import ShoppingCartItems


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField()


class ViewCartForm(forms.ModelForm):
    class Meta:
        model = ShoppingCartItems
        fields = []

    def __init__(self, cart_items, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for item in cart_items:
            self.fields[f'item_{item.id}_quantity'] = forms.IntegerField(
                label=f'Quantity for {item.product.name}',
                initial=item.quantity,
                min_value=0,
                required=False
            )