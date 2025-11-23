from . import db, bcrypt
from flask_login import UserMixin
from sqlalchemy import func

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(20))
    address = db.Column(db.Text)
    role = db.Column(db.Enum('customer', 'staff', 'admin'), nullable=False, default='customer')
    created_at = db.Column(db.TIMESTAMP, default=func.now())
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def get_id(self):
        return self.user_id

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Room(db.Model):
    __tablename__ = 'rooms'
    room_id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(50), unique=True, nullable=False)
    room_type = db.Column(db.String(100), nullable=False)
    price_per_night = db.Column(db.Numeric(10, 2), nullable=False)
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    features = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    bookings = db.relationship('Booking', backref='room', lazy=True)

class Booking(db.Model):
    __tablename__ = 'bookings'
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.room_id'), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), default='Confirmed', nullable=False) #e.g.,_Confirmed,_Checked-in,_Checked-out,_Cancelled
    payment_status = db.Column(db.String(50), default='Pending', nullable=False) #e.g.,_Pending,_Paid
    document_path = db.Column(db.String(255)) #Path_to_uploaded_document
    created_at = db.Column(db.TIMESTAMP, default=func.now())

class Notification(db.Model):
    __tablename__ = 'notifications'
    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id'), nullable=True)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50), nullable=False) #payment_verified,_booking_confirmed,_etc.
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=func.now())
    
    #Relationships
    user = db.relationship('User', backref='notifications', lazy=True)
    booking = db.relationship('Booking', backref='notifications', lazy=True)
    booking = db.relationship('Booking', backref='notifications', lazy=True)

