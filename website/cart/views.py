from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    max_qty = product.quantity
    form = CartAddProductForm(request.POST, max_quantity=max_qty, available_quantity=product.quantity)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
        return redirect('cart:cart_detail')
    else:
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(
                initial={'quantity': item['quantity'], 'update': True},
                max_quantity=item['product'].quantity,
                available_quantity=item['product'].quantity
            )

        return render(request, 'cart/cart_detail.html', {
            'cart': cart,
            'form_errors': form.errors,
        })



def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        product = item['products']
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'update': True
            },
            max_quantity=product.quantity,
            available_quantity=product.quantity
        )
    return render(request, 'cart/cart_detail.html', {'cart': cart})



def cart_order(request):
    return render(request, 'cart/order.html')

def checkout(request):
    return render(request, 'cart/checkout.html')