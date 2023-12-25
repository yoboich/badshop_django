from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from badshop_django.logger import logger


@method_decorator(csrf_exempt, name='dispatch')
def yoo_kassa_webhook_view(request):
    logger.debug(f'yoo_kassa request data = {request.POST}')
    return HttpResponse('')
