from flask import request
from app import app, db
from model.invoice import Invoice
from model.invoice_detail import InvoiceDetail
from model.product import Product


# create sale (invoice detail)
@app.post("/invoice_detail/create")
def create_invoice_detail():
    data = request.get_json(silent=True) or request.form
    if not data:
        return {"error": "Missing data"}, 400

    invoice_id = data.get("invoice_id")
    product_id = data.get("product_id")
    qty = data.get("qty")
    price = data.get("price")

    if not all([invoice_id, product_id, qty, price]):
        return {"error": "Missing fields"}, 400

    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        return {"error": "Invoice not found"}, 404

    product = Product.query.get(product_id)
    if not product:
        return {"error": "Product not found"}, 404

    qty = int(qty)
    price = float(price)
    total = qty * price

    detail = InvoiceDetail(invoice_id=invoice_id, product_id=product_id, qty=qty, price=price, total=total)
    db.session.add(detail)
    db.session.commit()

    return {"message": "Sale added", "detail": detail.to_dict(include_product=True)}, 200


# update sale detail
@app.post("/invoice_detail/update")
def update_invoice_detail():
    data = request.get_json(silent=True) or request.form
    if not data:
        return {"error": "Missing data"}, 400

    detail_id = data.get("id")
    if not detail_id:
        return {"error": "Missing id"}, 400

    detail = InvoiceDetail.query.get(detail_id)
    if not detail:
        return {"error": "Detail not found"}, 404

    qty = data.get("qty")
    price = data.get("price")

    if qty: detail.qty = int(qty)
    if price: detail.price = float(price)
    detail.total = detail.qty * detail.price

    db.session.commit()
    return {"message": "Sale detail updated", "detail": detail.to_dict(include_product=True)}, 200


# delete sale detail
@app.delete("/invoice_detail/delete/<int:detail_id>")
def delete_invoice_detail(detail_id):
    detail = InvoiceDetail.query.get(detail_id)
    if not detail:
        return {"error": "Detail not found"}, 404
    db.session.delete(detail)
    db.session.commit()
    return {"message": "Sale detail deleted"}, 200
