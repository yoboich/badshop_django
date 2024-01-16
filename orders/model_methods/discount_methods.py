
class DiscountMethodsMixin:
    
    @property
    def items_discount(self):
        return self.items_price_without_discount \
                - self.items_price_with_discount
    
    def _get_promocode_discount(self):
        price = self.items_price_with_discount *  \
                (100 - self.promocode.discount \
                / 100 - self.promocode
                )
        return price

    @property
    def promocode_discount(self):
        if self.promocode:
            return self._get_promocode_discount()
        else:
            return 0
        
    @property
    def items_price_with_promocode(self):
        return self.items_price_with_discount - self.promocode_discount
    
    @property
    def max_bonus_points_to_use(self):
        return int(.3 * self.items_price_with_promocode)

    def items_price_with_bonuses(self, request):
        if request.user.is_authenticated:
            bonus_points_to_use = \
                min(request.user.bonus_points, 
                    self.max_bonus_points_to_use
                    )
            return self.items_price_with_promocode \
                - bonus_points_to_use
        return self.items_price_with_promocode