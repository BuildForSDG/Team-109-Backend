from SDG_Backend.__init__ import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(youth_id):
    return Youth.query.get(youth_id)

class Youth(db.Model,UserMixin):

    __tablename__ = 'youths'

    id = db.Column(db.Integer,primary_key=True)
    profile_image = db.Column(db.String(20),nullable=False,default='default.JPG')
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    firstname = db.Column(db.String(64),index=True)
    lastname = db.Column(db.String(64),index=True)

    password_hash = db.Column(db.String(128))

    phone_number = db.Column(db.Integer,index=False,nullable=False,unique=True)
    date_of_birth = db.Column(db.Date,index=False,nullable=False,unique=False)
    date_registered = db.Column(db.DateTime,index=False,nullable=True,unique=False,default=datetime.utcnow)
    last_login = db.Column(db.DateTime,index=False,nullable=True,unique=False,default=datetime.utcnow)
    state_of_origin = db.Column(db.String(64),unique=False,index=True)
    local_govt = db.Column(db.String(64),unique=False,index=True)
    address = db.Column(db.String(64),unique=False,index=True)
    education_level = db.Column(db.String(64),unique=False,index=True)
    reason_for_applying = db.Column(db.Text,unique=False,index=True)
    bvn = db.Column(db.Integer,unique=True,index=True)
    status_id = db.Column(db.Integer, db.ForeignKey('statuss.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    sponsor_id = db.Column(db.Integer,db.ForeignKey('sponsors.id'))
    is_admin = db.Column(db.Boolean,default=False)

    sponsor = db.relationship('Sponsor',backref='youth',uselist=False)
    posts = db.relationship('BlogPost',backref='author',lazy=True)

    def __init__(self,email,username,password,firstname,lastname,phone_number,date_of_birth,state_of_origin,local_govt,
                address,education_level,reason_for_applying):

        self.email = email
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.password_hash = generate_password_hash(password)
        self.phone_number = phone_number
        self.date_of_birth = date_of_birth
        self.state_of_origin = state_of_origin
        self.local_govt = local_govt
        self.address = address
        self.education_level = education_level
        self.reason_for_applying = reason_for_applying
        #self.is_admin = is_admin


    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"username {self.username}"



class Sponsor(db.Model,UserMixin):

    __tablename__ = 'sponsors'

    id = db.Column(db.Integer,primary_key=True)
    profile_image = db.Column(db.String(20),nullable=False,default='default.JPG')
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    firstname = db.Column(db.String(64),index=True)
    lastname = db.Column(db.String(64),index=True)
    phone_number = db.Column(db.Integer,index=False,nullable=False,unique=True)

    password_hash = db.Column(db.String(128))

    date_registered = db.Column(db.DateTime,index=False,nullable=True,unique=False,default=datetime.utcnow)
    last_login = db.Column(db.DateTime,index=False,nullable=True,unique=False,default=datetime.utcnow)
    state_of_origin = db.Column(db.String(64),unique=False,index=True)
    local_govt = db.Column(db.String(64),unique=False,index=True)
    address = db.Column(db.String(64),unique=False,index=True)
    reason_for_donating = db.Column(db.Text,unique=False,index=True)

    #youth = db.relationship('Youth',backref='sponsor',uselist=True)
    #posts = db.relationship('BlogPost',backref='author',lazy=True)

    #youth_id = db.Column(db.Integer,db.ForeignKey('youths.id'))

    def __init__(self,email,username,firstname,lastname,password,phone_number):

        self.email = email
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.password_hash = generate_password_hash(password)
        self.phone_number = phone_number

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    #def get_id(self):
        #return (self.sponsor_id)

    def __repr__(self):
        return f"The Sponsor is {self.username}"


# Set up user_loader
@login_manager.user_loader
def load_user(youth_id):
    return Youth.query.get(int(youth_id))

#@login_manager.user_loader
#def load_user(sponsor_id):
#    return Sponsor.query.get(int(sponsor_id))


class Status(db.Model):
    """
    Create a Status table
    """

    __tablename__ = 'statuss'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    youth = db.relationship('Youth',backref='status',lazy='dynamic')

    def __repr__(self):
        return '<Status: {}>'.format(self.name)


class Project(db.Model):
    """
    Create a Project table
    """

    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    youth = db.relationship('Youth',backref='project',lazy='dynamic')

    def __repr__(self):
        return '<Project: {}>'.format(self.name)


class BlogPost(db.Model):

    youth = db.relationship(Youth)

    id = db.Column(db.Integer,primary_key=True)
    youth_id = db.Column(db.Integer,db.ForeignKey('youths.id'),nullable=False)
    #sponsor_id = db.Column(db.Integer,db.ForeignKey('sponsors.id'),nullable=False)

    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    title = db.Column(db.String(144),nullable=False)
    text = db.Column(db.Text,nullable=False)

    def __init__(self,title,text,youth_id):

        self.title = title
        self.text = text
        self.youth_id = youth_id

    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date} -- {self.title}"
