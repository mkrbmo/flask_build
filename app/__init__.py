from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = "auth.login"  # redirect to login page if not authenticated

db = SQLAlchemy()

def create_app(config_class="config.Config"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register routes
    from .routes import bp as main_bp
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    

    # Create tables
    with app.app_context():
        db.create_all()

    # Register CLI commands
    from .cli import register_commands
    register_commands(app)

    return app

from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


    
