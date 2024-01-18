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
    logger.debug(f'order.outer_id = {order.outer_id}')
    idempotence_key = str(uuid.uuid4())
    return_url = 'https://vitanow.ru' + reverse_lazy('payment_finished')
    logger.debug(f'order total price = {order.items_price_with_bonuses}')
    # items_list = create_items_list_for_yookass_receipt()
    items = order.orderitem_set.all()
    receipt_items = []
    # get_order_item_final_price
    for item in items:
        {
        "description": item.item.name,
        "quantity": item.quantity,
        "amount": {
            "value": item.quantity * item.price,
            "currency": "RUB"
        },
        "vat_code": "3",
        "payment_mode": "full_prepayment",
        "payment_subject": "marked",
        "mark_mode": "0",
        "mark_code_info":
            {
                "gs_1m": "DFGwNDY0MDE1Mzg2NDQ5MjIxNW9vY2tOelDFuUFwJh05MUVFMDYdOTJXK2ZaMy9uTjMvcVdHYzBjSVR3NFNOMWg1U2ZLV0dRMWhHL0UrZi8ydkDvPQ=="
            },
        "measure": "piece"
    }
    yoo_payment = yoo_Payment.create({
            "id": order.outer_id,
            "status": "pending",
            "paid": False,
            "capture": True,
            "amount": {
            "value": order.items_price_with_bonuses,
            "currency": "RUB"
            },
            "payment_method_data": {
            "type": "bank_card"
            },
            "confirmation": {
            "type": "redirect",
            "return_url": return_url
            },
            "receipt": {
                "customer": {
                    "email": "freelance-100@mail.ru"
                },
                "items": [
                    {
                        "description": "Топ трикотажный",
                        "quantity": "1.00",
                        "amount": {
                            "value": order.items_price_with_bonuses,
                            "currency": "RUB"
                        },
                        "vat_code": "3",
                        "payment_mode": "full_prepayment",
                        "payment_subject": "marked",
                        "mark_mode": "0",
                        "mark_code_info":
                            {
                                "gs_1m": "DFGwNDY0MDE1Mzg2NDQ5MjIxNW9vY2tOelDFuUFwJh05MUVFMDYdOTJXK2ZaMy9uTjMvcVdHYzBjSVR3NFNOMWg1U2ZLV0dRMWhHL0UrZi8ydkDvPQ=="
                            },
                        "measure": "piece"
                    }
                   
                ]
            },
            "description": ""
        }, idempotence_key)
    logger.debug(f'!!!')
    logger.debug(f'yoo_payment.dict - {yoo_payment.__dict__}')
    logger.debug(f'yoo_payment._PaymentResponse__confirmation.__dict__ =' \
                 f' {yoo_payment._PaymentResponse__confirmation.__dict__}'
                 )
    order.payment_response_id = yoo_payment._PaymentResponse__id
    order.save()
    if yoo_payment._PaymentResponse__status == 'pending' \
    and yoo_payment._PaymentResponse__paid == False:
        return True, yoo_payment
    return False, False
    

def get_payment_status(request):
    Configuration.account_id = '285619'
    Configuration.secret_key = 'test_pehJPGfr6C3c-BqjXCg7CzYq5PsIDdGjBxu0hwRQGxY'
