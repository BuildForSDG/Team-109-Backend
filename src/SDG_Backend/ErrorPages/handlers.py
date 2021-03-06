from flask import Blueprint,render_template

error_pages = Blueprint('error_pages',__name__)

@error_pages.app_errorhandler(404)
def error_404(error):
    return render_template('error_pages/404.html',title='Page Not Found'),404

@error_pages.app_errorhandler(403)
def error_403(error):
    return render_template('error_pages/403.html', title='Forbidden'),403

@error_pages.app_errorhandler(500)
def internal_server_error(error):
   return render_template('error_pages/500.html', title='Server Error'), 500
