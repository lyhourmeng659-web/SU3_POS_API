from app import app, db
from flask import request
from model import Category
from model.product import Product
from .func_ import *


# select all product RAW SQL function
@app.get('/product/list')
def product_list():
    sql = text("""
        SELECT p.*, c.name AS category_name, c.image AS category_image
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
    """)
    result = db.session.execute(sql).fetchall()
    rows = [dict(row._mapping) for row in result]
    return rows, 200


# select product by id product RAW SQL function
@app.get('/product/list-by-id/<int:product_id>')
def product_by_id(product_id):
    result = get_product_by_id(product_id)
    return result


# create product use ORM
@app.post('/product/create')
def create_product():
    form = request.get_json(silent=True) or request.form
    file = request.files.get('image')
    file_name = None
    if file:
        err = validate_image_type(file) or validate_image_size(file)
        if err:
            return err, 400
        file_name = file.filename
        save_path = f'static/image/product/{file_name}'
        file.save(save_path)
        watermark_image(save_path)

    if not form:
        return {"error": "form is empty"}, 400

    name = form.get('name')
    category_id = form.get('category_id')
    cost = form.get('cost')
    price = form.get('price')

    if not name: return {"error": "product name is missing"}, 400
    if not category_id: return {"error": "category id is missing"}, 400
    if not cost: return {"error": "cost is missing"}, 400
    if not price: return {"error": "price is missing"}, 400

    # ensure category exists
    try:
        category_id = int(category_id)
    except:
        return {"error": "invalid category id"}, 400

    category = Category.query.get(category_id)
    if not category:
        return {"error": "category not found"}, 400

    # duplicate product check
    existing_product = Product.query.filter_by(name=name).first()
    if existing_product:
        return {"error": "product already exists"}, 400

    product = Product(
        name=name,
        category_id=category_id,
        cost=float(cost),
        price=float(price),
        image=file_name
    )
    db.session.add(product)
    db.session.commit()

    return {
        "message": "Product created successfully",
        "product": product.to_dict(include_category=True)
    }, 200


# update product use ORM
@app.post('/product/update')
def update_product():
    form = request.get_json(silent=True) or request.form
    if not form:
        return {"error": "form is empty"}, 400

    try:
        product_id = int(form.get('product_id') or 0)
    except:
        return {"error": "invalid product id"}, 400
    name = form.get('name')
    category_id = form.get('category_id')
    cost = form.get('cost')
    price = form.get('price')

    if not product_id: return {"error": "product id is missing"}, 400
    if not name: return {"error": "product name is missing"}, 400
    if not category_id: return {"error": "category id is missing"}, 400
    if not cost: return {"error": "cost is missing"}, 400
    if not price: return {"error": "price is missing"}, 400

    product = Product.query.get(product_id)
    if not product:
        return {"error": "product not found"}, 400

    # ensure category exists
    try:
        category_id = int(category_id)
    except:
        return {"error": "invalid category id"}, 400
    category = Category.query.get(category_id)
    if not category:
        return {"error": "category not found"}, 400

    # duplicate name check but allow same product to keep its name
    existing_product = Product.query.filter_by(name=name).first()
    if existing_product and existing_product.id != product_id:
        return {"error": "product already exists"}, 400

    image_file = request.files.get('image')
    if image_file:
        file_name = image_file.filename
        save_path = f'static/image/product/{file_name}'
        image_file.save(save_path)
        watermark_image(save_path)
        product.image = file_name

    product.name = name
    product.category_id = category_id
    product.cost = float(cost)
    product.price = float(price)

    db.session.commit()

    return {
        "message": "Product updated successfully",
        "product": product.to_dict(include_category=True)
    }, 200


# delete product use ORM
@app.post('/product/delete')
def delete_product():
    form = request.get_json(silent=True)
    if not form.get('product_id'):
        return {"error": "product id is missing"}, 400

    # error when product not found
    is_existing = get_product_by_id(form.get('product_id'))
    if is_existing.get('error'):
        return {"error": "product not found "}, 400

    product_id = form.get('product_id')
    product = Product.query.get(product_id)

    db.session.delete(product)
    db.session.commit()

    return {
        "message": "Product deleted successfully",
    }, 200
