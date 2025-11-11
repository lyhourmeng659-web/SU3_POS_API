import traceback
from urllib import request
from app import app, db
from sqlalchemy import text
from flask import request
from model.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from .func_ import *


# for generate_user_password_hash
# @app.get('/test')
# def test():
#     assert False, check_password_hash(generate_password_hash('12345678'), '12345678')
#     return {"message": "user route is working"}, 200


# select all user use RAW SQL
@app.get('/user/list')
def user():
    sql = text("""
                SELECT * FROM users 
                """)
    result = db.session.execute(sql).fetchall()
    rows = [dict(row._mapping) for row in result]
    return rows, 200


# select user by id use RAW SQL function
@app.get('/user/list-by-id/<int:user_id>')
def user_by_id(user_id):
    result = get_user_by_id(user_id)
    return result


# create user use ORM
@app.post('/user/create')
def create_user():
    form = request.get_json(silent=True) or request.form
    file = request.files.get('profile')
    file_name = None
    # validate upload image
    if file:
        err = validate_image_type(file) or validate_image_size(file)
        if err:
            return err, 400
        file_name = file.filename
        save_path = f'static/image/user/{file_name}'
        file.save(save_path)
        watermark_image(save_path)

    # validate form fields
    if not form:
        return {"error": "form is empty"}, 400

    if not form.get('user_name'):
        return {"error": "username is missing"}, 400

    if not form.get('password'):
        return {"error": "password is missing"}, 400

    # create new user record
    user_name = form.get('user_name')

    # validation user already exists in user table
    existing_user = User.query.filter_by(user_name=user_name).first()
    if existing_user:
        return {"error": "User already exists"}, 400
    password = generate_password_hash(form.get('password'))
    user = User(
        user_name=user_name,
        password=password,
        profile=file_name
    )
    db.session.add(user)
    db.session.commit()

    return {
        "message": "user created successfully",
        "user_id": get_user_by_id(user.id)
    }, 200


# delete user use ORM
@app.post('/user/delete')
def delete_user():
    form = request.get_json(silent=True)
    if not form.get('user_id'):
        return {"error": "user id is missing"}, 400

    # error when user not found
    is_existing = get_user_by_id(form.get('user_id'))
    if is_existing.get('error'):
        return {"error": "user not found "}, 400

    user_id = form.get('user_id')
    user = User.query.get(user_id)
    db.session.delete(user)

    # sql = text("""
    #             DELETE FROM users
    #             WHERE id = :user_id
    #             """)

    # db.session.execute(sql,
    #                        {
    #                         "user_id": user_id,
    #                        })

    db.session.commit()
    return {
        "message": "user deleted successfully",
    }, 200


# update user use ORM
@app.post('/user/update')
def update_user():
    form = request.get_json(silent=True) or request.form
    if not form:
        return {"error": "form is empty"}

    if not form.get('user_id'):
        return {"error": "user id is missing"}, 400

    if not form.get('user_name'):
        return {"error": "username is missing"}, 400

    # error when user not found
    is_existing = get_user_by_id(form.get('user_id'))
    if is_existing.get('error'):
        return {"error": "user not found"}, 400

    user_id = form.get('user_id')
    user_name = form.get('user_name')

    # validation user already exists in user table
    existing_user = User.query.filter_by(user_name=user_name).first()
    if existing_user:
        return {"error": "User already exists"}, 400

    profile = form.get('profile')
    profile_file = request.files.get('profile')
    if profile_file:
        file_name = profile_file.filename
        save_path = f'static/image/user/{file_name}'
        profile_file.save(save_path)
        watermark_image(save_path)
        profile = file_name

    user = User.query.get(user_id)
    # assert False, user.user_name
    user.user_name = user_name
    user.profile = profile

    # sql = text("""
    #             UPDATE users
    #             SET branch_id = :branch_id, user_name = :user_name
    #             WHERE id = :user_id
    #             """)

    # db.session.execute(sql,
    #                             {
    #                                 "branch_id": branch_id,
    #                                 "user_name": user_name,
    #                                 "user_id": user_id
    #                             }
    #                             )

    db.session.commit()
    return {
        "message": "User updated successfully",
        "user_id": get_user_by_id(user_id
                                  )}, 200
