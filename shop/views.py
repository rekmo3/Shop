from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from main.models import Product
from .cart import Cart


@require_POST
def cart_add(request, product_id):
    """
    Додає товар у кошик (або оновлює його кількість) та повертає
    користувача на сторінку кошика.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    override_quantity = request.POST.get('override_quantity') in ('True', 'true', 'on', '1')
    cart.add(product=product, quantity=quantity, override_quantity=override_quantity)
    return redirect('shop:cart_detail')


def cart_remove(request, product_id):
    """
    Видаляє товар з кошика.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product.id)
    messages.success(request, f'Товар "{product.name}" видалено з кошика.')
    return redirect('shop:cart_detail')


def cart_detail(request):
    """
    Сторінка деталізації кошика.
    """
    cart = Cart(request)
    context = {
        "title": "Кошик",
        "cart": cart,
    }
    return render(request, "shop/cart_detail.html", context)
