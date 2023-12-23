from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from items.models import CartItem, Cart, Item
from items.services import get_cart_data

from badshop_django.logger import logger

# желательно разделить
def update_cart_ajax(request):
    quantity = int(request.POST.get('quantity'))
    item_id = request.POST.get('item_id')
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.quantity = quantity
    cart_item.save()

    cart_data = get_cart_data(request)
    cart_data.update({'success': 'success'})
    cart_data.update(
        {'total_cart_item_price_with_discount': \
         cart_item.total_price_with_discount()}
         )
    return JsonResponse(cart_data)
    

def toggle_item_active_state_ajax(request):
    cart_item_id = request.POST.get('cart_item_id')
    state = True if request.POST.get('state') == 'true' else False
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.is_active = state
    cart_item.save()

    return JsonResponse({'success':'success'})


def get_cart_data_ajax(request):
    cart_data = get_cart_data(request)
    return JsonResponse(cart_data)


# для модалки при добавлении продукта в корзину
def get_item_data_ajax(request):
    item_id = request.GET.get('item_id')
    item = Item.objects.get(id=item_id)
    cart = Cart.get_or_create_cart(request)
    cart_item, _ = CartItem.objects.get_or_create(
        item=item,
        cart=cart,
        defaults={'quantity': 1}
        )
    logger.debug(f'cart_item: {cart_item.__dict__}')
    
    rendered_item = render_to_string(
        'cart/__item_added_render.html', 
        {'item': cart_item}
        )
    
    return JsonResponse({'success': rendered_item})


import yookassa
from yookassa import Configuration
from yookassa import Payment as yoo_Payment
import uuid
import requests

from .models import Order


def order_page_view(request):
    Order.remove_current_user_unpaid_orders(request)
    order = Order.create_order_for_current_user(request)

    Configuration.account_id = '285619'
    Configuration.secret_key = 'test_pehJPGfr6C3c-BqjXCg7CzYq5PsIDdGjBxu0hwRQGxY'
   
    idempotence_key = str(uuid.uuid4())
   
    
    yoo_payment = yoo_Payment.create({
            "id": "23d93cac-000f-5111-8010-122628f15141",
            "status": "pending",
            "paid": False,
            "amount": {
            "value": "2.00",
            "currency": "RUB"
            },
            "payment_method_data": {
            "type": "bank_card"
            },
            "confirmation": {
            "type": "redirect",
            "return_url": "https://www.example.com/return_url"
            },
            "description": "Order No. 72"
        }, idempotence_key)
    logger.debug(yoo_payment.__dict__)
    logger.debug(yoo_payment._PaymentResponse__confirmation.__dict__)
    return redirect(yoo_payment._PaymentResponse__confirmation._ConfirmationRedirect__confirmation_url)
  

def payment_success_view(request):
    logger.debug(f'request body: {request._body.__dict__}')
    return render(request, 'orders/payment_success.html')