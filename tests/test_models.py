from tests.base import BaseTestCase
from app.models import User, Room, Booking
from app import db
import datetime

class TestModels(BaseTestCase):

    def test_user_model(self):
        user = User.query.filter_by(username='testcustomer').first()
        self.assertTrue(user.check_password('customerpass'))
        self.assertFalse(user.check_password('wrongpassword'))
        self.assertEqual(user.role, 'customer')

    def test_room_model(self):
        room = Room.query.filter_by(room_number='101').first()
        self.assertEqual(room.room_type, 'Single')
        self.assertEqual(room.price_per_night, 100)
        self.assertTrue(room.is_available)

    def test_booking_model(self):
        user = User.query.filter_by(username='testcustomer').first()
        room = Room.query.filter_by(room_number='101').first()
        booking = Booking(
            user_id=user.user_id, 
            room_id=room.room_id, 
            total_price=200,
            check_in_date=datetime.date(2025, 12, 1),
            check_out_date=datetime.date(2025, 12, 3)
        )
        db.session.add(booking)
        db.session.commit()

        self.assertIsNotNone(booking.booking_id)
        self.assertEqual(booking.user_id, user.user_id)
        self.assertEqual(booking.room_id, room.room_id)
        self.assertEqual(float(booking.total_price), 200.0)
