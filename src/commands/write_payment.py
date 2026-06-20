"""
Payments (write-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from models.payment import Payment
from db import get_sqlalchemy_session

def create_payment(order_id: int, user_id: int, total_amount: float):
    """Insert payment with items in MySQL"""
    if not order_id or not user_id or not total_amount or float(total_amount) <= 0:
        raise ValueError("Vous devez indiquer un ID commande, ID utilisateur et valeur pour le paiement.")
    
    session = get_sqlalchemy_session()

    try: 
        new_payment = Payment(order_id=order_id, user_id=user_id, total_amount=total_amount, is_paid=False)
        session.add(new_payment)
        session.flush() 
        session.commit()
        return new_payment.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def update_status_to_paid(payment_id: int):
    """Update payment status to paid in MySQL"""
    if not payment_id:
        raise ValueError("Vous devez indiquer un ID de paiement.")
    
    session = get_sqlalchemy_session()

    try:
        # Find the payment by ID
        payment = session.query(Payment).filter(Payment.id == payment_id).first()
        
        if not payment:
            raise ValueError(f"Aucun paiement trouvé avec l'ID {payment_id}")
        
        # Update the payment status
        payment.is_paid = True
        session.commit()
        
        return {
            "payment_id": payment_id,
            "order_id": payment.order_id,
            "is_paid": True
        }
        
    except Exception as e:
        session.rollback()
        return {
            "payment_id": payment_id,
            "order_id": payment.order_id,
            "is_paid": False,
            "error": e
        }
    finally:
        session.close()
