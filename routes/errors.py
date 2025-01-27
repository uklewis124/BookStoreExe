import jinja2
from flask import Blueprint, render_template

Errors = Blueprint('errors', __name__)

@Errors.errorhandler(404)
def error_404(e):
    return render_template('error_pages/404.html')

@Errors.errorhandler(403)
def error_403(e):
    return render_template('error_pages/403.html')

@Errors.errorhandler(400)
def error_400(e):
    return render_template('error_pages/400.html')

@Errors.errorhandler(500)
def error_500(e):
    return render_template('error_pages/500.html')

@Errors.errorhandler(jinja2.exceptions.TemplateSyntaxError)
def error_syntax(e):
    return render_template(
        'error_pages/syntax.html',
        error=e,
        file=e.filename,
        traceback=e.lineno)
    
@Errors.errorhandler(jinja2.exceptions.TemplateNotFound)
def error_404(e):
    return render_template('error_pages/404.html')