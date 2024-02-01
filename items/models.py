import uuid

from slugify import slugify

from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User  # Для авторизованных пользователей
from django.contrib.sessions.models import Session  # Для неавторизованных пользователей
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from badshop_django.logger import logger
from balance.models import PromoCode
from users.models import CustomUser
from utils.services import get_current_session, create_user_or_session_filter_dict
from .model_methods.cart_methods import CartMethodsMixin
from orders.model_methods.discount_methods import DiscountMethodsMixin


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название товара")
    image = models.ImageField(upload_to="items/%Y/%m/%d/", blank=True, null=True, verbose_name="Превью Изображение товара")
    price = models.IntegerField(default=0, blank=True, null=True, verbose_name="Цена товара")
    discount = models.IntegerField(default=0, blank=True, null=True, verbose_name="Скидка %")
    views_count = models.IntegerField(default=0, verbose_name="Количество просмотров")
    rating = models.IntegerField(default=0, blank=True, null=True, verbose_name="Рэйтинг")
    text = RichTextField(blank=True, null=True, verbose_name="Описание товара")
    compound = RichTextField(blank=True, null=True, verbose_name="Состав товара")
    delivery = RichTextField(blank=True, null=True, verbose_name="Информация о доставке")
    category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.CASCADE, verbose_name="Категория")
    brend = models.ForeignKey('Brend', blank=True, null=True, on_delete=models.CASCADE, verbose_name="Бренд")
    active_bad = models.ForeignKey('Bads', blank=True, null=True, on_delete=models.CASCADE, verbose_name='Активное вещество')
    slug = models.SlugField('Слаг',
        default='',
        max_length=500,
        blank=True, null=True,
        help_text='Оставьте пустым, оно само генерируется при заполнении названия'
    )

    bonus_percentage = models.FloatField(
        default=15, 
        verbose_name="Процент бонусных баллов"
        )

    def item_discount(self):
        return int(self.price * self.discount / 100)

    @property
    def sale_price(self):
        return int(self.price - self.item_discount())

    def calculate_bonus_points(self, purchase_amount):
        return int((self.bonus_percentage / 100) * purchase_amount)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name
    
    def unique_slug_generator(self, new_slug=None):
        if new_slug is not None:
            slug = new_slug
        else:
            slug = slugify(self.name)

        slug_exists = self.__class__.objects.filter(slug=slug).exists()
        if slug_exists:
            new_slug = "{slug}-{randstr}".format(
                slug=slug,
                randstr=str(uuid.uuid4())[:4]
            )
            return self.unique_slug_generator(new_slug=new_slug)

        self.slug = slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.unique_slug_generator()

        super().save(*args, **kwargs)


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





class Bads(models.Model):
    title = models.CharField(max_length=255, verbose_name='Активное вещество')
    
    class Meta:
        verbose_name = 'Активное вещество'
        verbose_name_plural = 'Активные вещества'

    def __str__(self) -> str:
        return self.title

class CertificateImages(models.Model):
    #########photo = models.ImageField(upload_to='certificates/%Y/%m/%d/', blank=True, null=True)
    certificate = models.FileField(upload_to='certificates/%Y/%m/%d/', blank=True, null=True, verbose_name='PDF Сертификат (не изображение!)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "PDF Сертификат"
        verbose_name_plural = "PDF Сертификаты"


class ItemImages(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True, null=True, verbose_name='Только PNG фото!')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return self.item.name
    
    class Meta:
        verbose_name = 'PNG Фото товара'
        verbose_name_plural = 'PNG Фото товаров'


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
    def get_favorite_items(cls, request):
        if request.user.is_authenticated:
            f_items = FavoriteItem.objects.filter(
                user=request.user,
                )
        elif request.session.session_key != None:
            session = get_current_session(request)
            f_items = FavoriteItem.objects.filter(
                session=session,
            )
        items = Item.objects.filter(
            id__in=f_items.values('item__id')
            )
        return items

    @classmethod
    def count_favorite_items(cls, request):
        
        return cls.get_favorite_items(request).count()  

    class Meta:
        unique_together = ('user', 'item')
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'


class CartItem(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, blank=True, null=True, )
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, blank=True, null=True, )
    quantity = models.PositiveIntegerField(default=1, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(
        verbose_name='Товар выбран для заказа в корзине',
        default=True)

    promocode = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Промокод')

    def total_price_with_discount(self):
        return self.item.sale_price * self.quantity
    
    class Meta:
        unique_together = ('cart', 'item')
        verbose_name = 'Товар корзины'
        verbose_name_plural = 'Товары корзины'

    def __str__(self):
        return self.item.name


class Cart(CartMethodsMixin, DiscountMethodsMixin, models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True,)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True,)
    # items = models.ManyToManyField(CartItem, verbose_name='Товары в корзине', through='CartItem')  # Множество элементов корзины
    promocode = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Промокод')

    
    def __str__(self):
        return f'{self.user if self.user else self.session}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


