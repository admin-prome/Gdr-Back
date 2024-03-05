from sqlalchemy import Column, Integer, String, Boolean
from source.jiraModule.utils.conexion.db import Base

class QuotaAmountOneMillion(Base):
    __tablename__ = 'quotaAmountOneMillion'
    
    id = Column(Integer, primary_key=True)
    dni = Column(Integer, nullable=False)
    opportunity = Column(String(255), nullable=False)
    executive = Column(String(255), nullable=False)
    quotaValue = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    notified = Column(Boolean, default=False)

    def __init__(self, dni, opportunity, executive, quotaValue, amount, notified):
        self.dni = dni
        self.opportunity = opportunity
        self.executive = executive
        self.quotaValue = quotaValue
        self.amount = amount
        self.notified = notified

    def __str__(self):
        return f"QuotaAmountOneMillion(ID: {self.id}, DNI: {self.dni}, Opportunity: {self.opportunity}, Executive: {self.executive}, QuotaValue: {self.quotaValue}, Amount: {self.amount}, Notified: {self.notified})"

    def __repr__(self):
        return f"QuotaAmountOneMillion(id={self.id}, dni={self.dni}, opportunity='{self.opportunity}', executive='{self.executive}', quotaValue={self.quotaValue}, amount={self.amount}, notified={self.notified})"
