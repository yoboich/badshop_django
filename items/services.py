from django.contrib.sessions.models import Session
from items.models import Cart, FavoriteItem

from utils.services import get_current_session

def get_cart_data(request):
    cart = get_or_create_cart(request)
    total_items_count = cart.total_quantity()
    discount = cart.total_discount()
    total_price = cart.total_price()
    
    total_price_without_discount = cart.items_price_without_discount()
    distinct_items_count = cart.cartitem_set.count()

    cart_data = {
        'total_items_count': total_items_count,
        'total_price_without_discount': total_price_without_discount,
        'discount': discount,
        'total_price': total_price,
        'distinct_items_count': distinct_items_count,
    }
    return cart_data



def get_or_create_cart(request):
    cart = []
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if request.session.session_key != None:
            session = get_current_session(request)
            cart, created = Cart.objects.get_or_create(session=session)

    return cart


def trasfer_cart_items_from_session_to_user(request):

    try:
        session = get_current_session(request)
        session_cart = Cart.objects.get(session=session)
        cart = get_or_create_cart(request)
        for cart_item in session_cart.cartitem_set.all():
            try:
                cart_item.cart = cart
                cart_item.save()
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

    print('!', favorite_item)
    return favorite_item, created