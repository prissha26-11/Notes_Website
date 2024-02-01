from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os

db = SQLAlchemy()
DB_NAME ="database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1234'
    app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///'+ path.join(os.getcwd(),f'{DB_NAME}') 
    db.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_perfix='/')
    app.register_blueprint(auth,url_perfix='/')

    from .models import User,Note

    if not path.exists('website/'+DB_NAME):
        with app.app_context():
            db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

        

