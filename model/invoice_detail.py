from app import db
from model.product import Product


class InvoiceDetail(db.Model):
    __tablename__ = "invoice_details"

    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

    # relationship
    invoice = db.relationship("Invoice", back_populates="details")
    product = db.relationship("Product")

    def to_dict(self, include_product=False):
        data = {
            "id": self.id,
            "invoice_id": self.invoice_id,
            "product_id": self.product_id,
            "qty": self.qty,
            "price": self.price,
            "total": self.total,
        }
        if include_product and self.product:
            data["product"] = self.product.to_dict(include_category=True)
        return data
