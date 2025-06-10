# Hotel Management System - Flask Application
# File structure:
# hotel_app/
# ├── app.py (this file)
# ├── config.py
# ├── requirements.txt
# ├── static/
# │   ├── css/
# │   │   └── style.css
# │   └── js/
# │       └── main.js
# └── templates/
#     ├── base.html
#     ├── login.html
#     ├── dashboard.html
#     ├── rooms.html
#     ├── customers.html
#     ├── billing.html
#     └── schema_update.html

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from mysql.connector import Error
import mysql.connector  # Add this line
from datetime import datetime, timedelta
import os
import uuid
from functools import wraps
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'hotel_management',
    'user': 'root',  # Change to your MySQL username
    'password': '',  # Change to your MySQL password
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

def get_db_connection():
    """Create database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def login_required(f):
    """Decorator to require login for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin/staff role for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('role') not in ['Admin', 'Staff']:
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('customer_portal'))
        return f(*args, **kwargs)
    return decorated_function

def staff_required(f):
    """Decorator to require staff or admin role for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('role') not in ['Admin', 'Staff']:
            flash('Access denied. Staff privileges required.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Home page - redirect to login or dashboard"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                # Get user with role information
                query = """
                SELECT l.Username, l.User_ID, l.Password, r.Role_name 
                FROM login l 
                JOIN role r ON l.Role_ID = r.Role_ID 
                WHERE l.Username = %s AND l.is_active = TRUE
                """
                cursor.execute(query, (username,))
                user = cursor.fetchone()
                
                if user and check_password_hash(user['Password'], password):
                    session['user_id'] = user['User_ID']
                    session['username'] = user['Username']
                    session['role'] = user['Role_name']
                    
                    # Update last login
                    update_query = "UPDATE login SET last_login = %s WHERE Username = %s"
                    cursor.execute(update_query, (datetime.now(), username))
                    connection.commit()
                    
                    flash('Login successful!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Invalid username or password!', 'error')
                    
            except Error as e:
                flash(f'Database error: {e}', 'error')
            finally:
                cursor.close()
                connection.close()
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out successfully!', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard with role-based redirection"""
    user_role = session.get('role')
    
    # Redirect users to their specific dashboards
    if user_role == 'Customer':
        return redirect(url_for('customer_portal'))
    elif user_role == 'Staff':
        return redirect(url_for('staff_dashboard'))
    elif user_role == 'Admin':
        # Show admin dashboard
        pass
    else:
        flash('Invalid user role', 'error')
        return redirect(url_for('logout'))
    
    connection = get_db_connection()
    stats = {
        'total_rooms': 0,
        'occupied_rooms': 0,
        'available_rooms': 0,
        'total_customers': 0,
        'total_staff': 0,
        'pending_bills': 0,
        'total_revenue': 0,
        'pending_documents': 0
    }
    
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            # Get room statistics
            cursor.execute("SELECT COUNT(*) as total FROM room")
            stats['total_rooms'] = cursor.fetchone()['total']
            
            cursor.execute("SELECT COUNT(*) as occupied FROM room WHERE Status = 'Occupied'")
            stats['occupied_rooms'] = cursor.fetchone()['occupied']
            
            cursor.execute("SELECT COUNT(*) as available FROM room WHERE Status = 'Available'")
            stats['available_rooms'] = cursor.fetchone()['available']
            
            # Get customer count
            cursor.execute("SELECT COUNT(*) as total FROM customer")
            stats['total_customers'] = cursor.fetchone()['total']
            
            # Get billing statistics
            cursor.execute("SELECT COUNT(*) as pending FROM billing WHERE Status = 'Pending'")
            stats['pending_bills'] = cursor.fetchone()['pending']
            
            cursor.execute("SELECT SUM(Total_amount) as revenue FROM billing WHERE Status = 'Paid'")
            result = cursor.fetchone()
            stats['total_revenue'] = float(result['revenue']) if result['revenue'] else 0
            
        except Error as e:
            flash(f'Error loading dashboard: {e}', 'error')
        finally:
            cursor.close()
            connection.close()
    
    return render_template('dashboard.html', stats=stats)

@app.route('/rooms')
@admin_required  # Changed from @login_required
def rooms():
    """Room management page"""
    connection = get_db_connection()
    rooms = []
    
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            query = """
            SELECT r.*, c.First_Name, c.Last_Name 
            FROM room r 
            LEFT JOIN customer c ON r.User_ID = c.User_ID 
            ORDER BY r.room_number
            """
            cursor.execute(query)
            rooms = cursor.fetchall()
        except Error as e:
            flash(f'Error loading rooms: {e}', 'error')
        finally:
            cursor.close()
            connection.close()
    
    return render_template('rooms.html', rooms=rooms)

@app.route('/customers')
@admin_required  # Changed from @login_required
def customers():
    """Customer management page"""
    connection = get_db_connection()
    customers = []
    
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            query = """
            SELECT c.*, r.room_number, r.Status as room_status
            FROM customer c 
            LEFT JOIN room r ON c.User_ID = r.User_ID 
            ORDER BY c.User_ID DESC
            """
            cursor.execute(query)
            customers = cursor.fetchall()
        except Error as e:
            flash(f'Error loading customers: {e}', 'error')
        finally:
            cursor.close()
            connection.close()
    
    return render_template('customers.html', customers=customers)

