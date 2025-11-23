from flask import render_template, redirect, url_for, flash, request, send_from_directory, abort, jsonify
from flask_login import login_required, current_user
from . import customer
from .forms import ProfileForm, BookingForm, DocumentUploadForm
from ..models import User, Room, Booking, Notification
from .. import db
from ..utils import save_document, check_room_availability, get_booked_dates, is_room_fully_booked
from datetime import datetime

@customer.route('/dashboard')
@login_required
def dashboard():
    return render_template('customer/dashboard.html', title='Dashboard', show_splash=True)

@customer.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.contact = form.contact.data
        current_user.address = form.address.data
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('customer.profile'))
    return render_template('customer/profile.html', title='Profile', form=form)

@customer.route('/rooms')
def view_rooms():
    rooms = Room.query.all()
    
    #Add_availability_info_for_each_room
    for room in rooms:
        room.fully_booked = is_room_fully_booked(room.room_id)
    
    return render_template('customer/rooms.html', title='All Rooms', rooms=rooms)

@customer.route('/book/<int:room_id>', methods=['GET', 'POST'])
@login_required
def book_room(room_id):
    room = Room.query.get_or_404(room_id)
    
    form = BookingForm()
    if form.validate_on_submit():
        checkin = form.checkin_date.data
        checkout = form.checkout_date.data
        
        #Basic_validation_for_dates_(allow_same-day_checkout)
        if checkin > checkout:
            flash('Check-out date must be on or after check-in date.', 'danger')
            return redirect(url_for('customer.book_room', room_id=room_id))
        
        #Check_if_dates_are_available
        if not check_room_availability(room_id, checkin, checkout):
            flash('Sorry, this room is not available for the selected dates. Please choose different dates.', 'danger')
            return redirect(url_for('customer.book_room', room_id=room_id))

        #Calculate_total_price_(minimum_1_night_for_same-day_bookings)
        num_days = max(1, (checkout - checkin).days)
        total_price = room.price_per_night * num_days

        booking = Booking(
            room_id=room.room_id,
            user_id=current_user.user_id,
            check_in_date=checkin,
            check_out_date=checkout,
            total_price=total_price,
            status='Pending'  #Booking_starts_as_Pending_until_staff/admin_confirms
        )
        
        db.session.add(booking)
        db.session.commit()
        flash('Booking request submitted! Waiting for staff confirmation.', 'success')
        return redirect(url_for('customer.my_bookings'))
    
    #Get_booked_dates_for_calendar
    booked_dates = get_booked_dates(room_id)
    
    return render_template('customer/book_room.html', title='Book Room', form=form, room=room, booked_dates=booked_dates)

@customer.route('/my-bookings')
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.user_id).order_by(Booking.booking_id.desc()).all()
    return render_template('customer/my_bookings.html', title='My Bookings', bookings=bookings)

@customer.route('/upload-document/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def upload_document(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.user_id:
        return abort(403)
        
    form = DocumentUploadForm()
    if form.validate_on_submit():
        if form.document.data:
            doc_path = save_document(form.document.data)
            booking.document_path = doc_path
            db.session.commit()
            flash('Document uploaded successfully.', 'success')
            return redirect(url_for('customer.my_bookings'))
    return render_template('customer/upload_document.html', title='Upload Document', form=form, booking=booking)

@customer.route('/download-bill/<int:booking_id>')
@login_required
def download_bill(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.user_id:
        return abort(403)
    #Calculate_number_of_nights_(minimum_1_for_same-day_bookings)
    num_nights = max(1, (booking.check_out_date - booking.check_in_date).days)
    # Recalculate subtotal to ensure it's correct (in case old bookings exist)
    subtotal = booking.room.price_per_night * num_nights
    # This is a placeholder for generating and downloading a PDF bill.
    # For now, it just shows the booking details.
    return render_template('customer/bill.html', title='Invoice', booking=booking, num_nights=num_nights, subtotal=subtotal)

@customer.route('/notifications')
@login_required
def notifications():
    # Get all notifications for current user, ordered by newest first
    notifications = Notification.query.filter_by(user_id=current_user.user_id).order_by(Notification.created_at.desc()).all()
    
    # Count unread notifications
    unread_count = Notification.query.filter_by(user_id=current_user.user_id, is_read=False).count()
    
    return render_template('customer/notifications.html', title='Notifications', notifications=notifications, unread_count=unread_count)

@customer.route('/notifications/mark-read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.user_id:
        return abort(403)
    
    notification.is_read = True
    db.session.commit()
    return redirect(url_for('customer.notifications'))

@customer.route('/notifications/mark-all-read', methods=['POST'])
@login_required
def mark_all_notifications_read():
    Notification.query.filter_by(user_id=current_user.user_id, is_read=False).update({'is_read': True})
    db.session.commit()
    flash('All notifications marked as read.', 'success')
    return redirect(url_for('customer.notifications'))
