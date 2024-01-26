import datetime
import json

from django import template
from items.models import FavoriteItem, Cart, CartItem
from utils.services import get_current_session


register = template.Library()



@register.filter
def get_favorite_status(item, request):
    fav_item = []
    if request.user.is_authenticated:
        fav_item = FavoriteItem.objects.filter(
            user=request.user,
            item=item
            )
    else:
        if request.session.session_key != None:
            session = get_current_session(request)
            fav_item = FavoriteItem.objects.filter(
                session=session,
                item=item
                )
    return bool(fav_item)



@register.filter
def check_if_item_in_cart(item, request):
    cart = Cart.get_or_create_cart(request)
    cart_items = CartItem.objects \
        .filter(cart=cart) \
        .values_list('item', flat=True)
    if item.id in cart_items:
        return True
    return False


@register.filter
def get_cart_items(request):
    cart = Cart.get_or_create_cart(request)
    cart_items = CartItem.objects \
        .filter(cart=cart) \
        .values_list('item', flat=True)
    return cart_items


@register.filter
def get_items_price_with_bonuses(obj, request):
    return obj.items_price_with_bonuses(request)


@register.filter
def get_max_bonus_points_to_use(obj, request):
    return obj.max_bonus_points_to_use(request)