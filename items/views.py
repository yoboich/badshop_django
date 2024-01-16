from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from items.forms import AddItemForm
from items.models import Item, FavoriteItem, CartItem

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

from items.services.services import (
    get_current_session, create_or_delete_favorite_item
)



from django.http import JsonResponse

class AddToCartView(View):
    def get(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        cart = request.session.get('cart', {})

        cart[item_id] = cart.get(item_id, 0) + 1
        request.session['cart'] = cart

        if request.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user, 
                item=item
                )
            cart_item.quantity = (cart_item.quantity if not created else 0) + 1
            cart_item.save()

        return JsonResponse({'message': 'Товар добавлен в корзину'})
    


def toggle_item_favorite_state_ajax(request):
    item_id = request.POST.get('item_id')
    item = get_object_or_404(Item, id=item_id)
    favorite_item, created = create_or_delete_favorite_item(
        request, item
        )
    
    return JsonResponse({
        'created': created,
        })
    

def get_favorite_total_count_ajax(request):
    favorite_total_count = FavoriteItem.count_favorite_items(request)
    return JsonResponse({'favorite_total_count': favorite_total_count})