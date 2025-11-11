from flask import request
from app import app, db
from model.invoice import Invoice
from model.invoice_detail import InvoiceDetail


# create invoice
@app.post("/invoice/create")
def create_invoice():
    data = request.get_json(silent=True) or request.form
    if not data:
        return {"error": "Missing data"}, 400

    invoice_no = data.get("invoice_no")
    customer_name = data.get("customer_name")

    if not invoice_no or not customer_name:
        return {"error": "Missing required fields"}, 400

    existing = Invoice.query.filter_by(invoice_no=invoice_no).first()
    if existing:
        return {"error": "Invoice number already exists"}, 400

    invoice = Invoice(invoice_no=invoice_no, customer_name=customer_name)
    db.session.add(invoice)
    db.session.commit()

    return {"message": "Invoice created", "invoice": invoice.to_dict()}, 200


# view invoice list
@app.get("/invoice/list")
def list_invoices():
    invoices = Invoice.query.order_by(Invoice.created_at.desc()).all()
    return [inv.to_dict() for inv in invoices], 200


# view invoice by id (with details)
@app.get("/invoice/list-by-id/<int:invoice_id>")
def get_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        return {"error": "Invoice not found"}, 404
    return invoice.to_dict(include_details=True), 200


# delete invoice
@app.delete("/invoice/delete/<int:invoice_id>")
def delete_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        return {"error": "Invoice not found"}, 404

    db.session.delete(invoice)
    db.session.commit()
    return {"message": "Invoice deleted successfully"}, 200
