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
#     └── billing.html

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
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
    """Main dashboard"""
    connection = get_db_connection()
    stats = {
        'total_rooms': 0,
        'occupied_rooms': 0,
        'available_rooms': 0,
        'total_customers': 0,
        'pending_bills': 0,
        'total_revenue': 0
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
@login_required
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
@login_required
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
            LEFT JOIN room r ON c.Room_ID = r.Room_ID 
            ORDER BY c.created_at DESC
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
@login_required
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

@app.route('/api/room/<int:room_id>/checkin', methods=['POST'])
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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

if __name__ == '__main__':
    app.run(debug=True)