@app.route('/billing')
@admin_required  # Changed from @login_required
def billing():
    """Billing management page"""
    connection = get_db_connection()
    bills = []
    
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            query = """
            SELECT b.*, c.First_Name, c.Last_Name 
            FROM billing b 
            JOIN customer c ON b.User_ID = c.User_ID 
            ORDER BY b.Date_Time DESC
            """
            cursor.execute(query)
            bills = cursor.fetchall()
        except Error as e:
            flash(f'Error loading billing: {e}', 'error')
        finally:
            cursor.close()
            connection.close()
    
    return render_template('billing.html', bills=bills)

# Protect all API endpoints
@app.route('/api/room/<int:room_id>/checkin', methods=['POST'])
@admin_required  # Changed from @login_required
def checkin_room(room_id):
    """API endpoint to check in a customer to a room"""
    data = request.json
    customer_id = data.get('customer_id')
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Update room status
            cursor.execute("""
                UPDATE room 
                SET Status = 'Occupied', User_ID = %s, Check_In = %s 
                WHERE Room_ID = %s
            """, (customer_id, datetime.now(), room_id))
            
            # Update customer room assignment
            cursor.execute("""
                UPDATE customer 
                SET Room_ID = %s 
                WHERE User_ID = %s
            """, (room_id, customer_id))
            
            connection.commit()
            return jsonify({'success': True, 'message': 'Check-in successful'})
            
        except Error as e:
            connection.rollback()
            return jsonify({'success': False, 'error': str(e)})
        finally:
            cursor.close()
            connection.close()
    
    return jsonify({'success': False, 'error': 'Database connection failed'})

@app.route('/api/room/<int:room_id>/checkout', methods=['POST'])
@admin_required
def checkout_room(room_id):
    """API endpoint to check out a customer from a room"""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Update room status
            cursor.execute("""
                UPDATE room 
                SET Status = 'Available', User_ID = NULL, Check_Out = %s 
                WHERE Room_ID = %s
            """, (datetime.now(), room_id))
            
            # Update customer room assignment
            cursor.execute("""
                UPDATE customer 
                SET Room_ID = NULL 
                WHERE Room_ID = %s
            """, (room_id,))
            
            connection.commit()
            return jsonify({'success': True, 'message': 'Check-out successful'})
            
        except Error as e:
            connection.rollback()
            return jsonify({'success': False, 'error': str(e)})
        finally:
            cursor.close()
            connection.close()
    
    return jsonify({'success': False, 'error': 'Database connection failed'})

@app.route('/api/customer/add', methods=['POST'])
@admin_required
def add_customer():
    """API endpoint to add a new customer"""
    data = request.json
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            query = """
            INSERT INTO customer (First_Name, Last_Name, Mobile_no, email, address) 
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data['first_name'],
                data['last_name'],
                data['mobile'],
                data['email'],
                data['address']
            ))
            connection.commit()
            return jsonify({'success': True, 'message': 'Customer added successfully'})
            
        except Error as e:
            return jsonify({'success': False, 'error': str(e)})
        finally:
            cursor.close()
            connection.close()
    
    return jsonify({'success': False, 'error': 'Database connection failed'})

@app.route('/api/bill/add', methods=['POST'])
@admin_required
def add_bill():
    """API endpoint to add a new bill"""
    data = request.json
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            query = """
            INSERT INTO billing (User_ID, Item, Quantity, Rate, Total_Tax, Total_amount, Billed_by, Status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data['customer_id'],
                data['item'],
                data['quantity'],
                data['rate'],
                data['tax'],
                data['total'],
                session['username'],
                'Pending'
            ))
            connection.commit()
            return jsonify({'success': True, 'message': 'Bill added successfully'})
            
        except Error as e:
            return jsonify({'success': False, 'error': str(e)})
        finally:
            cursor.close()
            connection.close()
    
    return jsonify({'success': False, 'error': 'Database connection failed'})

