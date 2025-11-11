from flask import jsonify

from app import app


@app.errorhandler(404)
def error_404(e):
    return jsonify({
        'status': 404,
        'message': 'page not found'
    }), 404


@app.errorhandler(500)
def error_500(e):
    return jsonify({
        'status': 500,
        'message': 'internal server error',
    }), 500


def error_403(e):
    return jsonify({
        'status': 403,
        'message': '403 You do not have access.',
    }), 403


app.register_error_handler(403, error_403)
# @app.errorhandler(Exception)
# def error_exception(e):
#     return jsonify({
#         'status': 500,
#         'message': str(e)
#     }), 500
