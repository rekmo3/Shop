from decimal import Decimal

from django.conf import settings

from main.models import Product


class Cart:
    """
    Обгортка над request.session для управління кошиком покупця.

    Товари зберігаються у сесії у вигляді словника:
    {
        "<product_id>": {"quantity": <int>, "price": "<str>"},
        ...
    }
    Ціна зберігається рядком, бо Decimal не серіалізується у JSON за замовчуванням.
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # зберігаємо порожній кошик у сесії
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Додає товар у кошик або оновлює його кількість.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}

        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity

        # захист від некоректного/від'ємного значення
        if self.cart[product_id]["quantity"] < 1:
            self.remove(product_id)
            return

        self.save()

    def save(self):
        # явно позначаємо сесію як змінену, щоб Django зберіг дані
        self.session.modified = True

    def remove(self, product_id):
        """
        Видаляє товар з кошика.
        """
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Перебирає товари в кошику та підтягує відповідні об'єкти Product з БД.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Повертає загальну кількість усіх одиниць товарів у кошику.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        """
        Повертає загальну вартість усіх товарів у кошику.
        """
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def clear(self):
        """
        Повністю очищає кошик (видаляє його із сесії).
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
