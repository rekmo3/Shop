from .cart import Cart


def cart(request):
    """
    Додає об'єкт кошика у контекст кожного шаблону,
    щоб лічильник товарів можна було вивести в шапці сайту.
    """
    return {"cart": Cart(request)}
