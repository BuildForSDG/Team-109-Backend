from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DateField,TextAreaField,IntegerField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

from flask_login import current_user
from SDG_Backend.models import Youth

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Log In')



class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('Username',validators=[DataRequired()])
    firstname = StringField('First Name',validators=[DataRequired()])
    lastname = StringField('Last Name',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('password_confirm',message='Password must match!')])
    password_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    phone_number = IntegerField('Phone Number',validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth',validators=[DataRequired()])
    state_of_origin = StringField('State of Origin',validators=[DataRequired()])
    local_govt = StringField('Local Govt.',validators=[DataRequired()])
    address = StringField('Residential Address',validators=[DataRequired()])
    education_level = StringField('Highest Education Level',validators=[DataRequired()])
    reason_for_applying = TextAreaField('Why should we consider you?',validators=[DataRequired()])


    submit = SubmitField('Register')

    def check_email(self,field):

        if Youth.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered!')

    def check_username(self,field):

        if Youth.query.filter_by(username=field.data).first():
            raise ValidationError('The Username has been taken!')

class UpdateYouthForm(FlaskForm):

    email = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('Username',validators=[DataRequired()])
    bvn = IntegerField('Bank Ver. Number')
    picture = FileField('Update Picture Profile',validators=[FileAllowed(['jpg','png','JPG','jpeg','JPEG','PNG'])])
    submit = SubmitField('Update Profile')
