from django.shortcuts import render
from django.http import JsonResponse
from items.models import CartItem, Cart


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
    