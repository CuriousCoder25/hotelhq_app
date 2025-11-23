import os
import getpass
from urllib.parse import urlparse
import mysql.connector
from app import create_app, db
from app.models import User

def create_database_if_not_exists(app):
    """Creates the database if it does not already exist."""
    database_uri = app.config['SQLALCHEMY_DATABASE_URI']
    parsed_uri = urlparse(database_uri)
    db_name = parsed_uri.path.lstrip('/')
    
    try:
        # Connect to MySQL server without specifying a database
        conn = mysql.connector.connect(
            host=parsed_uri.hostname,
            user=parsed_uri.username,
            password=parsed_uri.password,
            port=parsed_uri.port
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' created or already exists.")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
        exit(1)

def create_admin_user(app):
    """Prompts for and creates the first admin user."""
    with app.app_context():
        if User.query.filter_by(role='admin').first():
            print("Admin user already exists.")
            return

        print("Create the first admin user.")
        username = input("Enter admin username: ")
        email = input("Enter admin email: ")
        password = getpass.getpass("Enter admin password: ")
        
        admin = User(
            username=username,
            email=email,
            role='admin'
        )
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully.")

if __name__ == '__main__':
    # Create a temporary app instance to access config
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    
    # Create database
    create_database_if_not_exists(app)
    
    # Create tables and admin user within the application context
    with app.app_context():
        print("Dropping existing tables...")
        db.drop_all()
        print("Creating database tables...")
        db.create_all()
        print("Tables created.")
    
    create_admin_user(app)