@app.route('/api/bill/<int:bill_id>/pay', methods=['POST'])
@admin_required
def pay_bill(bill_id):
    """API endpoint to mark a bill as paid"""
    data = request.json
    payment_method = data.get('payment_method', 'Cash')
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                UPDATE billing 
                SET Status = 'Paid', payment_method = %s 
                WHERE Bill_no = %s
            """, (payment_method, bill_id))
            connection.commit()
            return jsonify({'success': True, 'message': 'Payment processed successfully'})
            
        except Error as e:
            return jsonify({'success': False, 'error': str(e)})
        finally:
            cursor.close()
            connection.close()
    
    return jsonify({'success': False, 'error': 'Database connection failed'})

@app.route('/create_test_user')
def create_test_user():
    """Temporary route to create test user"""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Create hashed password for 'admin123'
            hashed_password = generate_password_hash('admin123')
            
            # Insert or update admin user
            query = """
            INSERT INTO login (Username, Password, Role_ID, is_active) 
            VALUES ('admin', %s, 1, TRUE)
            ON DUPLICATE KEY UPDATE Password = %s
            """
            cursor.execute(query, (hashed_password, hashed_password))
            connection.commit()
            
            return "Test user created! Username: admin, Password: admin123"
        except Error as e:
            return f"Error: {e}"
        finally:
            cursor.close()
            connection.close()
    return "Database connection failed"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Customer registration"""
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')
        
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Check if username already exists
                cursor.execute("SELECT Username FROM login WHERE Username = %s", (username,))
                if cursor.fetchone():
                    flash('Username already exists. Please choose a different one.', 'error')
                    return render_template('signup.html')
                
                # Create login account with CUSTOMER role (change Role_ID to correct value)
                hashed_password = generate_password_hash(password)
                cursor.execute("""
                    INSERT INTO login (Username, Password, Role_ID, is_active) 
                    VALUES (%s, %s, 3, TRUE)
                """, (username, hashed_password))  # Changed from 2 to 3 (assuming Customer is Role_ID 3)
                
                user_id = cursor.lastrowid
                
                # Create customer record
                cursor.execute("""
                    INSERT INTO customer (User_ID, First_Name, Last_Name, email, Mobile_no) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, first_name, last_name, email, phone))
                
                connection.commit()
                flash('Account created successfully! Please login.', 'success')
                return redirect(url_for('login'))
                
            except Error as e:
                connection.rollback()
                flash(f'Error creating account: {e}', 'error')
                return render_template('signup.html')
            finally:
                cursor.close()
                connection.close()
        else:
            flash('Database connection failed', 'error')
            return render_template('signup.html')
    
    return render_template('signup.html')

@app.route('/customer_portal')
@login_required
def customer_portal():
    """Customer portal - for customers only"""
    if session.get('role') != 'Customer':
        return redirect(url_for('dashboard'))
    
    connection = get_db_connection()
    customer_data = {
        'bookings': [],
        'bills': [],
        'profile': {},
        'available_rooms': []
    }
    
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            user_id = session['user_id']
            
            # Get customer profile
            cursor.execute("""
                SELECT * FROM customer WHERE User_ID = %s
            """, (user_id,))
            customer_data['profile'] = cursor.fetchone()
            
            # Get customer's room bookings
            cursor.execute("""
                SELECT r.* FROM room r WHERE r.User_ID = %s
            """, (user_id,))
            customer_data['bookings'] = cursor.fetchall()
            
            # Get customer's bills
            cursor.execute("""
                SELECT * FROM billing WHERE User_ID = %s ORDER BY Date_Time DESC
            """, (user_id,))
            customer_data['bills'] = cursor.fetchall()
              # Get available rooms for booking (include all details for enhanced customer view)
            cursor.execute("""
                SELECT Room_ID, room_number, Room_type, Room_Price, Status, description, room_image
                FROM room 
                WHERE Status = 'Available' OR Status = 'Clean'
                ORDER BY room_number
            """)
            customer_data['available_rooms'] = cursor.fetchall()
            
        except Error as e:
            flash(f'Error loading data: {e}', 'error')
        finally:
            cursor.close()
            connection.close()
    
    return render_template('customer_portal.html', data=customer_data)

@app.route('/api/customer/book-room/<int:room_id>', methods=['POST'])
@login_required
def book_room(room_id):
    """API endpoint for customers to book rooms"""
    if session.get('role') != 'Customer':
        return jsonify({'success': False, 'error': 'Unauthorized'})
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Check if room is available
            cursor.execute("SELECT Status FROM room WHERE Room_ID = %s", (room_id,))
            room = cursor.fetchone()
            
            if not room or room[0] not in ['Available', 'Clean']:
                return jsonify({'success': False, 'error': 'Room not available'})
            
            # Book the room
            user_id = session['user_id']
            cursor.execute("""
                UPDATE room 
                SET Status = 'Occupied', User_ID = %s, Check_In = %s 
                WHERE Room_ID = %s
            """, (user_id, datetime.now(), room_id))
            
            connection.commit()
            return jsonify({'success': True, 'message': 'Room booked successfully'})
            
        except Error as e:
            return jsonify({'success': False, 'error': str(e)})
        finally:
            cursor.close()
            connection.close()
    
    return jsonify({'success': False, 'error': 'Database connection failed'})

@app.route('/api/customer/<int:customer_id>/remove', methods=['DELETE'])
@admin_required
def remove_customer(customer_id):
    """API endpoint to remove a customer"""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Check if customer exists and get their User_ID
            cursor.execute("SELECT User_ID FROM customer WHERE User_ID = %s", (customer_id,))
            customer = cursor.fetchone()
            
            if not customer:
                return jsonify({'success': False, 'error': 'Customer not found'})
            
            user_id = customer[0]
            
            # Check if customer has any active room bookings
            cursor.execute("SELECT COUNT(*) FROM room WHERE User_ID = %s AND Status = 'Occupied'", (user_id,))
            active_bookings = cursor.fetchone()[0]
            
            if active_bookings > 0:
                return jsonify({'success': False, 'error': 'Cannot remove customer with active room bookings'})
            
            # Check if customer has unpaid bills
            cursor.execute("SELECT COUNT(*) FROM billing WHERE User_ID = %s AND Status = 'Pending'", (user_id,))
            unpaid_bills = cursor.fetchone()[0]
            
            if unpaid_bills > 0:
                return jsonify({'success': False, 'error': 'Cannot remove customer with unpaid bills'})
            
            # Remove customer's room assignments (if any)
            cursor.execute("UPDATE room SET User_ID = NULL, Check_In = NULL, Check_Out = NULL WHERE User_ID = %s", (user_id,))
            
            # Delete customer record
            cursor.execute("DELETE FROM customer WHERE User_ID = %s", (user_id,))
            
            # Delete login record
            cursor.execute("DELETE FROM login WHERE User_ID = %s", (user_id,))
            
            connection.commit()
            return jsonify({'success': True, 'message': 'Customer removed successfully'})
            
        except Error as e:
            connection.rollback()
            return jsonify({'success': False, 'error': str(e)})
        finally:
            cursor.close()
            connection.close()
    
    return jsonify({'success': False, 'error': 'Database connection failed'})

# New Room Management API Endpoints

@app.route('/api/room/add', methods=['POST'])
@admin_required
def add_room():
    """API endpoint to add a new room"""
    try:
        room_number = request.form.get('room_number')
        room_type = request.form.get('room_type')
        price = request.form.get('price')
        status = request.form.get('status')
        description = request.form.get('description', '')
        
        # Handle image upload
        image_filename = None
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                # Create images directory if it doesn't exist
                import os
                os.makedirs('static/images/rooms', exist_ok=True)
                
                # Generate unique filename
                import uuid
                filename = f"{uuid.uuid4()}_{image.filename}"
                image_path = f"static/images/rooms/{filename}"
                image.save(image_path)
                image_filename = filename
        
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # First check which columns exist
                cursor.execute("DESCRIBE room")
                columns = [col[0] for col in cursor.fetchall()]
                
                # Build insert query based on available columns
                base_columns = ['room_number', 'Status']
                base_values = [room_number, status]
                
                # Add optional columns if they exist
                if 'Room_type' in columns:
                    base_columns.append('Room_type')
                    base_values.append(room_type)
                elif 'Room_Category' in columns:
                    base_columns.append('Room_Category')
                    base_values.append(room_type)
                elif 'category' in columns:
                    base_columns.append('category')
                    base_values.append(room_type)
                
                if 'Room_Price' in columns:
                    base_columns.append('Room_Price')
                    base_values.append(float(price))
                elif 'price' in columns:
                    base_columns.append('price')
                    base_values.append(float(price))
                
                if 'description' in columns:
                    base_columns.append('description')
                    base_values.append(description)
                
                if 'room_image' in columns:
                    base_columns.append('room_image')
                    base_values.append(image_filename)
                
                # Build and execute query
                placeholders = ', '.join(['%s'] * len(base_values))
                columns_str = ', '.join(base_columns)
                query = f"INSERT INTO room ({columns_str}) VALUES ({placeholders})"
                
                cursor.execute(query, base_values)
                connection.commit()
                return jsonify({'success': True, 'message': 'Room added successfully'})
                
            except Error as e:
                connection.rollback()
                return jsonify({'success': False, 'error': str(e)})
            finally:
                cursor.close()
                connection.close()
        
        return jsonify({'success': False, 'error': 'Database connection failed'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/room/<int:room_id>', methods=['GET'])
@admin_required
def get_room(room_id):
    """API endpoint to get room details"""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM room WHERE Room_ID = %s", (room_id,))
            room = cursor.fetchone()
            
            if room:
                return jsonify({'success': True, 'room': room})
            else:
                return jsonify({'success': False, 'error': 'Room not found'})
                
        except Error as e:
            return jsonify({'success': False, 'error': str(e)})
        finally:
            cursor.close()
            connection.close()
    
    return jsonify({'success': False, 'error': 'Database connection failed'})

@app.route('/api/room/<int:room_id>/update', methods=['PUT'])
@admin_required
def update_room(room_id):
    """API endpoint to update room details"""
    try:
        room_number = request.form.get('room_number')
        room_type = request.form.get('room_type')
        price = request.form.get('price')
        status = request.form.get('status')
        description = request.form.get('description', '')
        
        # Handle image upload
        image_filename = None
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                # Create images directory if it doesn't exist
                import os
                os.makedirs('static/images/rooms', exist_ok=True)
                
                # Generate unique filename
                import uuid
                filename = f"{uuid.uuid4()}_{image.filename}"
                image_path = f"static/images/rooms/{filename}"
                image.save(image_path)
                image_filename = filename
        
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # First check which columns exist
                cursor.execute("DESCRIBE room")
                columns = [col[0] for col in cursor.fetchall()]
                
                # Build update query based on available columns
                update_parts = ['room_number = %s', 'Status = %s']
                update_values = [room_number, status]
                
                # Add optional columns if they exist
                if 'Room_type' in columns:
                    update_parts.append('Room_type = %s')
                    update_values.append(room_type)
                elif 'Room_Category' in columns:
                    update_parts.append('Room_Category = %s')
                    update_values.append(room_type)
                elif 'category' in columns:
                    update_parts.append('category = %s')
                    update_values.append(room_type)
                
                if 'Room_Price' in columns:
                    update_parts.append('Room_Price = %s')
                    update_values.append(float(price))
                elif 'price' in columns:
                    update_parts.append('price = %s')
                    update_values.append(float(price))
                
                if 'description' in columns:
                    update_parts.append('description = %s')
                    update_values.append(description)
                
                if image_filename and 'room_image' in columns:
                    update_parts.append('room_image = %s')
                    update_values.append(image_filename)
                
                # Add WHERE clause parameter
                update_values.append(room_id)
                
                # Build and execute query
                update_str = ', '.join(update_parts)
                query = f"UPDATE room SET {update_str} WHERE Room_ID = %s"
                
                cursor.execute(query, update_values)
                connection.commit()
                return jsonify({'success': True, 'message': 'Room updated successfully'})
                
            except Error as e:
                connection.rollback()
                return jsonify({'success': False, 'error': str(e)})
            finally:
                cursor.close()
                connection.close()
        
        return jsonify({'success': False, 'error': 'Database connection failed'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/room/<int:room_id>/status', methods=['PUT'])
@admin_required
def change_room_status(room_id):
    """API endpoint to change room status"""
    data = request.json
    new_status = data.get('status')
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                UPDATE room 
                SET Status = %s 
                WHERE Room_ID = %s
            """, (new_status, room_id))
            
            connection.commit()
            return jsonify({'success': True, 'message': f'Room status changed to {new_status}'})
            
        except Error as e:
            connection.rollback()
            return jsonify({'success': False, 'error': str(e)})
        finally:
            cursor.close()
            connection.close()
    
    return jsonify({'success': False, 'error': 'Database connection failed'})

