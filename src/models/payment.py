"""
Payment class 
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from sqlalchemy import Column, Integer, Float, Boolean
from models.base import Base

class Payment(Base):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    is_paid = Column(Boolean, nullable=False)
