from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string

from django.contrib.auth.forms import PasswordResetForm
from django.http import HttpRequest
from django.http import HttpResponse
from django.core.mail import EmailMessage

from items.models import CartItem, Cart, Item
from items.services.services import get_cart_data
from users.forms import AddressForm
from users.models import Address
from orders.models import TransportCompany

from badshop_django.logger import logger
from .services import create_yoo_kassa_payment
from balance.models import PromoCode
from items.models import Cart

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
    
    if request.method == 'POST':
        address_form = AddressForm(request.POST, initial={'user': request.user})
        if address_form.is_valid():
            address_form.save()
            return redirect('myadress')  # Перенаправление на список адресов после успешного сохранения
    else:
        address_form = AddressForm(initial={'user': request.user})
        


    order = Order.create_new_order_for_current_user(request)
    logger.debug(f'order.status when created = {order.status}')
    if request.user.is_authenticated:
        addresses = Address.objects.filter(user=request.user)
    else: 
        addresses = []
    context = {
        'title': 'Оформление заказа',
        'addresses': addresses,
        'transport_companies': TransportCompany.objects.all(),
        'address_form': address_form,
        'order': order,
    }
    return render(request, 'cart/order.html', context)

  
def save_order_data_view(request):
    if request.method == 'POST':
        order = Order.save_form_data_to_order(request)
        payment_created, yoo_payment = create_yoo_kassa_payment(order)
        if payment_created:
            logger.debug(f'order status when order is saved = {order.status}')
            return redirect(
                yoo_payment \
                ._PaymentResponse__confirmation \
                ._ConfirmationRedirect__confirmation_url
                )
        else:
            logger.debug('!error') # поменять
        

def payment_finished_view(request):
    return render(request, 'cart/payment_finished.html')


def apply_promocode_ajax(request):
    code = request.POST.get('promocode')
    try:
        promocode = PromoCode.objects.get(code=code)
    except:
        return JsonResponse({'error': 'Неверный код'})
    
    cart = Cart.get_or_create_cart(request)
    if cart.promocode:
        return JsonResponse({'error': 'Вы уже активировали промокод'})
    cart.promocode = promocode
    cart.save()
    result = {
        'success': 'Промокод активирован',
        'promocode_discount': cart.promocode_discount,
        'bonus_discount': cart.max_bonus_points_to_use(request),
        'price_with_bonuses': cart.items_price_with_bonuses(request),
    }

    return JsonResponse(result)


def delete_cart_item_ajax(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        cart_item = get_object_or_404(
            CartItem, 
            id=cart_item_id
            )
        try:
            cart_item.delete()
            cart_data = get_cart_data(request)
            cart_data.update({'result': 'success'})
            return JsonResponse(cart_data)
        except Exception as e:
            logger.debug(
                f'Ошибка при удалении товара из корзины - {e}'
                )
            return JsonResponse({'result': 'error'})
        
        

        