from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from badshop_django.logger import logger
from yookassa import Configuration, Webhook
from yookassa import Payment as yoo_Payment


@method_decorator(csrf_exempt, name='dispatch')
def yoo_kassa_webhook_view(request):
    Configuration.account_id = '285619'
    Configuration.secret_key = 'test_pehJPGfr6C3c-BqjXCg7CzYq5PsIDdGjBxu0hwRQGxY'


    response = Webhook.add({
        "event": "payment.succeeded",
        "url": "https://vitanow.ru/test_yoo_kassa_response/",
    })
    logger.debug(f'yoo_kassa SDK data = {response}')
    logger.debug(f'yoo_kassa request data = {request.GET}')
    return HttpResponse('')
