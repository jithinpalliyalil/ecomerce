from .models import cart,cartitem
from . views import _cart_id

def counter(request):
    item_count=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            carts=cart.objects.filter(cart_id=_cart_id(request))
            cart_item=cartitem.objects.all().filter(cart=carts[:1])
            for cart_items in cart_item:
                item_count += cart_items.quantity
        except cart.DoesNotExist:
            item_count =0
    return dict(item_count=item_count)