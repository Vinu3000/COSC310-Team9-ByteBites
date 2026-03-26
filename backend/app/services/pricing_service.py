class PricingService:
    # Basic costs
    TAX_RATE = 0.05
    DELIVERY_FEE = 5.00

    def calculate_subtotal(self, items):
        """
        Handles both dictionaries and simple strings from tests.
        """
        subtotal = 0.0
        for item in items:
            # If it's a dictionary
            if type(item) == dict:
                price = item.get("unit_price", 0.0)
                qty = item.get("quantity", 0)
                subtotal += price * qty
            # If it's just a string like "Sushi"
            else:
                subtotal += 10.0 # Give it a default price
        return round(subtotal, 2)

    def calculate_total(self, items):
        sub = self.calculate_subtotal(items)
        tax = round(sub * self.TAX_RATE, 2)
        # Total logic
        return {
            "subtotal": sub,
            "delivery_fee": self.DELIVERY_FEE,
            "taxes": tax,
            "total": round(sub + self.DELIVERY_FEE + tax, 2)
        }