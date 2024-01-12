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
    logger.debug(f'yoo_kassa request data = {request.body}')
    body_dict = json.loads(request.body)
    payment_response_id = body_dict['object']['id']
    logger.debug(f'payment_response_id = {payment_response_id}')
    status =body_dict['object']['status']
    if status == 'succeeded':
        
        try:
            order = Order.objects.get(payment_response_id=payment_response_id)
        except:
            logger.error("Order doesn't exist")
            return

        if order.status == 'OP':
            logger.debug(f'order already paid. duplicate request!')
            return HttpResponse('')

        order.status = 'OP'
        order.save()
        

        Cart.delete_cart_for_paid_order(order)
        Payment.objects.create(
            order=order,
            payment_amount=order.total_price
        )
        
        if not order.user:
            logger.debug(f"order user doesn't exist, creating new one. current user is {request.user}")
            user, created = CustomUser.create_account_for_unathourized_user(
                order.email
                )
            if created:
                password_reset_for_new_user(request, order.email)
            order.user = user
            order.save()
        logger.debug(f'order.total_bonus_points = {order.total_bonus_points()}')
        user.bonus_points += order.total_bonus_points()
        user.save()
        logger.debug(f'user = {user}')
        logger.debug(f'bonus_points = {user.bonus_points}')
        message = f'Ура! Ваш платеж прошел успешно. Скоро мы доставим ваши покупки.'
        title = f'Ваша покупка на Vitanow'
        email = EmailMessage(title, message, "no-reply@vitanow.ru", [order.email])
        email.send()

        return HttpResponse('')
    

