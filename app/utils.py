import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app
from datetime import datetime, timedelta

def allowed_file(filename):
    """Checks if the file's extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_document(file):
    """Saves an uploaded document with a secure, unique filename."""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = str(uuid.uuid4()) + os.path.splitext(filename)[1]
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        return unique_filename
    return None

def check_room_availability(room_id, check_in_date, check_out_date, exclude_booking_id=None):
    """
    Check if a room is available for the given date range.
    Returns True if available, False if there's a conflict.
    
    Args:
        room_id: The room to check
        check_in_date: Desired check-in date
        check_out_date: Desired check-out date
        exclude_booking_id: Optional booking ID to exclude from check (for editing existing bookings)
    """
    from .models import Booking, Room
    
    # First check if room is operational (not under maintenance)
    room = Room.query.get(room_id)
    if not room or not room.is_available:
        return False  # Room is under maintenance or doesn't exist
    
    # Query for conflicting bookings
    query = Booking.query.filter(
        Booking.room_id == room_id,
        Booking.status.in_(['Pending', 'Confirmed', 'Checked-in']),  # Only active bookings
        # Check for date overlap: 
        # For same-day bookings (check_in == check_out), we need to check if dates match exactly
        # For multi-day bookings, check if ranges overlap
        Booking.check_in_date <= check_out_date,
        Booking.check_out_date >= check_in_date
    )
    
    # Exclude current booking if editing
    if exclude_booking_id:
        query = query.filter(Booking.booking_id != exclude_booking_id)
    
    conflicting_bookings = query.all()
    
    return len(conflicting_bookings) == 0

def get_booked_dates(room_id, days_ahead=40):
    """
    Get all booked date ranges for a room for the next X days.
    Returns a list of dicts with check_in and check_out dates.
    """
    from .models import Booking
    
    today = datetime.now().date()
    end_date = today + timedelta(days=days_ahead)
    
    bookings = Booking.query.filter(
        Booking.room_id == room_id,
        Booking.status.in_(['Pending', 'Confirmed', 'Checked-in']),
        Booking.check_out_date > today,  # Only future/current bookings
        Booking.check_in_date <= end_date  # Within our date range
    ).all()
    
    booked_ranges = []
    for booking in bookings:
        booked_ranges.append({
            'check_in': booking.check_in_date.strftime('%Y-%m-%d'),
            'check_out': booking.check_out_date.strftime('%Y-%m-%d'),
            'booking_id': booking.booking_id
        })
    
    return booked_ranges

def is_room_fully_booked(room_id, days_ahead=40):
    """
    Check if a room is fully booked for the next X days.
    Returns True if there are no available dates in the range.
    """
    from .models import Booking, Room
    
    # First check if room is operational
    room = Room.query.get(room_id)
    if not room or not room.is_available:
        return True  # Room under maintenance counts as "fully booked"
    
    today = datetime.now().date()
    end_date = today + timedelta(days=days_ahead)
    total_days = days_ahead
    
    # Get all active bookings within the range
    bookings = Booking.query.filter(
        Booking.room_id == room_id,
        Booking.status.in_(['Confirmed', 'Checked-in']),  # Only confirmed bookings count
        Booking.check_out_date > today,
        Booking.check_in_date < end_date
    ).all()
    
    if not bookings:
        return False
    
    # Count booked days
    booked_days = set()
    for booking in bookings:
        current_date = max(booking.check_in_date, today)
        end = min(booking.check_out_date, end_date)
        
        while current_date < end:
            booked_days.add(current_date)
            current_date += timedelta(days=1)
    
    # If all days are booked, room is fully booked
    return len(booked_days) >= total_days

