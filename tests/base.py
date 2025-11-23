import unittest
from app import create_app, db
from app.models import User, Room, Booking
from app.config import TestingConfig

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        # Create a test admin user
        self.admin_user = User(username='testadmin', email='admin@test.com', role='admin')
        self.admin_user.set_password('adminpass')
        
        # Create a test staff user
        self.staff_user = User(username='teststaff', email='staff@test.com', role='staff')
        self.staff_user.set_password('staffpass')

        # Create a test customer user
        self.customer_user = User(username='testcustomer', email='customer@test.com', role='customer')
        self.customer_user.set_password('customerpass')

        # Create a test room
        self.room = Room(room_number='101', room_type='Single', price_per_night=100)

        db.session.add_all([self.admin_user, self.staff_user, self.customer_user, self.room])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username, password):
        return self.client.post('/auth/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/auth/logout', follow_redirects=True)

if __name__ == '__main__':
    unittest.main()
