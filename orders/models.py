import uuid

from django.contrib.sessions.models import Session
from django.db import models
from django.db.models import Sum, F, FloatField

from balance.models import PromoCode
from items.models import CartItem, Cart
from users.models import CustomUser, Address
from utils.services import create_user_or_session_filter_dict


# Create your models here.
class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    item = models.ForeignKey('items.item', on_delete=models.PROTECT, )
    quantity = models.IntegerField()
    price = models.FloatField(null=True, blank=True)
    
    class Meta():
        verbose_name = 'Единица заказа'
        verbose_name_plural = 'Единицы заказа'

    def __str__(self):
        return f'{self.order} - {self.item}'
    

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True)
    order_items = models.ManyToManyField('OrderItem', verbose_name='Предметы заказа', related_name='order_item_set')
    date_created = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=240, blank=True, null=True, verbose_name='Комментарий к заказу')
    delivery_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Адрес доставки')


    STATUS_CHOICES = (
        ('OP', 'Оплачен'),
        ('DL', 'Доставлен'),
        ('NP', 'Не оплачен'),
        ('DD', 'Выполняется доставка'),
        ('NA', 'Не активен')
    )

    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='NP', verbose_name='Статус заказа', blank=True, null=True)

    def total_price(self):
        total = OrderItem.objects \
            .filter(order=self) \
            .aggregate(
                total=Sum(F('price'), 
                output_field=FloatField()
                ))
        return total
    
    @classmethod
    def create_order_for_current_user(cls, request):
        filter_dict = create_user_or_session_filter_dict(
            request
            )
        order = Order.objects.create(
            **filter_dict,  
            status='NP'
        )

        return order
    
    @classmethod
    def remove_current_user_unpaid_orders(cls, request):
        filter_dict = create_user_or_session_filter_dict(
            request
            )
        not_paid_orders = Order.objects.filter(
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
        order = Order.objects.get_or_create(
            **filter_dict,  
            status='NP'
        )
        return order

    @classmethod
    def add_cart_items_to_order(cls, request):
        cart = Cart.get_or_create_cart(request)
        order = cls.get_current_user_order
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                item=cart_item,
                price=cart_item.item.sale_price,
                quantity=cart_item.quantity
            )
    

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"{self.user.email}, {self.status}"


class OrderStatus(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Статусы заказов'
        verbose_name_plural = 'Статусы заказов'


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_amount = models.IntegerField()
    payment_date = models.DateTimeField(auto_now_add=True)

    outer_id = models.UUIDField(
        verbose_name='айди для банка',
        default=uuid.uuid4, 
        editable=False
        )


    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'






class AppliedPromoCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True, blank=True)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Примененный промокод'
        verbose_name_plural = 'Примененные промокоды'
        

class TransportCompany(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название организации')

    class Meta:
        verbose_name = 'Транспортная компания'
        verbose_name_plural = 'Транспортные компании'

    def __str__(self):
        return self.name