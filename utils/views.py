from django.shortcuts import render
from django.http import HttpResponse

from badshop_django.logger import logger

def yoo_kassa_webhook_view(request):
    logger.debug(f'yoo_kassa request data = {request.POST}')
    return HttpResponse('')
