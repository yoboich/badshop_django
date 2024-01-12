from django import template
from items.models import Category

register = template.Library()

@register.simple_tag
def category_list():
    return Category.objects.all()