@app.route('/api/room/<int:room_id>/delete', methods=['DELETE'])
@admin_required
def delete_room(room_id):
    """API endpoint to delete a room"""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Check if room is occupied
            cursor.execute("SELECT Status FROM room WHERE Room_ID = %s", (room_id,))
            room = cursor.fetchone()
            
            if not room:
                return jsonify({'success': False, 'error': 'Room not found'})
            
            if room[0] == 'Occupied':
                return jsonify({'success': False, 'error': 'Cannot delete occupied room'})
            
            # Delete the room
            cursor.execute("DELETE FROM room WHERE Room_ID = %s", (room_id,))
            
            connection.commit()
            return jsonify({'success': True, 'message': 'Room deleted successfully'})
            
        except Error as e:
            connection.rollback()
            return jsonify({'success': False, 'error': str(e)})
        finally:
            cursor.close()
            connection.close()
    
    return jsonify({'success': False, 'error': 'Database connection failed'})

@app.route('/debug/room-columns')
@admin_required
def debug_room_columns():
    """Debug route to check room table structure"""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("DESCRIBE room")
            columns = cursor.fetchall()
            column_info = []
            for col in columns:
                column_info.append({
                    'Field': col[0],
                    'Type': col[1],
                    'Null': col[2],
                    'Key': col[3],
                    'Default': col[4],
                    'Extra': col[5]
                })
            return jsonify({'success': True, 'columns': column_info})
        except Error as e:
            return jsonify({'success': False, 'error': str(e)})
        finally:
            cursor.close()
            connection.close()
    return jsonify({'success': False, 'error': 'Database connection failed'})

