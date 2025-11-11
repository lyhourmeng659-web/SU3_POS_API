from app import db
from datetime import datetime


class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)
    invoice_no = db.Column(db.String(50), unique=True, nullable=False)
    customer_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationship
    details = db.relationship("InvoiceDetail", back_populates="invoice", cascade="all, delete-orphan")

    def to_dict(self, include_details=False):
        data = {
            "id": self.id,
            "invoice_no": self.invoice_no,
            "customer_name": self.customer_name,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        if include_details:
            data["details"] = [d.to_dict(include_product=True) for d in self.details]
        return data
