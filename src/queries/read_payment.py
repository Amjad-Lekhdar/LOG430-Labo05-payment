"""
Payment (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from db import get_sqlalchemy_session
from models.payment import Payment

def get_payment_by_id(payment_id):
    """Get payment by ID """
    session = get_sqlalchemy_session()
    result = session.query(Payment).filter_by(id=payment_id).all()

    if len(result):
        return {
            "id": result[0].id,
            "order_id": result[0].order_id,
            "user_id": result[0].user_id,
            "total_amount": result[0].total_amount,
            "is_paid": result[0].is_paid,
        }
    else:
        return {}

