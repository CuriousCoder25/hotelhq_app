from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from .config import config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
csrf = CSRFProtect()
bcrypt = Bcrypt()

def create_app(config_name='default'):
    """
    Creates and configures the Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    bcrypt.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .customer import customer as customer_blueprint
    app.register_blueprint(customer_blueprint, url_prefix='/customer')

    from .staff import staff as staff_blueprint
    app.register_blueprint(staff_blueprint, url_prefix='/staff')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    # Context processor to make unread notification count available in all templates
    @app.context_processor
    def inject_notification_count():
        from flask_login import current_user
        from .models import Notification
        if current_user.is_authenticated and current_user.role == 'customer':
            unread_count = Notification.query.filter_by(
                user_id=current_user.user_id, 
                is_read=False
            ).count()
            return dict(unread_notification_count=unread_count)
        return dict(unread_notification_count=0)

    return app
