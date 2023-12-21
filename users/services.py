
from badshop_django.logger import logger
from items.services import get_or_create_cart, get_current_session
from items.models import Cart
from django.contrib.auth import authenticate
from items.models import FavoriteItem

def transfer_items_from_session_to_user_cart(request):
    user = get_user_from_auth_form(request)
    session = get_current_session(request)
    session_cart = Cart.objects.get(session=session)
    cart = get_or_create_cart(request, user=user)
    for cart_item in session_cart.cartitem_set.all():
        try:
            cart_item.cart = cart
            cart_item.save()
        except:
            pass


def transfer_items_form_session_to_user_favorites(request):
    user = get_user_from_auth_form(request)
    session = get_current_session(request)
    session_favs = FavoriteItem.objects.filter(
        session=session
        )
    
    for item in session_favs:
        try:
            item.user = user
            item.session = None
            item.save()
        except:
            pass

def get_user_from_auth_form(request):
    email = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(email=email, password=password)
    
    return user