from tests.base import BaseTestCase
from flask import url_for
from app.models import User, Room
from app import db

class TestAdminRoutes(BaseTestCase):

    def test_admin_dashboard_unauthorized(self):
        # Test access for non-admin (customer)
        self.login('testcustomer', 'customerpass')
        with self.app.test_request_context():
            response = self.client.get(url_for('admin.dashboard'), follow_redirects=True)
        self.assertEqual(response.status_code, 403) # Forbidden

        # Test access for non-admin (staff)
        self.logout()
        self.login('teststaff', 'staffpass')
        with self.app.test_request_context():
            response = self.client.get(url_for('admin.dashboard'), follow_redirects=True)
        self.assertEqual(response.status_code, 403)

    def test_admin_dashboard_authorized(self):
        self.login('testadmin', 'adminpass')
        with self.app.test_request_context():
            response = self.client.get(url_for('admin.dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Dashboard', response.data)

    def test_add_room(self):
        self.login('testadmin', 'adminpass')
        with self.app.test_request_context():
            response = self.client.post(url_for('admin.add_edit_room'), data=dict(
                room_number='201',
                room_type='Double',
                price_per_night=200.0,
                features='Test feature'
            ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Room added successfully', response.data)
        room = Room.query.filter_by(room_number='201').first()
        self.assertIsNotNone(room)
        self.assertEqual(room.room_type, 'Double')

    def test_manage_users(self):
        self.login('testadmin', 'adminpass')
        response = self.client.get(url_for('admin.manage_users'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testcustomer', response.data)
        self.assertIn(b'teststaff', response.data)

    def test_edit_user(self):
        self.login('testadmin', 'adminpass')
        user_to_edit = User.query.filter_by(username='testcustomer').first()
        response = self.client.post(url_for('admin.edit_user', user_id=user_to_edit.user_id), data=dict(
            username='editedcustomer',
            email='edited@customer.com',
            role='staff'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User has been updated', response.data)
        edited_user = User.query.get(user_to_edit.id)
        self.assertEqual(edited_user.username, 'editedcustomer')
        self.assertEqual(edited_user.role, 'staff')
