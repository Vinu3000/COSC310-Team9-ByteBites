class PricingService:
    TAX_RATE = 0.05
    DELIVERY_FEE = 5.00

    def calculate_subtotal(self, items):
        subtotal = 0.0
        for item in items:
            subtotal += item["unit_price"] * item["quantity"]
        return round(subtotal, 2)

    def calculate_taxes(self, subtotal):
        return round(subtotal * self.TAX_RATE, 2)

    def calculate_delivery_fee(self):
        return self.DELIVERY_FEE

    def calculate_total(self, items):
        subtotal = self.calculate_subtotal(items)
        delivery_fee = self.calculate_delivery_fee()
        taxes = self.calculate_taxes(subtotal)
        total = round(subtotal + delivery_fee + taxes, 2)

        return {
            "subtotal": subtotal,
            "delivery_fee": delivery_fee,
            "taxes": taxes,
            "total": total
        }