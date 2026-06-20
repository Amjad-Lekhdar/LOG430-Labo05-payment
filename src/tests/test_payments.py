import pytest
import json
from controllers import payment_controller
from payments_api import app

# Assuming your Flask app is importable as 'app' from your main module
# from your_app_module import app

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_payment(client, monkeypatch):
    """Smoke test for POST /payments - Create a new payment"""
    monkeypatch.setattr("payments_api.add_payment", lambda request: {"payment_id": 1})

    payload = {
        "user_id": 1,
        "order_id": 999,
        "total_amount": 123.45
    }
    
    response = client.post(
        '/payments',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code in [200, 201], f"Expected 200 or 201, got {response.status_code}"
    assert response.json is not None, "Response should contain JSON data"

def test_process_payment(client, monkeypatch):
    """Smoke test for POST /payments/process/<payment_id> - Process a payment"""
    monkeypatch.setattr(
        "payments_api.process_payment",
        lambda payment_id, credit_card_data: {"order_id": 999, "payment_id": payment_id, "is_paid": True},
    )

    payment_id = 1 
    payload = {
        "cardNumber": 9999999999999,
        "cardCode": 123,
        "expirationDate": "2030-01-05"
    }
    response = client.post(f'/payments/process/{payment_id}',
                                data=json.dumps(payload),
                                content_type='application/json')
    assert response.status_code in [200, 201], f"Expected 200 or 201, got {response.status_code}"
    

def test_get_payment(client, monkeypatch):
    """Smoke test for GET /payments/<payment_id> - Retrieve payment details"""
    monkeypatch.setattr(
        "payments_api.get_payment",
        lambda payment_id: {"order_id": 999, "payment_id": payment_id, "is_paid": True},
    )

    payment_id = 1  
    response = client.get(f'/payments/{payment_id}')
    assert response.status_code in [200, 201], f"Expected 200 or 201, got {response.status_code}"
    
def test_update_order_calls_store_manager(monkeypatch):
    """PUT /orders is called with the order payment status."""
    calls = {}

    class FakeResponse:
        def raise_for_status(self):
            calls["raise_for_status"] = True

        def json(self):
            return {"updated": True}

    def fake_put(url, json, headers, timeout):
        calls["url"] = url
        calls["json"] = json
        calls["headers"] = headers
        calls["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr(payment_controller.config, "STORE_MANAGER_ORDERS_URL", "http://gateway/store-manager-api/orders")
    monkeypatch.setattr(payment_controller.requests, "put", fake_put)

    result = payment_controller.update_order(12, True)

    assert result == {"updated": True}
    assert calls["url"] == "http://gateway/store-manager-api/orders"
    assert calls["json"] == {"order_id": 12, "is_paid": True}
    assert calls["headers"] == {'Content-Type': 'application/json'}
    assert calls["timeout"] == 5
    assert calls["raise_for_status"] is True

def test_process_payment_updates_order_after_local_payment(monkeypatch):
    """Processing a payment propagates is_paid=True to Store Manager."""
    calls = {}

    monkeypatch.setattr(payment_controller, "_process_credit_card_payment", lambda credit_card_data: None)
    monkeypatch.setattr(
        payment_controller,
        "update_status_to_paid",
        lambda payment_id: {"payment_id": payment_id, "order_id": 44, "is_paid": True},
    )

    def fake_update_order(order_id, is_paid):
        calls["order_id"] = order_id
        calls["is_paid"] = is_paid
        return {"updated": True}

    monkeypatch.setattr(payment_controller, "update_order", fake_update_order)

    result = payment_controller.process_payment(7, {"cardNumber": 9999999999999})

    assert result == {"order_id": 44, "payment_id": 7, "is_paid": True}
    assert calls == {"order_id": 44, "is_paid": True}
