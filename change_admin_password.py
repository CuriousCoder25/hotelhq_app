import getpass
from app import create_app, db
from app.models import User

def change_admin_password():
    """Change the admin user's password"""
    app = create_app()
    
    with app.app_context():
        # Get admin user
        admin = User.query.filter_by(role='admin').first()
        
        if not admin:
            print("Error: No admin user found in database!")
            return
        
        print(f"Admin user found: {admin.username} ({admin.email})")
        print()
        
        # Get new password
        new_password = getpass.getpass("Enter new admin password: ")
        confirm_password = getpass.getpass("Confirm new password: ")
        
        if new_password != confirm_password:
            print("Error: Passwords do not match!")
            return
        
        if len(new_password) < 4:
            print("Error: Password must be at least 4 characters long!")
            return
        
        # Update password
        admin.set_password(new_password)
        db.session.commit()
        
        print()
        print("✓ Admin password successfully updated!")
        print(f"Username: {admin.username}")
        print("You can now login with the new password.")

if __name__ == '__main__':
    print("=" * 50)
    print("Change Admin Password")
    print("=" * 50)
    print()
    change_admin_password()
    print()
    print("=" * 50)
