from flask import Blueprint, render_template, jsonify
from werkzeug.exceptions import HTTPException

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

@errors.app_errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    
    return render_template('errors/500.html'), 500 