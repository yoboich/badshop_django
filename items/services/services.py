
from django.contrib.sessions.models import Session
from items.models import Cart, FavoriteItem
from utils.services import get_current_session, create_user_or_session_filter_dict

from badshop_django.logger import logger



def get_cart_data(request):
    cart = Cart.get_or_create_cart(request)

    cart_data = {
        'total_items_count': cart.total_quantity,
        'total_price_without_discount': cart.items_price_without_discount,
        'discount': cart.items_discount,
        'total_price': cart.items_price_with_bonuses(request),
        'distinct_items_count': cart.cartitem_set.count(),
    }
    return cart_data



def trasfer_cart_items_from_session_to_user(request):

    try:
        session = get_current_session(request)
        session_cart = Cart.objects.get(session=session)
        cart = Cart.get_or_create_cart(request)
        logger.debug(f'!!cart = {cart}')
        for cart_item in session_cart.cartitem_set.all():
            try:
                cart_item.cart = cart
                cart_item.save()
                logger.debug(cart_item.__dict__)
            except:
                pass
    except:
        pass


def create_or_delete_favorite_item(request, item):
    created = False
    favorite_item = None
    if request.user.is_authenticated:
        favorite_item, created = FavoriteItem.objects.get_or_create(
            user=request.user,
            item=item)
    else:
        if request.session.session_key != None:
            session = get_current_session(request)
            favorite_item, created = FavoriteItem.objects.get_or_create(
                session=session,
                item=item
                )

    if not created and favorite_item != None:
            favorite_item.delete()

    return favorite_item, created