@app.route('/debug/update-schema', methods=['POST'])
@admin_required
def update_room_schema():
    """Update room table schema to add missing columns"""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Get current columns
            cursor.execute("DESCRIBE room")
            columns = [col[0] for col in cursor.fetchall()]
            
            updates_made = []
            
            # Add Room_type column if missing
            if 'Room_type' not in columns:
                try:
                    cursor.execute("ALTER TABLE room ADD COLUMN Room_type VARCHAR(50) DEFAULT 'Standard'")
                    updates_made.append('Room_type')
                except Error as e:
                    if "Duplicate column name" not in str(e):
                        raise e
            
            # Add description column if missing
            if 'description' not in columns:
                try:
                    cursor.execute("ALTER TABLE room ADD COLUMN description TEXT")
                    updates_made.append('description')
                except Error as e:
                    if "Duplicate column name" not in str(e):
                        raise e
            
            # Add room_image column if missing
            if 'room_image' not in columns:
                try:
                    cursor.execute("ALTER TABLE room ADD COLUMN room_image VARCHAR(255)")
                    updates_made.append('room_image')
                except Error as e:
                    if "Duplicate column name" not in str(e):
                        raise e
            
            # Add Room_Price column if missing
            if 'Room_Price' not in columns:
                try:
                    cursor.execute("ALTER TABLE room ADD COLUMN Room_Price DECIMAL(10,2) NOT NULL DEFAULT 0.00")
                    updates_made.append('Room_Price')
                except Error as e:
                    if "Duplicate column name" not in str(e):
                        raise e
            
            # Update existing rooms without Room_type
            if 'Room_type' in updates_made or 'Room_type' in columns:
                cursor.execute("UPDATE room SET Room_type = 'Standard' WHERE Room_type IS NULL OR Room_type = ''")
            
            connection.commit()
            
            return jsonify({
                'success': True, 
                'message': f'Schema updated successfully. Added columns: {", ".join(updates_made) if updates_made else "No new columns needed"}',
                'updates': updates_made
            })
            
        except Error as e:
            connection.rollback()
            return jsonify({'success': False, 'error': str(e)})
        finally:
            cursor.close()
            connection.close()
    
    return jsonify({'success': False, 'error': 'Database connection failed'})

@app.route('/admin/schema-update')
@admin_required
def schema_update_page():
    """Display schema update page"""
    return render_template('schema_update.html')

# Customer API endpoints for enhanced portal

