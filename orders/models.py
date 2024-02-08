import uuid

from django.contrib.sessions.models import Session
from django.db import models
from django.db.models import Sum, F, FloatField, Value

from balance.models import PromoCode
from items.models import CartItem, Cart
from users.models import CustomUser, Address

from badshop_django.logger import logger

from .model_methods.order_methods import OrderMethodsMixin
from .model_methods.discount_methods import DiscountMethodsMixin



# Create your models here.
class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    item = models.ForeignKey('items.item', on_delete=models.PROTECT, )
    quantity = models.IntegerField()
    price = models.FloatField(
        null=True, blank=True
        )
    sale_price = models.IntegerField(
        null=True, blank=True
        )
    
    class Meta():
        verbose_name = 'Единица заказа'
        verbose_name_plural = 'Единицы заказа'

    def __str__(self):
        return f'{self.order} - {self.item}'
    

class Order(OrderMethodsMixin, DiscountMethodsMixin, models.Model):
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        verbose_name='Пользователь', 
        blank=True, null=True
        )
    session = models.ForeignKey(
        Session, 
        on_delete=models.CASCADE, 
        blank=True, null=True
        )
    order_items = models.ManyToManyField(
        'OrderItem', 
        verbose_name='Предметы заказа', 
        related_name='order_item_set'
        )
    
    promocode_discount = models.IntegerField(
        verbose_name='Скидка по промокоду',
    )
    items_discount = models.IntegerField(
        verbose_name='Скидка на товары',
    )
    items_price_with_promocode = models.IntegerField(
        verbose_name='Стоимость товаров с учетом промокода'
    )
    
    items_price_with_bonuses = models.IntegerField(
        verbose_name='Стоимость товаров с учетом бонусов'
    )

    date_created = models.DateTimeField(
        auto_now_add=True
        )
    comment = models.CharField(
        max_length=240, 
        blank=True, 
        null=True, 
        verbose_name='Комментарий к заказу'
        )
    transport_company = models.ForeignKey(
        to='TransportCompany',
        verbose_name='Транспортная компания',
        on_delete=models.PROTECT,
        null=True, blank=True
        )
    delivery_address = models.CharField(
        max_length=255,
        verbose_name='Адрес доставки',
        null=True, blank=True
        )
    full_name = models.CharField(
        max_length=255,
        verbose_name='ФИО получателя',
        null=True, blank=True
        )
    phone = models.CharField(
        max_length=16,
        verbose_name='Телефон получателя',
        null=True, blank=True
    )
    email = models.CharField(
        max_length=255,
        verbose_name='Email',
        null=True, blank=True
    )

    STATUS_CHOICES = (
        ('OP', 'Оплачен'),
        ('DL', 'Доставлен'),
        ('NP', 'Не оплачен'),
        ('DD', 'Выполняется доставка'),
        ('NA', 'Не активен')
    )

    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='NP', verbose_name='Статус заказа', blank=True, null=True)

    outer_id = models.UUIDField(
        verbose_name='айди для банка',
        default=uuid.uuid4, 
        editable=False
        )
    payment_response_id = models.CharField(
        max_length=255,
        verbose_name='айди платежа в банке',
        editable=False,
        null=True, blank=True
    )

    promocode_discount_percentage = models.IntegerField(
        verbose_name='Скидка по промокоду',
        default=0
        )

    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"{self.email}, {self.status}"


class OrderStatus(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Статусы заказов'
        verbose_name_plural = 'Статусы заказов'


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_amount = models.IntegerField()
    payment_date = models.DateTimeField(auto_now_add=True)

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