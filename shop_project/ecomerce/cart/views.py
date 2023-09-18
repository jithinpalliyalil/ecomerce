from django.shortcuts import redirect, render, get_object_or_404
from shopping.models import product
from .models import cart, cartitem
from django.core.exceptions import ObjectDoesNotExist
def _cart_id(request):
    carts = request.session.session_key
    if not carts:
        carts = request.session.create()
    return carts

def add_cart(request,product_id):
    products = product.objects.get(id=product_id)
    try:
        carts = cart.objects.get(cart_id=_cart_id(request))
    except cart.DoesNotExist:
        carts = cart.objects.create(cart_id=_cart_id(request))
        carts.save(),
    try:
        cart_item = cartitem.objects.get(product=products, cart=carts)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save()
    except cartitem.DoesNotExist:
        cart_item = cartitem.objects.create(product=products, quantity=1, cart=carts)
        cart_item.save()
    return redirect('cart:cart_detail')
def cart_detail(request,total=0,counter=0,cart_item=None):
    try:
        carts = cart.objects.get(cart_id=_cart_id(request))
        cart_item = cartitem.objects.filter(cart=carts, active=True)
        for cart_items in cart_item:
            total += (cart_items.product.price * cart_items.quantity)
            counter += cart_items.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html', dict(cart_item=cart_item, total=total, counter=counter))
def cart_remove(request,product_id):
    carts = cart.objects.get(cart_id=_cart_id(request))
    products = get_object_or_404(product, id=product_id)
    cart_items = cartitem.objects.get(product=products, cart=carts)
    if cart_items.quantity > 1:
        cart_items.quantity -= 1
        cart_items.save()
    else:
        cart_items.delete()
    return redirect('cart:cart_detail')

def full_remove(request,product_id):
    carts = cart.objects.get(cart_id=_cart_id(request))
    products = get_object_or_404(product, id=product_id)
    cart_items = cartitem.objects.get(product=products, cart=carts)
    cart_items.delete()
    return redirect('cart:cart_detail')