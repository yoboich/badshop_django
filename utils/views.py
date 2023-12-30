import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.mail import EmailMessage

from badshop_django.logger import logger

from orders.models import Order, Payment
from items.models import Cart
from users.models import CustomUser
from utils.services import password_reset_for_new_user


@method_decorator(csrf_exempt, name='dispatch')
def yoo_kassa_webhook_view(request):
    print('!here - yoo_kassa_webhook_view')
    logger.debug(f'yoo_kassa request data = {request.body}')
    body_dict = json.loads(request.body)
    order_outer_id = body_dict['object']['id']
    logger.debug(f'order_outer_id = {order_outer_id}')
    status =body_dict['object']['status']
    if status == 'succeeded':
        
        try:
            order = Order.objects.get(outer_id=order_outer_id)
        except:
            logger.error("Order doesn't exist")
            return

        order.status = 'OP'
        order.save()
        

        Cart.delete_cart_for_paid_order(order)
        Payment.objects.create(
            order=order,
            amount=order.total_price()
        )
        
        if not request.user.is_authenticated:
            CustomUser.create_account_for_unathourized_user(order.email)
            password_reset_for_new_user(request, order.email)

        message = f'Ура! Ваш платеж прошел успешно. Скоро мы доставим ваши покупки.'
        title = f'Ваша покупка на Vitanow'
        email = EmailMessage(title, message, "no-reply@vitanow.ru", [order.email])
        email.send()

        return HttpResponse('')
    

