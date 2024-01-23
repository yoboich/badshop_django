
from django.db.models import Sum, FloatField, F, Value
from django.apps import apps

from utils.services import (
    create_user_or_session_filter_dict
)
from items.models import Cart


class OrderMethodsMixin:

    @property
    def total_quantity(self):
        return sum(
            [item.quantity for item \
             in self.orderitem_set.all()
            ]
            )
    
    @property
    def items_price_without_discount(self):
        return sum(item.price * item.quantity 
            for item in self.orderitem_set.all()
        )
    
    @property
    def items_price_with_discount(self):
        return sum(item.sale_price * item.quantity 
            for item in self.orderitem_set.all()
        )

    @classmethod
    def create_order_for_current_user(cls, request):
        cart = Cart.get_or_create_cart(request)
        filter_dict = create_user_or_session_filter_dict(
            request
            )
        order = cls.objects.create(
            **filter_dict,  
            status='NP',
            promocode_discount=cart.promocode_discount,
            items_discount=cart.items_discount,
            items_price_with_promocode=cart.items_price_with_promocode,
            items_price_with_bonuses=cart.items_price_with_bonuses(request),
        )

        return order
    
    @classmethod
    def remove_current_user_unpaid_orders(cls, request):
        filter_dict = create_user_or_session_filter_dict(
            request
            )
        not_paid_orders = cls.objects.filter(
            **filter_dict,
            status='NP'
        )
        for order in not_paid_orders:
            order.status = 'NA'
            order.save()

    @classmethod
    def get_current_user_order(cls, request):
        filter_dict = create_user_or_session_filter_dict(
            request
            )
        order, _ = cls.objects.get_or_create(
            **filter_dict,  
            status='NP'
        )
        return order

    @classmethod
    def add_cart_items_to_order(cls, request):
        OrderItem = apps.get_model('orders', 'OrderItem')
        cart = Cart.get_or_create_cart(request)
        order = cls.get_current_user_order(request)
        for cart_item in cart.cartitem_set.all():
            OrderItem.objects.create(
                order=order,
                item=cart_item.item,
                price=cart_item.item.price,
                sale_price=cart_item.item.sale_price,
                quantity=cart_item.quantity
            )
    
    @classmethod
    def save_form_data_to_order(cls, request):
        '''Сохраняем данные из формы заказа в заказ'''
        TransportCompany = apps.get_model(
            'orders', 
            'TransportCompany'
            )
        Address = apps.get_model('users', 'Address')
        order = cls.get_current_user_order(request)
        form = request.POST
        if 'radio-transport' in form:
            order.transport_company=TransportCompany.objects.get(
                id=form['radio-transport']
                )
        if 'radio-address' in form:
            address = Address.objects.get(
                id=form['radio-address']
                )
            order.delivery_address = address.full_address()
        else:
            order.delivery_address = form['address']
        order.full_name = ' '.join(filter(None, (
            form['first_name'], 
            form['last_name'], 
            form['patronymic']
            )))
        order.email = form['email']
        order.comment = form['comment']
        order.save()
        return order

    @classmethod
    def create_new_order_for_current_user(cls, request):
        cls.remove_current_user_unpaid_orders(request)
        order = cls.create_order_for_current_user(request)
        cls.add_cart_items_to_order(request)
        return order

    # количество бонусов, которые нужно начислить пользователю за заказ
    @property
    def total_bonus_points(self):
        OrderItem = apps.get_model('orders', 'OrderItem')
        total_bonus_points = OrderItem.objects \
            .filter(order=self) \
            .aggregate(
                total=Sum(
                    F('price') \
                    * F('quantity') \
                    * F('item__bonus_percentage') \
                    / Value(100), 
                output_field=FloatField()
                ))['total']
        return total_bonus_points

    def total_bonus_in_order(self):
        pass