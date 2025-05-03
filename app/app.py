from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static', static_url_path='/')
    app.config.from_object(Config)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    from models import Users
    
    # define to the login manager how to load a user 
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(user_id)
    
    bcrypt = Bcrypt(app)
    
    from routes import register_routes
    register_routes(app, db, bcrypt)
    
    db.init_app(app)
    
    Migrate(app, db)
    
    return app
