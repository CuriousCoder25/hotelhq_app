from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm
from ..models import User
from .. import db

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('customer.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role='customer'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'staff':
            return redirect(url_for('staff.dashboard'))
        else:
            return redirect(url_for('customer.dashboard'))
            
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login successful.', 'success')
            if next_page:
                return redirect(next_page)
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'staff':
                return redirect(url_for('staff.dashboard'))
            else:
                return redirect(url_for('customer.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('auth/login.html', title='Login', form=form, show_splash=True)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('customer.dashboard'))
        else:
            flash('Invalid old password.', 'danger')
    return render_template('auth/change_password.html', title='Change Password', form=form)

#Password_reset_routes-Simplified_for_local_college_project
#Validates_email_and_allows_direct_password_reset_without_email_service
@auth.route('/reset-password', methods=['GET', 'POST'])
def password_reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('customer.dashboard'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            #Store_email_in_session_for_password_reset
            from flask import session
            session['reset_email'] = user.email
            flash('Email verified! In a production environment, a password reset link would be sent to your email using Flask-Mail with an SMTP server. For this demo, you can proceed to reset your password directly.', 'success')
            return redirect(url_for('auth.password_reset'))
        else:
            flash('No account found with that email address.', 'danger')
    return render_template('auth/password_reset_request.html', title='Reset Password', form=form)

@auth.route('/reset-password-confirm', methods=['GET', 'POST'])
def password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('customer.dashboard'))
    
    from flask import session
    if 'reset_email' not in session:
        flash('Please enter your email first.', 'danger')
        return redirect(url_for('auth.password_reset_request'))
    
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=session['reset_email']).first()
        if user:
            user.set_password(form.password.data)
            db.session.commit()
            session.pop('reset_email', None)
            flash('Your password has been reset successfully! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('An error occurred. Please try again.', 'danger')
            return redirect(url_for('auth.password_reset_request'))
    return render_template('auth/password_reset.html', title='Reset Password', form=form)
