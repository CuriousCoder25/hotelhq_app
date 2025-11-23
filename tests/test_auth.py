from tests.base import BaseTestCase
from flask import url_for

class TestAuthRoutes(BaseTestCase):

    def test_login_page(self):
        with self.app.test_request_context():
            response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_register_page(self):
        with self.app.test_request_context():
            response = self.client.get(url_for('auth.register'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_successful_login_logout(self):
        # Login
        with self.app.test_request_context():
            response = self.login('testcustomer', 'customerpass')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Customer Dashboard', response.data)

        # Logout
        with self.app.test_request_context():
            response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out.', response.data)
        self.assertIn(b'Login', response.data)

    def test_failed_login(self):
        with self.app.test_request_context():
            response = self.login('testcustomer', 'wrongpassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login Unsuccessful. Please check username and password', response.data)

    def test_registration(self):
        with self.app.test_request_context():
            response = self.client.post(url_for('auth.register'), data=dict(
                username='newuser',
                email='new@user.com',
                password='newpassword',
                confirm_password='newpassword',
                role='customer'
            ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your account has been created!', response.data)
        self.assertIn(b'Login', response.data)
