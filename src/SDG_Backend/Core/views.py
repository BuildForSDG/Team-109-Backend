from flask import render_template,request,Blueprint,abort
from flask_login import login_user,current_user,logout_user,login_required
from SDG_Backend.models import BlogPost

core = Blueprint('core',__name__)

# add homepage for everyone
@core.route('/')
def index():

    page = request.args.get('page',1,type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)

    return render_template('Core/index.html',blog_posts=blog_posts)


# add about us view
@core.route('/info')
def info():
    return render_template('Core/info.html')


# add youth dashboard view
@core.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('Core/dashboard.html', title="Dashboard")


# add sponsor dashboard view
@core.route('/sponsor_dashboard')
@login_required
def sponsor_dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('Core/sponsor_dashboard.html', title="Sponsor Dashboard")


# add admin dashboard view
@core.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.username == 'admin':
        abort(403)

    return render_template('Core/admin_dashboard.html', title="Admin Dashboard")
