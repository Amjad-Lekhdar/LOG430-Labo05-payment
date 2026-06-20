import pytest
from flask import Flask
import json
from payments_api import app

# Assuming your Flask app is importable as 'app' from your main module
# from your_app_module import app

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_payment(client):
    """Smoke test for POST /payments - Create a new payment"""
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

def test_process_payment(client):
    """Smoke test for POST /payments/process/<payment_id> - Process a payment"""
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
    

def test_get_payment(client):
    """Smoke test for GET /payments/<payment_id> - Retrieve payment details"""
    payment_id = 1  
    response = client.get(f'/payments/{payment_id}')
    assert response.status_code in [200, 201], f"Expected 200 or 201, got {response.status_code}"
    