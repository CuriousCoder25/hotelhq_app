from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import admin
from .forms import RoomForm, UserForm, EditUserForm, BookingStatusForm, PaymentStatusForm, EditBookingForm
from ..models import Room, User, Booking, Notification
from .. import db
from ..decorators import admin_required
from ..utils import save_document, check_room_availability
import os

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html', title='Admin Dashboard', show_splash=True)

# Room Management
@admin.route('/rooms')
@login_required
@admin_required
def manage_rooms():
    rooms = Room.query.all()
    return render_template('admin/manage_rooms.html', title='Manage Rooms', rooms=rooms)

@admin.route('/room/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_room():
    form = RoomForm()
    if form.validate_on_submit():
        image_url = None
        if form.image.data:
            image_url = save_document(form.image.data)
        
        room = Room(
            room_number=form.room_number.data,
            room_type=form.room_type.data,
            price_per_night=form.price_per_night.data,
            features=form.features.data,
            image_url=image_url
        )
        db.session.add(room)
        db.session.commit()
        flash('Room added successfully.', 'success')
        return redirect(url_for('admin.manage_rooms'))
    return render_template('admin/add_edit_room.html', title='Add Room', form=form)

@admin.route('/room/edit/<int:room_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_room(room_id):
    room = Room.query.get_or_404(room_id)
    form = RoomForm(obj=room)
    if form.validate_on_submit():
        if form.image.data:
            # Optionally, delete old image
            if room.image_url:
                try:
                    os.remove(os.path.join('app', 'static', 'uploads', room.image_url))
                except OSError:
                    pass # Ignore if file doesn't exist
            room.image_url = save_document(form.image.data)

        room.room_number = form.room_number.data
        room.room_type = form.room_type.data
        room.price_per_night = form.price_per_night.data
        room.features = form.features.data
        db.session.commit()
        flash('Room updated successfully.', 'success')
        return redirect(url_for('admin.manage_rooms'))
    return render_template('admin/add_edit_room.html', title='Edit Room', form=form, room=room)

@admin.route('/room/toggle-maintenance/<int:room_id>', methods=['POST'])
@login_required
@admin_required
def toggle_room_maintenance(room_id):
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
    flash(f'Room {room.room_number} is now {status}.', 'success')
    return redirect(url_for('admin.manage_rooms'))

@admin.route('/room/delete/<int:room_id>', methods=['POST'])
@login_required
@admin_required
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    
    # Check if room has any bookings
    bookings_count = Booking.query.filter_by(room_id=room_id).count()
    if bookings_count > 0:
        flash(f'Cannot delete room {room.room_number}. It has {bookings_count} booking(s) associated with it. Please delete or reassign the bookings first.', 'danger')
        return redirect(url_for('admin.manage_rooms'))
    
    db.session.delete(room)
    db.session.commit()
    flash('Room deleted successfully.', 'success')
    return redirect(url_for('admin.manage_rooms'))

# User Management
@admin.route('/users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/manage_users.html', title='Manage Users', users=users)

@admin.route('/user/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully.', 'success')
        return redirect(url_for('admin.manage_users'))
    return render_template('admin/add_user.html', title='Add User', form=form)

@admin.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm(user=user, obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data
        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('admin.manage_users'))
    return render_template('admin/edit_user.html', title='Edit User', form=form, user=user)

@admin.route('/user/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    # Add check to prevent admin from deleting themselves
    if user.user_id == current_user.user_id:
        flash("You cannot delete your own account.", "danger")
        return redirect(url_for('admin.manage_users'))
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('admin.manage_users'))

# Booking Management
@admin.route('/bookings')
@login_required
@admin_required
def manage_bookings():
    bookings = Booking.query.order_by(Booking.booking_id.desc()).all()
    return render_template('admin/manage_bookings.html', title='Manage Bookings', bookings=bookings)

@admin.route('/booking/delete/<int:booking_id>', methods=['POST'])
@login_required
@admin_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    db.session.delete(booking)
    db.session.commit()
    flash('Booking deleted successfully.', 'success')
    return redirect(url_for('admin.manage_bookings'))

@admin.route('/booking/edit/<int:booking_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    form = EditBookingForm(obj=booking)
    
    # Populate room choices
    rooms = Room.query.all()
    form.room_id.choices = [(room.room_id, f'Room {room.room_number} - {room.room_type}') for room in rooms]
    
    if form.validate_on_submit():
        new_room = Room.query.get(form.room_id.data)
        
        # Check if new dates/room are available (excluding current booking)
        if not check_room_availability(form.room_id.data, form.check_in_date.data, form.check_out_date.data, exclude_booking_id=booking_id):
            flash('Sorry, the selected room is not available for these dates.', 'danger')
            return redirect(url_for('admin.edit_booking', booking_id=booking_id))
        
        # Update booking details (dates and room only)
        booking.check_in_date = form.check_in_date.data
        booking.check_out_date = form.check_out_date.data
        booking.room_id = form.room_id.data
        
        # Recalculate total price
        num_days = (form.check_out_date.data - form.check_in_date.data).days
        booking.total_price = new_room.price_per_night * num_days
        
        db.session.commit()
        flash('Booking updated successfully.', 'success')
        return redirect(url_for('admin.manage_bookings'))
    
    # Pre-populate form
    form.room_id.data = booking.room_id
    
    return render_template('admin/edit_booking.html', title='Edit Booking', form=form, booking=booking)

@admin.route('/booking/status/<int:booking_id>', methods=['GET', 'POST'])
@login_required
@admin_required
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
        return redirect(url_for('admin.manage_bookings'))
    
    return render_template('admin/change_status.html', title='Change Booking Status', form=form, booking=booking)

@admin.route('/booking/payment/<int:booking_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def change_payment_status(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    form = PaymentStatusForm(obj=booking)
    
    if form.validate_on_submit():
        old_status = booking.payment_status
        booking.payment_status = form.payment_status.data
        
        # Create notification if payment verified
        if old_status != 'Paid' and form.payment_status.data == 'Paid':
            notification = Notification(
                user_id=booking.user_id,
                booking_id=booking.booking_id,
                message=f"Your payment for Room {booking.room.room_number} booking (Check-in: {booking.check_in_date.strftime('%Y-%m-%d')}) has been verified!",
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
        flash('Payment status updated successfully.', 'success')
        return redirect(url_for('admin.manage_bookings'))
    
    return render_template('admin/change_payment.html', title='Change Payment Status', form=form, booking=booking)

@admin.route('/booking/cancel/<int:booking_id>', methods=['POST'])
@login_required
@admin_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.status = 'Cancelled'
    
    # Create notification
    notification = Notification(
        user_id=booking.user_id,
        booking_id=booking.booking_id,
        message=f"Your booking for Room {booking.room.room_number} has been cancelled.",
        notification_type='booking_cancelled'
    )
    db.session.add(notification)
    
    db.session.commit()
    flash('Booking cancelled successfully.', 'success')
    return redirect(url_for('admin.manage_bookings'))

@admin.route('/booking/view-bill/<int:booking_id>')
@login_required
@admin_required
def view_bill(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    # Calculate number of nights (minimum 1 for same-day bookings)
    num_nights = max(1, (booking.check_out_date - booking.check_in_date).days)
    # Recalculate subtotal to ensure it's correct
    subtotal = booking.room.price_per_night * num_nights
    return render_template('admin/view_bill.html', title='View Bill', booking=booking, num_nights=num_nights, subtotal=subtotal)

@admin.route('/logs')
@login_required
@admin_required
def view_logs():
    # This is a placeholder. A real implementation would involve a logging service.
    logs = ["Log entry 1: User logged in", "Log entry 2: Room booked"]
    return render_template('admin/view_logs.html', title='System Logs', logs=logs)
