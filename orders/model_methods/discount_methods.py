
class DiscountMethodsMixin:
    
    @property
    def items_discount(self):
        return self.items_price_without_discount \
                - self.items_price_with_discount
    
    def _get_promocode_discount(
            self,
            promocode_discount_percentage
        ):
        price = self.items_price_with_discount \
                * promocode_discount_percentage \
                / 100
        return price

    @property
    def promocode_discount(self):
        # для корзины
        if self.promocode:
            promocode_discount_percentage = self.promocode.discount
        # для заказа
        elif hasattr(self, 'promocode_discount_percentage'):
            promocode_discount_percentage = self.promocode_discount
        
        try:
            return self._get_promocode_discount(
                promocode_discount_percentage
                )
        # для корзины, если промокод не применяется
        except:
            return 0
        
    @property
    def items_price_with_promocode(self):
        return self.items_price_with_discount - self.promocode_discount
    
    def max_bonus_points_to_use(self, request):
        if request.user.is_authenticated:
            return min(request.user.bonus_points, 
                int(.3 * self.items_price_with_promocode)
                )
        else:
            return 0

    def items_price_with_bonuses(self, request):
        return self.items_price_with_promocode \
            - self.max_bonus_points_to_use(request)