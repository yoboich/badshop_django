import uuid

from yookassa import Configuration
from yookassa import Payment as yoo_Payment

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from utils.services import get_current_session, create_user_or_session_filter_dict

from .models import Order
from items.models import Cart
from badshop_django.logger import logger

# creating new order and removing previous unpaid orders
     

def create_yoo_kassa_payment(order):
    Configuration.account_id = '285619'
    Configuration.secret_key = 'test_pehJPGfr6C3c-BqjXCg7CzYq5PsIDdGjBxu0hwRQGxY'
    print('!!', order)
    idempotence_key = str(order.outer_id)
    return_url = 'https://vitanow.ru' + reverse_lazy('payment_finished')
    yoo_payment = yoo_Payment.create({
            "id": order.outer_id,
            "status": "pending",
            "paid": False,
            "capture": True,
            "amount": {
            "value": order.total_price,
            "currency": "RUB"
            },
            "payment_method_data": {
            "type": "bank_card"
            },
            "confirmation": {
            "type": "redirect",
            "return_url": return_url
            },
            "description": ""
        }, idempotence_key)
    
    logger.debug(yoo_payment.__dict__)
    logger.debug(yoo_payment._PaymentResponse__confirmation.__dict__)
    if yoo_payment._PaymentResponse__status == 'pending' \
    and yoo_payment._PaymentResponse__paid == False:
        return True, yoo_payment
    return False, False
    

def get_payment_status(request):
    Configuration.account_id = '285619'
    Configuration.secret_key = 'test_pehJPGfr6C3c-BqjXCg7CzYq5PsIDdGjBxu0hwRQGxY'
