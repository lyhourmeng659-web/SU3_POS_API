from app import app
from flask import abort


@app.route("/admin")
def forbidden():
    abort(403)
