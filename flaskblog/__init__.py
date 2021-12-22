from flask import Flask
from flaskblog.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from flask_mail import Mail



db = SQLAlchemy() #database
bcrypt = Bcrypt() #hash passwords
login_manager = LoginManager() #login
login_manager.login_view = 'users.login' #if someone tries to acces the account page without being loggin in redirect them to the login page
login_manager.login_message_category = 'info' #message displaed if unlogged in user tried to access account, info is bootstrap class
mail = Mail()



def create_app(config_class=Config):   #func to create instances of our app
    app=Flask(__name__)
    app.config.from_object(Config)   #Gets the keys from config.py

    db.init_app(app)
    bcrypt.init_app(app)   #Make sure the things outside the class have access to the app
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users   #importing the blueprint from the folder users, and the file routes.py
    app.register_blueprint(users)

    from flaskblog.posts.routes import posts   #importing the blueprint from the folder posts, and the file routes.py
    app.register_blueprint(posts)

    from flaskblog.main.routes import main   #importing the blueprint from the folder main, and the file routes.py
    app.register_blueprint(main)

    from flaskblog.errors.handlers import errors
    app.register_blueprint(errors)

    return app
