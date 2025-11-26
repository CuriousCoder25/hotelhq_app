from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from . import staff
from .forms import WalkInBookingForm, PaymentVerificationForm, RoomStatusForm, BookingStatusForm, ProfileForm
from ..models import Booking, Room, User, Notification
from .. import db
from ..decorators import staff_required
from ..utils import check_room_availability, get_booked_dates
from datetime import date

@staff.route('/dashboard')
@login_required
@staff_required
def dashboard():
    today = date.today()
    total_checkins = Booking.query.filter_by(check_in_date=today).count()
    return render_template('staff/dashboard.html', title='Staff Dashboard', total_checkins=total_checkins, show_splash=True)

@staff.route('/profile', methods=['GET', 'POST'])
@login_required
@staff_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.contact = form.contact.data
        current_user.address = form.address.data
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('staff.profile'))
    return render_template('staff/profile.html', title='My Profile', form=form)

@staff.route('/bookings')
@login_required
@staff_required
def view_bookings():
    bookings = Booking.query.order_by(Booking.booking_id.desc()).all()
    return render_template('staff/bookings.html', title='All Bookings', bookings=bookings)

@staff.route('/walk-in-booking', methods=['GET', 'POST'])
@login_required
@staff_required
def walk_in_booking():
    form = WalkInBookingForm()
    # Show all rooms in dropdown (availability will be checked for specific dates)
    form.room_id.choices = [(r.room_id, f"Room {r.room_number} - {r.room_type}") for r in Room.query.all()]
    
    if form.validate_on_submit():
        room = Room.query.get(form.room_id.data)
        
        # Check if room is available for the selected dates
        if not check_room_availability(form.room_id.data, form.checkin_date.data, form.checkout_date.data):
            flash('Sorry, this room is not available for the selected dates.', 'danger')
            return redirect(url_for('staff.walk_in_booking'))
        
        # For walk-ins, we can create a temporary user or use a generic one.
        # Here, we'll create a new user for each walk-in for simplicity.
        user = User.query.filter_by(email=form.customer_email.data).first()
        if not user:
            user = User(
                username=form.customer_name.data,
                email=form.customer_email.data,
                role='customer'
            )
            user.set_password('defaultpassword') # Or a random one
            db.session.add(user)
            db.session.commit()

        num_days = max(1, (form.checkout_date.data - form.checkin_date.data).days)
        total_price = room.price_per_night * num_days

        booking = Booking(
            room_id=form.room_id.data,
            user_id=user.user_id,
            check_in_date=form.checkin_date.data,
            check_out_date=form.checkout_date.data,
            total_price=total_price,
            payment_status='Paid', # Walk-in implies payment is made
            status='Confirmed' # Walk-in bookings are confirmed immediately
        )
        
        db.session.add(booking)
        db.session.commit()
        flash('Walk-in booking created successfully.', 'success')
        return redirect(url_for('staff.view_bookings'))
        
    return render_template('staff/walk_in_booking.html', title='Walk-in Booking', form=form)

@staff.route('/verify-payment/<int:booking_id>', methods=['GET', 'POST'])
@login_required
@staff_required
def verify_payment(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    form = PaymentVerificationForm(obj=booking)
    if form.validate_on_submit():
        old_status = booking.payment_status
        booking.payment_status = form.status.data
        
        # Create notification if payment was verified (changed to Paid)
        if old_status != 'Paid' and form.status.data == 'Paid':
            notification = Notification(
                user_id=booking.user_id,
                booking_id=booking.booking_id,
                message=f"Your payment for Room {booking.room.room_number} booking (Check-in: {booking.check_in_date.strftime('%Y-%m-%d')}) has been verified and confirmed!",
                notification_type='payment_verified'
            )
            db.session.add(notification)
            
            # Also update booking status to Confirmed if it was Pending
            if booking.status == 'Pending':
                booking.status = 'Confirmed'
                booking_notification = Notification(
                    user_id=booking.user_id,
                    booking_id=booking.booking_id,
                    message=f"Your booking for Room {booking.room.room_number} has been confirmed! Check-in: {booking.check_in_date.strftime('%Y-%m-%d')}",
                    notification_type='booking_confirmed'
                )
                db.session.add(booking_notification)
        
        db.session.commit()
        flash('Payment status updated.', 'success')
        return redirect(url_for('staff.view_bookings'))
    return render_template('staff/verify_payment.html', title='Verify Payment', form=form, booking=booking)

@staff.route('/update-room-status/<int:room_id>', methods=['POST'])
@login_required
@staff_required
def update_room_status(room_id):
    room = Room.query.get_or_404(room_id)
    
    # Check if status is sent from dropdown
    new_status = request.form.get('status')
    if new_status:
        room.is_available = (new_status == 'operational')
    else:
        # Fallback to toggle if no status sent
        room.is_available = not room.is_available
    
    status = "operational" if room.is_available else "under maintenance"
    db.session.commit()
    flash(f'Room {room.room_number} maintenance status updated to {status}.', 'success')
    return redirect(url_for('staff.manage_rooms'))

@staff.route('/rooms')
@login_required
@staff_required
def manage_rooms():
    rooms = Room.query.all()
    return render_template('staff/manage_rooms.html', title='Room Maintenance Status', rooms=rooms)

@staff.route('/checkout-booking/<int:booking_id>', methods=['POST'])
@login_required
@staff_required
def checkout_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    # Mark booking as completed
    booking.status = 'Completed'
    
    db.session.commit()
    flash('Booking checked out successfully.', 'success')
    return redirect(url_for('staff.view_bookings'))

@staff.route('/delete-booking/<int:booking_id>', methods=['POST'])
@login_required
@staff_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    db.session.delete(booking)
    db.session.commit()
    flash('Booking deleted successfully.', 'success')
    return redirect(url_for('staff.view_bookings'))

@staff.route('/booking/status/<int:booking_id>', methods=['GET', 'POST'])
@login_required
@staff_required
def change_booking_status(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    form = BookingStatusForm(obj=booking)
    
    if form.validate_on_submit():
        old_status = booking.status
        booking.status = form.status.data
        
        # Create notification for status change
        if old_status != form.status.data:
            notification = Notification(
                user_id=booking.user_id,
                booking_id=booking.booking_id,
                message=f"Your booking status for Room {booking.room.room_number} has been updated to: {form.status.data}",
                notification_type='booking_status_changed'
            )
            db.session.add(notification)
        
        db.session.commit()
        flash('Booking status updated successfully.', 'success')
        return redirect(url_for('staff.view_bookings'))
    
    return render_template('admin/change_status.html', title='Change Booking Status', form=form, booking=booking)

@staff.route('/view-bill/<int:booking_id>')
@login_required
@staff_required
def view_bill(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    num_nights = max(1, (booking.check_out_date - booking.check_in_date).days)
    subtotal = booking.room.price_per_night * num_nights        
    return render_template('customer/bill.html', title='Invoice', booking=booking, subtotal=subtotal)

@staff.route('/api/room/<int:room_id>/booked-dates')
@login_required
@staff_required
def get_room_booked_dates(room_id):
    """API endpoint to get booked dates for a specific room"""
    booked_dates = get_booked_dates(room_id)
    return jsonify(booked_dates)
