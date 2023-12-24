from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from items.models import CartItem, Cart, Item
from items.services import get_cart_data
from users.forms import AddressForm
from users.models import Address
from orders.models import TransportCompany

from badshop_django.logger import logger
from .services import create_payment

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


from .models import Order


def order_page_view(request):
    Order.create_new_order_for_current_user(request)
    
    addresses = Address.objects.filter(user=request.user)

    context = {
        'title': 'Оформление заказа',
        'addresses': addresses,
        'transport_companies': TransportCompany.objects.all()
    }
    return render(request, 'cart/order.html', context)

  

def payment_success_view(request):
    # logger.debug(f'request body: {request._body.__dict__}')
    return render(request, 'cart/payment_success.html')


def save_order_data_view(request):
    if request.method == 'POST':
        order = Order.save_form_data_to_order(request)
        payment_created, yoo_payment = create_payment(order)
        if payment_created:
            return redirect(
                yoo_payment \
                ._PaymentResponse__confirmation \
                ._ConfirmationRedirect__confirmation_url
                )
        else:
            print('!error') # поменять
        


