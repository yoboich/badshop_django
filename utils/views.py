import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse

from yookassa import Configuration, Webhook
from yookassa import Payment as yoo_Payment
from yookassa.domain.notification import WebhookNotification
from badshop_django.logger import logger

@method_decorator(csrf_exempt, name='dispatch')
def yoo_kassa_webhook_view(request):

    logger.debug(f'yoo_kassa request data = {request.body}')
    event_json = json.loads(request.body)
    try:
        notification_object = WebhookNotification(event_json)
    except Exception:
        pass

    # Получите объекта платежа
    payment = notification_object.object
    logger.debug(f'yoo_kassa payment object = {payment}')
