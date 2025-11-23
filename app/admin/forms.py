from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DecimalField, FileField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flask_wtf.file import FileAllowed
from app.models import User

class RoomForm(FlaskForm):
    room_number = StringField('Room Number', validators=[DataRequired(), Length(max=50)])
    room_type = SelectField('Room Type', choices=[('Single', 'Single'), ('Double', 'Double'), ('Suite', 'Suite'), ('Deluxe', 'Deluxe')], validators=[DataRequired()])
    price_per_night = DecimalField('Price Per Night', validators=[DataRequired()])
    features = TextAreaField('Features')
    image = FileField('Room Image', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Save Room')

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[('staff', 'Staff'), ('admin', 'Admin')], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create User')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken.')

class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[('customer', 'Customer'), ('staff', 'Staff'), ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Update User')

    def __init__(self, user, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.original_email = user.email

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already taken.')

class BookingStatusForm(FlaskForm):
    status = SelectField('Booking Status', 
                        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), 
                                ('Checked-in', 'Checked-in'), ('Checked-out', 'Checked-out'), 
                                ('Cancelled', 'Cancelled')], 
                        validators=[DataRequired()])
    submit = SubmitField('Update Status')

class PaymentStatusForm(FlaskForm):
    payment_status = SelectField('Payment Status', 
                                choices=[('Pending', 'Pending'), ('Paid', 'Paid')], 
                                validators=[DataRequired()])
    submit = SubmitField('Update Payment')

class EditBookingForm(FlaskForm):
    check_in_date = DateField('Check-in Date', validators=[DataRequired()], format='%Y-%m-%d')
    check_out_date = DateField('Check-out Date', validators=[DataRequired()], format='%Y-%m-%d')
    room_id = SelectField('Room', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Update Booking')
