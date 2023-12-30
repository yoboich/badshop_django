from django.contrib import admin

from orders.models import Order, OrderStatus, Payment, AppliedPromoCode, TransportCompany

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'date_created', 'status', 'outer_id', 'payment_response_id')
    readonly_fields = ('outer_id', 'payment_response_id')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_amount', 'payment_date',)

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderStatus)
admin.site.register(AppliedPromoCode)
admin.site.register(TransportCompany)