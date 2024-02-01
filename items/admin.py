from django.contrib import admin
from django.db import models

from items.models import (
    Item, Category, Brend, 
    CertificateImages, CartItem, 
    Cart, FavoriteItem, ItemImages, 
    UserItem, ActiveBad
)


class CertificateImageInline(admin.TabularInline):  # или `admin.TabularInline` для табличного представления
    model = CertificateImages
    extra = 1
# Register your models here.

class ItemImagesInline(admin.TabularInline):
    model = ItemImages
    extra = 1

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = (CertificateImageInline, ItemImagesInline)
    list_display = ('name', 'price', 'discount', 'bonus_percentage', 'sale_price','views_count', 'category')
    list_filter = ('name', 'price')
    search_fields = ('name', 'price')
    prepopulated_fields = {"slug": ("name",)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)
    list_editable = ('title',)
    search_fields = ('title',)

@admin.register(FavoriteItem)
class FavoriteItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'session', 'date_added')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'session',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'cart', 'date_added')


@admin.register(UserItem)
class UserItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item')

admin.site.register(Category)
admin.site.register(CertificateImages)
admin.site.register(Brend)
admin.site.register(ActiveBad)
