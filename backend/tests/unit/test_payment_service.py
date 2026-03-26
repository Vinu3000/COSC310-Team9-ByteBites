from app.services.payment_service import PaymentService


def test_payment_success():
    service = PaymentService()
    result = service.process_payment("card", "12345678")
    assert result == "Success"


def test_payment_rejected_invalid_card():
    service = PaymentService()
    result = service.process_payment("card", "99990000")
    assert result == "Rejected"


def test_payment_rejected_invalid_method():
    service = PaymentService()
    result = service.process_payment("bitcoin")
    assert result == "Rejected"