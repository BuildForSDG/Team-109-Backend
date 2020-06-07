# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DateField,TextAreaField,IntegerField, SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from ..models import Status, Project, Sponsor
from wtforms.ext.sqlalchemy.fields import QuerySelectField


class StatusForm(FlaskForm):
    """
    Form for admin to add or edit a status
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ProjectForm(FlaskForm):
    """
    Form for admin to add or edit a project
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SponsorForm(FlaskForm):
    """
    Form for admin to add a sponsor
    """
    email = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('Username',validators=[DataRequired()])
    firstname = StringField('Firstname',validators=[DataRequired()])
    lastname = StringField('Lastname',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('password_confirm',message='Password must match!')])
    password_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    phone_number = IntegerField('Phone Number',validators=[DataRequired()])
    submit = SubmitField('Register')

class YouthAssignForm(FlaskForm):
    """
    Form for admin to assign atatus, roles and sponsors to youth
    """
    status = QuerySelectField(query_factory=lambda: Status.query.all(),get_label="name")
    project = QuerySelectField(query_factory=lambda: Project.query.all(),get_label="name")
    sponsor = QuerySelectField(query_factory=lambda: Sponsor.query.all(),get_label="username")
    submit = SubmitField('Submit')
