from flask import render_template,request,url_for,redirect,Blueprint,flash
from flask_login import login_user,current_user,logout_user,login_required
from .. import db
from ..models import Youth,BlogPost
from .forms import LoginForm,RegistrationForm,UpdateYouthForm
from .picture_handler import add_profile_pic

youths = Blueprint('youths',__name__)

# Register
@youths.route('/register',methods=['GET','POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        youth = Youth(email=form.email.data,username=form.username.data,firstname=form.firstname.data,lastname=form.lastname.data,password=form.password.data,
                        phone_number=form.phone_number.data,date_of_birth=form.date_of_birth.data,state_of_origin=form.state_of_origin.data,
                        local_govt=form.local_govt.data,address=form.address.data,education_level=form.education_level.data,reason_for_applying=form.reason_for_applying.data)

        db.session.add(youth)
        db.session.commit()
        flash('Thank you for registering!')
        return redirect(url_for('youths.login'))

    return render_template('Youth/register.html',form=form)

# Login
@youths.route('/login',methods=['GET','POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        youth = Youth.query.filter_by(email=form.email.data).first()

        if youth.check_password(form.password.data) and youth is not None:
            login_user(youth)
            flash('Log in Successful!')

            if youth.is_admin:
                return redirect(url_for('core.admin_dashboard'))
            else:
                return redirect(url_for('core.index'))

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('core.index')

            return redirect(next)


        else:
            flash('Invalid email or password.')

    return render_template('Youth/login.html',form=form)

# Logout
@youths.route('/logout')
def logout():

    logout_user()
    flash('You have successfully been logged out.')

    return redirect(url_for('core.index'))

# Account
@youths.route('/account',methods=['GET','POST'])
@login_required
def account():

    form = UpdateYouthForm()

    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bvn = form.bvn.data

        db.session.commit()
        flash('Your Profile has been Updated!')
        return redirect(url_for('youths.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static',filename='profile_pics/'+current_user.profile_image)
    return render_template('Youth/account.html',profile_image=profile_image,form=form)

# List of Blog Posts
@youths.route('/<username>')
def youth_posts(username):

    page = request.args.get('page',1,type=int)
    youth = Youth.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=youth).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)

    return render_template('youth_blog_posts.html',blog_posts=blog_posts,user=user)
