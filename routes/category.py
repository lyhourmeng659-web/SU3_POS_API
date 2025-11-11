from app import app, db
from flask import request
from model.category import Category
from .func_ import *


# select all category use RAW SQL
@app.get('/category/list')
def category():
    sql = text("""
                SELECT * FROM categories
                """)
    result = db.session.execute(sql).fetchall()
    rows = [dict(row._mapping) for row in result]
    return rows, 200


# select category by id category RAW SQL function
@app.get('/category/list-by-id/<int:category_id>')
def category_by_id(category_id):
    result = get_category_by_id(category_id)
    return result


# create category use ORM
@app.post('/category/create')
def create_category(category_id=None):
    form = request.get_json(silent=True) or request.form
    file = request.files.get('image')
    file_name = None
    # validate upload image
    if file:
        err = validate_image_type(file) or validate_image_size(file)
        if err:
            return err, 400
        file_name = file.filename
        save_path = f'static/image/category/{file_name}'
        file.save(save_path)
        watermark_image(save_path)

    # validate form fields
    if not form:
        return {"error": "form is empty"}, 400

    if not form.get('name'):
        return {"error": "category name is missing"}, 400

    # create new user record
    category_name = form.get('name')

    # validation user already exists in user table
    existing_category = Category.query.filter_by(name=category_name).first()
    if existing_category and existing_category.id != category_id:
        return {"error": "category already exists"}, 400

    # existing_category = Category.query.filter_by(name=category_name).first()
    # if existing_category:
    #     return {"error": "category already exists"}, 400

    category = Category(
        name=category_name,
        image=file_name
    )

    db.session.add(category)
    db.session.commit()

    return {
        "message": "Category created successfully",
        "product_id": get_category_by_id(category.id)
    }, 200


# delete category use ORM
@app.post('/category/delete')
def delete_category():
    form = request.get_json(silent=True)
    if not form.get('category_id'):
        return {"error": "category id is missing"}, 400

    # error when category not found
    is_existing = get_category_by_id(form.get('category_id'))
    if is_existing.get('error'):
        return {"error": "category not found "}, 400

    category_id = form.get('category_id')
    category = Category.query.get(category_id)

    db.session.delete(category)
    db.session.commit()

    return {
        "message": "Category deleted successfully",
    }, 200


# update category use ORM
@app.post('/category/update')
def update_category():
    form = request.get_json(silent=True) or request.form
    if not form:
        return {"error": "form is empty"}

    if not form.get('category_id'):
        return {"error": "category id is missing"}, 400

    if not form.get('name'):
        return {"error": "category name is missing"}, 400

    # error when category not found
    is_existing = get_category_by_id(form.get('category_id'))
    if is_existing.get('error'):
        return {"error": "category not found"}, 400

    category_id = form.get('category_id')
    category_name = form.get('name')

    # validation user already exists in user table
    existing_category = Category.query.filter_by(name=category_name).first()
    if existing_category and existing_category.id != category_id:
        return {"error": "category already exists"}, 400

    image = form.get('image')
    image_file = request.files.get('image')
    if image_file:
        file_name = image_file.filename
        save_path = f'static/image/category/{file_name}'
        image_file.save(save_path)
        watermark_image(save_path)
        image = file_name

    category = Category.query.get(category_id)
    category.name = category_name
    category.image = image

    db.session.commit()
    return {
        "message": "Category updated successfully",
        "user_id": get_category_by_id(category_id
                                  )}, 200