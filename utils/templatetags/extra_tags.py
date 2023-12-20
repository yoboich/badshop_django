import datetime
import json

from django import template
from items.models import FavoriteItem
from utils.services import get_current_session


register = template.Library()



@register.filter
def get_favorite_status(item, request):
    fav_item = []
    if request.user.is_authenticated:
        fav_item = FavoriteItem.objects.filter(
            user=request.user,
            item=item
            )
    else:
        if request.session.session_key != None:
            session = get_current_session(request)
            fav_item = FavoriteItem.objects.filter(
                session=session,
                item=item
                )
    return bool(fav_item)