from app.services.pricing_service import PricingService


def test_calculate_total():
    service = PricingService()

    items = [
        {"unit_price": 10.0, "quantity": 2},
        {"unit_price": 5.0, "quantity": 1}
    ]

    result = service.calculate_total(items)

    assert result["subtotal"] == 25.0
    assert result["delivery_fee"] == 5.0
    assert result["taxes"] == 1.25
    assert result["total"] == 31.25
