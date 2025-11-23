from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Optional, Length, Email

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact = StringField('Contact', validators=[Optional(), Length(max=20)])
    address = StringField('Address', validators=[Optional()])
    submit = SubmitField('Update Profile')

class WalkInBookingForm(FlaskForm):
    customer_name = StringField('Customer Name', validators=[DataRequired()])
    customer_email = StringField('Customer Email', validators=[DataRequired()])
    room_id = SelectField('Room', coerce=int, validators=[DataRequired()])
    checkin_date = DateField('Check-in Date', validators=[DataRequired()], format='%Y-%m-%d')
    checkout_date = DateField('Check-out Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Create Booking')

class PaymentVerificationForm(FlaskForm):
    status = SelectField('Payment Status', choices=[
        ('Pending', 'Pending'),
        ('Paid', 'Paid')
    ], validators=[DataRequired()])
    submit = SubmitField('Update Status')

class RoomStatusForm(FlaskForm):
    status = SelectField('Room Status', choices=[
        ('operational', 'Operational'),
        ('maintenance', 'Under Maintenance')
    ], validators=[DataRequired()])
    submit = SubmitField('Update Status')

class BookingStatusForm(FlaskForm):
    status = SelectField('Booking Status', 
                        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), 
                                ('Checked-in', 'Checked-in'), ('Checked-out', 'Checked-out'), 
                                ('Cancelled', 'Cancelled')], 
                        validators=[DataRequired()])
    submit = SubmitField('Update Status')
