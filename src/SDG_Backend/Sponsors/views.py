from flask import render_template,request,url_for,redirect,Blueprint,flash
from flask_login import login_user,current_user,logout_user,login_required
from .. import db
from ..models import Sponsor,BlogPost
from .forms import LoginForm,RegistrationForm,UpdateSponsorForm
from .picture_handler import add_profile_pic

sponsors = Blueprint('sponsors',__name__)

# Register
@sponsors.route('/register',methods=['GET','POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        sponsor = Sponsor(email=form.email.data,username=form.username.data,firstname=form.firstname.data,
                            lastname=form.lastname.data,password=form.password.data,phone_number=form.phone_number.data)

        db.session.add(sponsor)
        db.session.commit()
        flash('Thank you for registering!')
        return redirect(url_for('sponsors.login'))

    return render_template('Sponsor/register.html',form=form)

# Login
@sponsors.route('/login',methods=['GET','POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        sponsor = Sponsor.query.filter_by(email=form.email.data).first()

        if sponsor.check_password(form.password.data) and sponsor is not None:
            login_user(sponsor)
            flash('Log in Successful!')

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('sponsors.sponsors_dashboard')

            return redirect(next)

        else:
            flash('Invalid email or password.')

    return render_template('Sponsor/login.html',form=form)

# Logout
@sponsors.route('/logout')
def logout():

    logout_user()
    flash('You have successfully been logged out.')

    return redirect(url_for('core.index'))

# Account
@sponsors.route('/account',methods=['GET','POST'])
@login_required
def account():

    form = UpdateSponsorForm()

    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data

        current_user.date_of_birth=form.date_of_birth.data
        current_user.state_of_origin=form.state_of_origin.data
        current_user.local_govt=form.local_govt.data
        current_user.address=form.address.data
        current_user.reason_for_donating=form.reason_for_donating.data

        db.session.commit()
        flash('Sponsor Account Updated!')
        return redirect(url_for('sponsors.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static',filename='profile_pics/'+current_user.profile_image)
    return render_template('Sponsor/account.html',profile_image=profile_image,form=form)

# List of Blog Posts
@sponsors.route('/<username>')
def sponsor_posts(username):

    page = request.args.get('page',1,type=int)
    sponsor = Sponsor.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=sponsor).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)

    return render_template('sponsor_blog_posts.html',blog_posts=blog_posts,user=user)
