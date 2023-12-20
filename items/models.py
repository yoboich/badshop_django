from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User  # Для авторизованных пользователей
from django.contrib.sessions.models import Session  # Для неавторизованных пользователей
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from balance.models import PromoCode
from users.models import CustomUser
from utils.services import get_current_session


# Create your models here.
class Item(models.Model):

    name = models.CharField(max_length=200, verbose_name="Название товара")
    image = models.ImageField(upload_to="items/%Y/%m/%d/", blank=True, null=True, verbose_name="Изображение товара")
    price = models.IntegerField(default=0, blank=True, null=True, verbose_name="Цена товара")
    discount = models.IntegerField(default=0, blank=True, null=True, verbose_name="Скидка")
    seil_price = models.IntegerField(default=0, blank=True, null=True, verbose_name="Цена со скидкой")
    rating = models.IntegerField(default=0, blank=True, null=True, verbose_name="Рэйтинг")
    text = RichTextField(blank=True, null=True, verbose_name="Описание товара")
    compound = RichTextField(blank=True, null=True, verbose_name="Состав товара")
    delivery = RichTextField(blank=True, null=True, verbose_name="Информация о доставке")
    category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.CASCADE, verbose_name="Категория")
    brend = models.ForeignKey('Brend', blank=True, null=True, on_delete=models.CASCADE, verbose_name="Бренд")

    bonus_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=15, verbose_name="Процент бонусных баллов", blank=True, null=True)

    def calculate_bonus_points(self, purchase_amount):
        return int((self.bonus_percentage / 100) * purchase_amount)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.price is not None and self.discount is not None:
            self.seil_price = self.price - (self.price * self.discount / 100)
        else:
            self.seil_price = None
        super(Item, self).save(*args, **kwargs)

class Category(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name="Название категории")
    parent = models.ForeignKey(
        'self',  # Ссылка на этот же класс (Category)
        on_delete=models.CASCADE,  # Удалять подкатегории, если удалена родительская категория
        blank=True,
        null=True,
        verbose_name="Родительская категория",
    )
    image = models.ImageField(upload_to="categories/images/%Y/%m/%d/", blank=True, null=True)
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title

class CertificateImages(models.Model):
    photo = models.ImageField(upload_to='certificates/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "Сертификат"
        verbose_name_plural = "Сертификаты"


class Brend(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="brends/images/%Y/%m/%d/")
    
    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return self.name



class FavoriteItem(models.Model):
    user = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True,)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    @classmethod
    def count_favorite_items(cls, request):
        if request.user.is_authenticated:
            return FavoriteItem.objects.filter(
                user=request.user,
                ).count()
        if request.session.session_key != None:
            session = get_current_session(request)
            return FavoriteItem.objects.filter(
                session=session,
            ).count()
        return 0

    class Meta:
        unique_together = ('user', 'item')


class CartItem(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, blank=True, null=True, )
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, blank=True, null=True, )
    quantity = models.PositiveIntegerField(default=1, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(
        verbose_name='Товар выбран для заказа в корзине',
        default=True)

    # promocode = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Промокод')

    def total_price_with_discount(self):
        return self.item.seil_price * self.quantity
    
    class Meta:
        unique_together = ('cart', 'item')
        verbose_name = 'Товар корзины'
        verbose_name_plural = 'Товары корзины'

    def __str__(self):
        return self.item.name


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True,)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True,)
    items = models.ManyToManyField(Item, verbose_name='Товары в корзине', through='CartItem')  # Множество элементов корзины
    promocode = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Промокод')

    def distinct_items_count(self):
        return self.cartitem_set.count()

    def total_quantity(self):
        return sum([item.quantity for item in self.cartitem_set.all() if item.is_active])

    def items_price_without_discount(self):
        return sum(item.item.price * item.quantity for item in self.cartitem_set.all() if item.is_active)
    
    def total_discount(self):
        return sum(item.item.price * item.item.discount / 100 * item.quantity 
                   for item in self.cartitem_set.all()
                   if item.is_active
                   )
    
    def total_price(self):
        total_original_price = self.items_price_without_discount()
        total_discount = self.total_discount()
        if self.promocode:
            total_discount += total_original_price * (self.promocode.discount_percent / 100)
        return total_original_price - total_discount

    def __str__(self):
        return f'{self.user if self.user else self.session}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


