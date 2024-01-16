from badshop_django.logger import logger

from utils.services import create_user_or_session_filter_dict

class CartMethodsMixin:
    # кол-во SKU
    @property
    def distinct_items_count(self):
        return self.cartitem_set.count()

    @property
    def total_quantity(self):
        return sum([item.quantity \
                    for item in self.cartitem_set.all() \
                        if item.is_active]
                    )
    
    @property
    def items_price_without_discount(self):
        return sum(item.item.price * item.quantity \
                    for item in self.cartitem_set.all() \
                        if item.is_active
                    )
    
    @property 
    def items_price_with_discount(self):
        return sum(item.item.sale_price * item.quantity 
            for item in self.cartitem_set.all()
        )


    @classmethod
    def get_or_create_cart(cls, request, user=None):
        if user:
            cart, created = cls.objects.get_or_create(
                user=user
                )
            return cart

        filter_dict = create_user_or_session_filter_dict(
            request
            )
        
        if filter_dict != {}:
            cart, created = cls.objects.get_or_create(
                **filter_dict
                    )

            logger.debug(f'cart = {cart}')
            return cart
        
        return 

    @classmethod
    def delete_current_user_cart(cls, request):
        cart = cls.get_or_create_cart(request)
        cart.delete()

    @classmethod
    def delete_cart_for_paid_order(cls, order):
        try:
            if order.user:
                cart = cls.objects.get(user=order.user)
            else:
                cart = cls.objects.get(session=order.session)
            cart.delete()
            logger.debug(f'! cart was just deleted')
        except:
            logger.debug(f'! cart already deleted')
