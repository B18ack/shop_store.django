from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            self.session[settings.CART_SESSION_ID] = {}
            cart = self.session[settings.CART_SESSION_ID]
        self.cart = cart 
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['products'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    
    def __len__(self):
        # считает ск товаров в корзине
        return sum(item['quantity'] for item in self.cart.values())
    

    def add(self, product, quantity=1, update_quantity=False):
        # добавление товара в корзину или обновление кол-ва
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                  'price': str(product.price)}
        if  update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()      


    def save(self):
        # сохраняем товар
        self.session.modified = True
    
    
    def remove(self, product):
        # удаляем товар
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    

    def get_total_price(self):
        # получаем общ стоимость
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    

    def clear(self):
        # очистка корзины
        del self.session[settings.CART_SESSION_ID]
        self.save()