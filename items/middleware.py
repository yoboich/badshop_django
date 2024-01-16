
from .models import CartItem, FavoriteItem, Item, Cart 
from .services.services import trasfer_cart_items_from_session_to_user

from badshop_django.logger import logger


class AddToDatabaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        return response
    

class InitSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.session['hey'] = 'hello'
        response = self.get_response(request)

        return response