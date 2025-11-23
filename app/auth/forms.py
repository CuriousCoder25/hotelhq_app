from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from app.models import User

#Custom_password_strength_validator
def validate_password_strength(form, field):
    password = field.data
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not any(char.isupper() for char in password):
        raise ValidationError('Password must contain at least one uppercase letter.')
    if not any(char.islower() for char in password):
        raise ValidationError('Password must contain at least one lowercase letter.')
    if not any(char.isdigit() for char in password):
        raise ValidationError('Password must contain at least one number.')
    if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?' for char in password):
        raise ValidationError('Password must contain at least one special character (!@#$%^&*() etc.).')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), validate_password_strength])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken. Please choose a different one.')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), validate_password_strength])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), validate_password_strength])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
