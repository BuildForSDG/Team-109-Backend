# SDG_Backend/Admin/views.py

from flask import Blueprint, render_template, redirect, url_for, flash, abort, session, request
from flask_login import current_user, login_required
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView

from SDG_Backend import db
from SDG_Backend.models import Youth, Status, Project, Sponsor
from .forms import StatusForm, ProjectForm, YouthAssignForm, SponsorForm

admins = Blueprint('admins', __name__)


class AdminView(ModelView):
    """
    Secures the admin Views
    """

    can_view_details = True
    page_size = 100
    column_exclude_list = ['password']
    #column_searchable_list = ['email','username','phone_number','state_of_origin','address']
    create_modal = True
    edit_modal = True
    can_export = True

    def __init__(self, *args, **kwargs):

        super().__init__(*args,**kwargs)
        self.static_folder = 'static'

    def is_accessible(self):

        return session.get('youth') == 'admin'

    def inaccessible_callback(self,name,**kwargs):

        if not self.is_accessible():
            return redirect(url_for('core.index',next=request.url))


class AnalyticsView(BaseView):

    @expose('/')
    def index(self):
        return self.render_template('analytics.html')


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.username == 'admin':
        abort(403)

# Status Views
@admins.route('/status', methods=['GET', 'POST'])
@login_required
def list_statuss():
    """
    List all Status
    """
    check_admin()

    statuss = Status.query.all()

    return render_template('Admin/Status/statuss.html',statuss=statuss, title="Status")


@admins.route('/status/add', methods=['GET', 'POST'])
@login_required
def add_status():
    """
    Add a status to the database
    """
    check_admin()

    add_status = True

    form = StatusForm()
    if form.validate_on_submit():
        status = Status(name=form.name.data,description=form.description.data)

        try:
            # add status to the database
            db.session.add(status)
            db.session.commit()
            flash('You have successfully added a new status.')
        except:
            # in case status name already exists
            flash('Error: status name already exists.')

        # redirect to status page
        return redirect(url_for('admins.list_statuss'))

    # load status template
    return render_template('Admin/Status/status.html', action="Add",
                           add_status=add_status, form=form,
                           title="Add Status")


@admins.route('/status/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_status(id):
    """
    Edit a status
    """
    check_admin()

    add_status = False

    status = Status.query.get_or_404(id)
    form = StatusForm(obj=status)
    if form.validate_on_submit():
        status.name = form.name.data
        status.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the status.')

        # redirect to the status page
        return redirect(url_for('admins.list_statuss'))

    form.description.data = status.description
    form.name.data = status.name
    return render_template('admins/Status/status.html', action="Edit",
                           add_status=add_status, form=form,
                           status=status, title="Edit Status")


@admins.route('/status/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_status(id):
    """
    Delete a status from the database
    """
    check_admin()

    status = Status.query.get_or_404(id)
    db.session.delete(status)
    db.session.commit()
    flash('You have successfully deleted the status.')

    # redirect to the status page
    return redirect(url_for('admins.list_statuss'))

    return render_template(title="Delete Status")



@admins.route('/projects')
@login_required
def list_projects():
    check_admin()
    """
    List all projects
    """
    projects = Project.query.all()
    return render_template('Admin/Projects/projects.html',projects=projects, title='Projects')


@admins.route('/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    """
    Add a project to the database
    """
    check_admin()

    add_project = True

    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data,description=form.description.data)

        try:
            # add project to the database
            db.session.add(project)
            db.session.commit()
            flash('You have successfully added a new project.')
        except:
            # in case project name already exists
            flash('Error: project name already exists.')

        # redirect to the projects page
        return redirect(url_for('admins.list_projects'))

    # load project template
    return render_template('Admin/Projects/project.html', add_project=add_project,
                           form=form, title='Add Project')


@admins.route('/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    """
    Edit a project
    """
    check_admin()

    add_project = False

    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        db.session.add(project)
        db.session.commit()
        flash('You have successfully edited the project.')

        # redirect to the projects page
        return redirect(url_for('admins.list_projects'))

    form.description.data = project.description
    form.name.data = project.name
    return render_template('Admin/Projects/project.html', add_project=add_project,
                           form=form, title="Edit Project")


@admins.route('/projects/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_project(id):
    """
    Delete a projcet from the database
    """
    check_admin()

    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('You have successfully deleted the project.')

    # redirect to the projects page
    return redirect(url_for('admins.list_projects'))

    return render_template(title="Delete Project")



@admins.route('/sponsors')
@login_required
def list_sponsors():
    check_admin()
    """
    List all sponsors
    """
    sponsors = Sponsor.query.all()
    return render_template('Admin/Sponsors/sponsors.html',sponsors=sponsors, title='Sponsors')


@admins.route('/sponsors/add', methods=['GET', 'POST'])
@login_required
def add_sponsor():
    """
    Add a sponsor to the database
    """
    check_admin()

    add_sponsor = True

    form = SponsorForm()
    if form.validate_on_submit():
        sponsor = Sponsor(email=form.email.data,username=form.username.data,firstname=form.firstname.data,
                            lastname=form.lastname.data,password=form.password.data,phone_number=form.phone_number.data)

        try:
            # add sponsor to the database
            db.session.add(sponsor)
            db.session.commit()
            flash('You have successfully added a new sponsor.')
        except:
            # in case sponsor name already exists
            flash('Error: sponsor already exists.')

        # redirect to the sponsors page
        return redirect(url_for('admins.list_sponsors'))

    # load project template
    return render_template('Admin/Sponsors/sponsor.html', add_sponsor=add_sponsor,
                           form=form, title='Add Sponsor')


@admins.route('/youth')
@login_required
def list_youth():
    """
    List all youths
    """
    check_admin()

    youths = Youth.query.all()
    return render_template('Admin/Youth/youths.html', youths=youths, title='Youth')


@admins.route('/youth/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_youth(id):
    """
    Assign a status, a project or a sponsor to a Youth
    """
    check_admin()

    youth = Youth.query.get_or_404(id)

    # prevent admin from being assigned a status or project
    if youth.username == 'admin':
        abort(403)

    form = YouthAssignForm(obj=youth)
    if form.validate_on_submit():
        youth.status = form.status.data
        youth.project = form.project.data
        youth.sponsor = form.sponsor.data

        #db.session.add(youth)
        db.session.commit()
        flash('You have successfully assigned a status, a project and a sponsor.')

        # redirect to the projects page
        return redirect(url_for('admins.list_youth'))

    return render_template('Admin/Youth/youth.html', youth=youth, form=form, title='Assign Youth')
