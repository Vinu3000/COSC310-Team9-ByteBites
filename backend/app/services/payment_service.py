class PaymentService:
    def process_payment(self, payment_method, card_number=None):
        if payment_method not in ["card", "cash"]:
            return "Rejected"

        if payment_method == "card":
            if not card_number:
                return "Rejected"
            if card_number.endswith("0000"):
                return "Rejected"

        return "Success"