@app.route('/api/customer/upload-documents', methods=['POST'])
@login_required
def upload_customer_documents():
    """API endpoint for customers to upload legal documents"""
    if session.get('role') != 'Customer':
        return jsonify({'success': False, 'error': 'Unauthorized'})
    
    try:
        user_id = session['user_id']
        
        # Create documents directory if it doesn't exist
        docs_dir = 'static/documents/customers'
        os.makedirs(docs_dir, exist_ok=True)
        
        uploaded_files = []
        
        # Handle ID document upload
        if 'id_document' in request.files:
            id_file = request.files['id_document']
            if id_file.filename != '':
                filename = f"{user_id}_id_{uuid.uuid4()}_{id_file.filename}"
                id_path = os.path.join(docs_dir, filename)
                id_file.save(id_path)
                uploaded_files.append(('ID Document', filename))
        
        # Handle address proof upload
        if 'address_proof' in request.files:
            address_file = request.files['address_proof']
            if address_file.filename != '':
                filename = f"{user_id}_address_{uuid.uuid4()}_{address_file.filename}"
                address_path = os.path.join(docs_dir, filename)
                address_file.save(address_path)
                uploaded_files.append(('Address Proof', filename))
        
        if not uploaded_files:
            return jsonify({'success': False, 'error': 'No files uploaded'})
        
        # TODO: Store document information in database
        # For now, we'll just confirm upload success
        
        return jsonify({
            'success': True, 
            'message': f'Successfully uploaded {len(uploaded_files)} document(s)',
            'files': uploaded_files
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/customer/update-profile', methods=['PUT'])
@login_required
def update_customer_profile():
    """API endpoint for customers to update their profile"""
    if session.get('role') != 'Customer':
        return jsonify({'success': False, 'error': 'Unauthorized'})
    
    data = request.json
    user_id = session['user_id']
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Update customer profile
            query = """
            UPDATE customer 
            SET First_Name = %s, Last_Name = %s, email = %s, Mobile_no = %s, address = %s
            WHERE User_ID = %s
            """
            cursor.execute(query, (
                data.get('first_name'),
                data.get('last_name'),
                data.get('email'),
                data.get('phone'),
                data.get('address'),
                user_id
            ))
            
            connection.commit()
            return jsonify({'success': True, 'message': 'Profile updated successfully'})
            
        except Error as e:
            connection.rollback()
            return jsonify({'success': False, 'error': str(e)})
        finally:
            cursor.close()
            connection.close()
    
    return jsonify({'success': False, 'error': 'Database connection failed'})

@app.route('/api/customer/pay-bill/<int:bill_id>', methods=['POST'])
@login_required
def customer_pay_bill(bill_id):
    """API endpoint for customers to pay their bills"""
    if session.get('role') != 'Customer':
        return jsonify({'success': False, 'error': 'Unauthorized'})
    
    data = request.json
    payment_method = data.get('payment_method', 'Online')
    user_id = session['user_id']
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Verify the bill belongs to the customer
            cursor.execute("SELECT User_ID FROM billing WHERE Bill_no = %s", (bill_id,))
            bill = cursor.fetchone()
            
            if not bill or bill[0] != user_id:
                return jsonify({'success': False, 'error': 'Bill not found or unauthorized'})
            
            # Update bill status to paid
            cursor.execute("""
                UPDATE billing 
                SET Status = 'Paid', payment_method = %s 
                WHERE Bill_no = %s
            """, (payment_method, bill_id))
            
            connection.commit()
            return jsonify({'success': True, 'message': 'Payment processed successfully'})
            
        except Error as e:
            connection.rollback()
            return jsonify({'success': False, 'error': str(e)})
        finally:
            cursor.close()
            connection.close()
    
    return jsonify({'success': False, 'error': 'Database connection failed'})

@app.route('/staff_management')
@admin_required
def staff_management():
    """Staff management page - Admin only"""
    connection = get_db_connection()
    staff_members = []
    staff_stats = {
        'total': 0,
        'active': 0,
        'inactive': 0,
        'new_this_month': 0
    }
    
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            # First, check if created_at column exists in login table
            cursor.execute("DESCRIBE login")
            login_columns = [col['Field'] for col in cursor.fetchall()]
            
            # Build query based on available columns
            if 'created_at' in login_columns:
                query = """
                SELECT l.User_ID, l.Username, l.is_active, l.created_at, l.last_login,
                       s.First_Name, s.Last_Name, s.email, s.Mobile_no, s.position, s.hire_date
                FROM login l 
                LEFT JOIN staff s ON l.User_ID = s.User_ID
                WHERE l.Role_ID = 2
                ORDER BY l.created_at DESC
                """
            else:
                # Fallback query without created_at column
                query = """
                SELECT l.User_ID, l.Username, l.is_active, l.last_login,
                       s.First_Name, s.Last_Name, s.email, s.Mobile_no, s.position, s.hire_date
                FROM login l 
                LEFT JOIN staff s ON l.User_ID = s.User_ID
                WHERE l.Role_ID = 2
                ORDER BY l.User_ID DESC
                """
            
            cursor.execute(query)
            staff_members = cursor.fetchall()
            
            # Debug: print raw results
            print(f"Debug: Found {len(staff_members)} staff members")
            if staff_members:
                print(f"Debug: First staff member keys: {list(staff_members[0].keys()) if staff_members[0] else 'None'}")
            
            # Calculate statistics safely
            staff_stats['total'] = len(staff_members) if staff_members else 0
            staff_stats['active'] = len([s for s in staff_members if s and s.get('is_active')]) if staff_members else 0
            staff_stats['inactive'] = len([s for s in staff_members if s and not s.get('is_active')]) if staff_members else 0
            
            # Count new staff this month
            from datetime import datetime, timedelta
            thirty_days_ago = datetime.now() - timedelta(days=30)
            staff_stats['new_this_month'] = 0
            if staff_members:
                staff_stats['new_this_month'] = len([
                    s for s in staff_members 
                    if s and s.get('hire_date') and s['hire_date'] >= thirty_days_ago.date()
                ])
            
        except Error as e:
            print(f"Database Error: {e}")  # Debug print
            flash(f'Error loading staff: {e}', 'error')
        finally:
            cursor.close()
            connection.close()
    
    return render_template('staff_management.html', staff_members=staff_members, staff_stats=staff_stats)

@app.route('/api/staff/add', methods=['POST'])
@admin_required
def add_staff():
    """API endpoint to add new staff member"""
    data = request.json
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Check if username already exists
            cursor.execute("SELECT Username FROM login WHERE Username = %s", (data['username'],))
            if cursor.fetchone():
                return jsonify({'success': False, 'error': 'Username already exists'})
            
            # Create login account with STAFF role (Role_ID = 2)
            hashed_password = generate_password_hash(data['password'])
            cursor.execute("""
                INSERT INTO login (Username, Password, Role_ID, is_active) 
                VALUES (%s, %s, 2, TRUE)
            """, (data['username'], hashed_password))
            
            user_id = cursor.lastrowid
            
            # Create staff record
            cursor.execute("""
                INSERT INTO staff (User_ID, First_Name, Last_Name, email, Mobile_no, position, hire_date) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (user_id, data['first_name'], data['last_name'], data['email'], 
                  data['phone'], data['position'], datetime.now().date()))
            
            connection.commit()
            return jsonify({'success': True, 'message': 'Staff member added successfully'})
            
        except Error as e:
            connection.rollback()
            return jsonify({'success': False, 'error': str(e)})
        finally:
            cursor.close()
            connection.close()
    
    return jsonify({'success': False, 'error': 'Database connection failed'})

@app.route('/api/staff/<int:staff_id>/delete', methods=['DELETE'])
@admin_required
def delete_staff(staff_id):
    """API endpoint to delete staff member"""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Check if staff exists
            cursor.execute("SELECT User_ID FROM staff WHERE User_ID = %s", (staff_id,))
            if not cursor.fetchone():
                return jsonify({'success': False, 'error': 'Staff member not found'})
            
            # Delete staff record
            cursor.execute("DELETE FROM staff WHERE User_ID = %s", (staff_id,))
            
            # Delete login record
            cursor.execute("DELETE FROM login WHERE User_ID = %s", (staff_id,))
            
            connection.commit()
            return jsonify({'success': True, 'message': 'Staff member deleted successfully'})
            
        except Error as e:
            connection.rollback()
            return jsonify({'success': False, 'error': str(e)})
        finally:
            cursor.close()
            connection.close()
    
    return jsonify({'success': False, 'error': 'Database connection failed'})

@app.route('/api/staff/<int:staff_id>/toggle', methods=['PUT'])
@admin_required
def toggle_staff_status(staff_id):
    """API endpoint to toggle staff active/inactive status"""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Toggle is_active status
            cursor.execute("""
                UPDATE login 
                SET is_active = NOT is_active 
                WHERE User_ID = %s AND Role_ID = 2
            """, (staff_id,))
            
            connection.commit()
            return jsonify({'success': True, 'message': 'Staff status updated successfully'})
            
        except Error as e:
            connection.rollback()
            return jsonify({'success': False, 'error': str(e)})
        finally:
            cursor.close()
            connection.close()
    
    return jsonify({'success': False, 'error': 'Database connection failed'})

@app.route('/staff_dashboard')
@login_required
def staff_dashboard():
    """Staff dashboard - for staff members only"""
    if session.get('role') != 'Staff':
        return redirect(url_for('dashboard'))
    
    connection = get_db_connection()
    staff_data = {
        'pending_documents': [],
        'today_checkins': [],
        'today_checkouts': [],
        'available_rooms': [],
        'recent_bookings': [],
        'stats': {
            'pending_docs': 0,
            'today_checkins': 0,
            'available_rooms': 0,
            'total_customers': 0
        }
    }
    
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            # Get customers with pending document verification
            cursor.execute("""
                SELECT c.*, l.Username 
                FROM customer c 
                JOIN login l ON c.User_ID = l.User_ID 
                WHERE c.document_status != 'Approved' OR c.document_status IS NULL
                ORDER BY c.User_ID DESC
                LIMIT 10
            """)
            staff_data['pending_documents'] = cursor.fetchall()
            staff_data['stats']['pending_docs'] = len(staff_data['pending_documents'])
            
            # Get today's check-ins
            cursor.execute("""
                SELECT r.*, c.First_Name, c.Last_Name 
                FROM room r 
                JOIN customer c ON r.User_ID = c.User_ID 
                WHERE DATE(r.Check_In) = CURDATE() AND r.Status = 'Occupied'
                ORDER BY r.Check_In DESC
            """)
            staff_data['today_checkins'] = cursor.fetchall()
            staff_data['stats']['today_checkins'] = len(staff_data['today_checkins'])
            
            # Get available rooms
            cursor.execute("""
                SELECT Room_ID, room_number, Room_type, Room_Price, Status 
                FROM room 
                WHERE Status IN ('Available', 'Clean')
                ORDER BY room_number
            """)
            staff_data['available_rooms'] = cursor.fetchall()
            staff_data['stats']['available_rooms'] = len(staff_data['available_rooms'])
            
            # Get total customers
            cursor.execute("SELECT COUNT(*) as total FROM customer")
            staff_data['stats']['total_customers'] = cursor.fetchone()['total']
            
            # Get recent bookings
            cursor.execute("""
                SELECT r.*, c.First_Name, c.Last_Name 
                FROM room r 
                JOIN customer c ON r.User_ID = c.User_ID 
                WHERE r.Status = 'Occupied'
                ORDER BY r.Check_In DESC
                LIMIT 5
            """)
            staff_data['recent_bookings'] = cursor.fetchall()
            
        except Error as e:
            flash(f'Error loading dashboard: {e}', 'error')
        finally:
            cursor.close()
            connection.close()
    
    return render_template('staff_dashboard.html', data=staff_data)

# Staff API endpoints for customer management and document verification

@app.route('/api/staff/customer/add', methods=['POST'])
@staff_required
def staff_add_customer():
    """API endpoint for staff to add new customers"""
    data = request.json
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Check if username already exists
            cursor.execute("SELECT Username FROM login WHERE Username = %s", (data['username'],))
            if cursor.fetchone():
                return jsonify({'success': False, 'error': 'Username already exists'})
            
            # Create login account with CUSTOMER role (Role_ID = 3)
            hashed_password = generate_password_hash(data['password'])
            cursor.execute("""
                INSERT INTO login (Username, Password, Role_ID, is_active) 
                VALUES (%s, %s, 3, TRUE)
            """, (data['username'], hashed_password))
            
            user_id = cursor.lastrowid
            
            # Create customer record
            cursor.execute("""
                INSERT INTO customer (User_ID, First_Name, Last_Name, email, Mobile_no, address, document_status) 
                VALUES (%s, %s, %s, %s, %s, %s, 'Pending')
            """, (user_id, data['first_name'], data['last_name'], data['email'], 
                  data['phone'], data['address']))
            
            connection.commit()
            return jsonify({'success': True, 'message': 'Customer added successfully', 'user_id': user_id})
            
        except Error as e:
            connection.rollback()
            return jsonify({'success': False, 'error': str(e)})
        finally:
            cursor.close()
            connection.close()
    
    return jsonify({'success': False, 'error': 'Database connection failed'})

@app.route('/api/staff/room/<int:room_id>/book', methods=['POST'])
@staff_required
def staff_book_room():
    """API endpoint for staff to book rooms for customers"""
    data = request.json
    room_id = data.get('room_id')
    customer_id = data.get('customer_id')
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Check if room is available
            cursor.execute("SELECT Status FROM room WHERE Room_ID = %s", (room_id,))
            room = cursor.fetchone()
            
            if not room or room[0] not in ['Available', 'Clean']:
                return jsonify({'success': False, 'error': 'Room not available'})
            
            # Check if customer exists
            cursor.execute("SELECT User_ID FROM customer WHERE User_ID = %s", (customer_id,))
            if not cursor.fetchone():
                return jsonify({'success': False, 'error': 'Customer not found'})
            
            # Book the room
            cursor.execute("""
                UPDATE room 
                SET Status = 'Occupied', User_ID = %s, Check_In = %s 
                WHERE Room_ID = %s
            """, (customer_id, datetime.now(), room_id))
            
            connection.commit()
            return jsonify({'success': True, 'message': 'Room booked successfully'})
            
        except Error as e:
            connection.rollback()
            return jsonify({'success': False, 'error': str(e)})
        finally:
            cursor.close()
            connection.close()
    
    return jsonify({'success': False, 'error': 'Database connection failed'})

@app.route('/api/staff/document/verify/<int:customer_id>', methods=['PUT'])
@staff_required
def verify_customer_documents(customer_id):
    """API endpoint for staff to verify customer documents"""
    data = request.json
    status = data.get('status')  # 'Approved', 'Rejected', 'Pending'
    notes = data.get('notes', '')
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Update customer document status
            cursor.execute("""
                UPDATE customer 
                SET document_status = %s, verification_notes = %s, verified_by = %s, verification_date = %s
                WHERE User_ID = %s
            """, (status, notes, session['username'], datetime.now(), customer_id))
            
            connection.commit()
            return jsonify({'success': True, 'message': f'Document status updated to {status}'})
            
        except Error as e:
            connection.rollback()
            return jsonify({'success': False, 'error': str(e)})
        finally:
            cursor.close()
            connection.close()
    
    return jsonify({'success': False, 'error': 'Database connection failed'})

@app.route('/api/staff/booking/confirm/<int:room_id>', methods=['POST'])
@staff_required
def confirm_booking(room_id):
    """API endpoint for staff to confirm customer bookings"""
    data = request.json
    customer_id = data.get('customer_id')
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Check if customer documents are approved
            cursor.execute("SELECT document_status FROM customer WHERE User_ID = %s", (customer_id,))
            customer = cursor.fetchone()
            
            if not customer:
                return jsonify({'success': False, 'error': 'Customer not found'})
            
            if customer[0] != 'Approved':
                return jsonify({'success': False, 'error': 'Customer documents must be verified before confirming booking'})
            
            # Update room booking confirmation
            cursor.execute("""
                UPDATE room 
                SET booking_confirmed = TRUE, confirmed_by = %s, confirmation_date = %s
                WHERE Room_ID = %s AND User_ID = %s
            """, (session['username'], datetime.now(), room_id, customer_id))
            
            connection.commit()
            return jsonify({'success': True, 'message': 'Booking confirmed successfully'})
            
        except Error as e:
            connection.rollback()
            return jsonify({'success': False, 'error': str(e)})
        finally:
            cursor.close()
            connection.close()
    
    return jsonify({'success': False, 'error': 'Database connection failed'})

if __name__ == '__main__':
    app.run(debug=True)