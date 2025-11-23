from tests.base import BaseTestCase
from flask import url_for
from app.models import Room

class TestCustomerRoutes(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.login('testcustomer', 'customerpass')

    def test_customer_dashboard(self):
        with self.app.test_request_context():
            response = self.client.get(url_for('customer.dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Customer Dashboard', response.data)

    def test_view_rooms(self):
        with self.app.test_request_context():
            response = self.client.get(url_for('customer.rooms'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Our Rooms', response.data)
        self.assertIn(b'101', response.data) # Check if test room is displayed

    def test_book_room(self):
        room = Room.query.filter_by(room_number='101').first()
        with self.app.test_request_context():
            response = self.client.post(url_for('customer.book_room', room_id=room.room_id), data=dict(
                check_in_date='2025-12-01',
                check_out_date='2025-12-03'
            ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Room booked successfully', response.data)
        self.assertIn(b'My Bookings', response.data)

    def test_my_bookings(self):
        # First, book a room to have a booking to view
        self.test_book_room()
        with self.app.test_request_context():
            response = self.client.get(url_for('customer.my_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'My Bookings', response.data)
        self.assertIn(b'101', response.data) # Check if the booked room is listed
