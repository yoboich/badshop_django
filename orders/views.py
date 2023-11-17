from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from items.models import CartItem, Cart, Item


def update_cart_ajax(request):
    quantity = int(request.POST.get('quantity'))
    item_id = request.POST.get('item_id')
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.quantity = quantity
    cart_item.save()

    print(cart_item.quantity)

    cart = Cart.objects.get(user=request.user)
    total_items_count = cart.calculate_total_items_count()
    discount = cart.calculate_total_discount()
    total_price = cart.calculate_total_price()
    total_price_without_discount = cart.calculate_items_price_without_discount()
    
    return JsonResponse({
        'success': 'success',
        'total_items_count': total_items_count,
        'total_price_without_discount': total_price_without_discount,
        'discount': discount,
        'total_price': total_price}
        )
    

def get_item_data_ajax(request):
    item_id = request.GET.get('item_id')
    item = CartItem.objects.get(
        item=Item.objects.get(id=item_id)
        )
    
    rendered_item = render_to_string(
        'cart/__item_added_render.html', 
        {'item': item}
        )
    
    return JsonResponse({'success': rendered_item})