from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, FileField
from wtforms.validators import DataRequired, Length, Email, Optional
from flask_wtf.file import FileAllowed

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact = StringField('Contact', validators=[Optional(), Length(max=20)])
    address = StringField('Address', validators=[Optional()])
    submit = SubmitField('Update Profile')

class BookingForm(FlaskForm):
    checkin_date = DateField('Check-in Date', validators=[DataRequired()], format='%Y-%m-%d')
    checkout_date = DateField('Check-out Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Book Now')

class DocumentUploadForm(FlaskForm):
    document = FileField('Legal Document (PDF/JPEG/PNG)', validators=[
        DataRequired(),
        FileAllowed(['pdf', 'jpeg', 'jpg', 'png'], 'Only PDF, JPEG and PNG files are allowed!')
    ])
    submit = SubmitField('Upload')
