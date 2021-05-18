from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, current_user, UserMixin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# ! INITIALIZE DATABASE
db = SQLAlchemy()
DB_NAME = "bloodbank.db"

# ! INITIALIZE FLASK
app = Flask(__name__)
login = LoginManager(app)

@login.user_loader
def load_user(user_id):
    return AdminUser.query.get(user_id)

class AdminUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

def create_app():

    # ! ENCRYPT COOKIE OR SESSION DATA
    app.secret_key = '1234567890'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # ! Connecting database with app
    db.init_app(app)

    # ! CREATING ADMIN
    # ? ACCOUNT CREATION THROUGH TERMINAL INSTEAD OF LOGIN PAGE
    admin = Admin(app, 'Admin Area', template_mode='bootstrap3')
    admin.add_view(MyModelView(AdminUser, db.session))

    # ! REGISTER OUR BLUEPRINTS IN OUR APP
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Patient, Donor, Doctor, Bloodbank, Blood, Blooddelivery

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
