import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from config import app_config
from SDG_Backend import models

###################################

app = Flask(__name__, instance_relative_config=True)


basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'p9Bv<3Eid9%$i01'
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy(app)

login_manager = LoginManager()

####################################

def create_app(config_name):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    Bootstrap(app)
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "youth.login"

    migrate = Migrate(app, db)

    from .models import Youth,Sponsor,Status,Project,BlogPost
    from .Admin.views import AdminView,AnalyticsView

    admin = Admin(app,name='Admin Dashboard',base_template='base.html',index_view=AdminView(Youth,db.session),url='/admin',endpoint='admin')
    admin.add_view(AnalyticsView(name='Analytics',endpoint='analytics'))
    admin.add_view(AdminView(Sponsor,db.session))
    admin.add_view(AdminView(Status,db.session))
    admin.add_view(AdminView(Project,db.session))
    admin.add_view(AdminView(BlogPost,db.session))

    from .Admin.views import admins
    app.register_blueprint(admins,url_prefix='/admins')

    from .Core.views import core
    app.register_blueprint(core)

    from .ErrorPages.handlers import error_pages
    app.register_blueprint(error_pages)

    from .Youths.views import youths
    app.register_blueprint(youths,url_prefix='/youths')

    from .Sponsors.views import sponsors
    app.register_blueprint(sponsors,url_prefix='/sponsors')

    from .BlogPosts.views import blog_posts
    app.register_blueprint(blog_posts)


    return app

####################################



####################################
