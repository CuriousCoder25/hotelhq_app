# 2-Day Crash Course: Bootstrap, HTML & Flask
*Hotel Management System Development Guide*

## Day 1: HTML & Bootstrap Fundamentals

### HTML Essentials
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hotel Management</title>
</head>
<body>
    <!-- Content goes here -->
</body>
</html>
```

**Key HTML Elements Used in Hotel System:**
- `<nav>` - Navigation bars
- `<div>` - Container elements
- `<form>` - User input forms
- `<table>` - Data display (room listings, customer data)
- `<button>` - Interactive elements
- `<input>` - Form fields (text, password, file uploads)
- `<select>` - Dropdown menus
- `<img>` - Room images

### Bootstrap 5.3.0 Framework

**CDN Links (used in base.html):**
```html
<!-- CSS -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<!-- JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

**Grid System:**
```html
<div class="container">
    <div class="row">
        <div class="col-md-6">Left column</div>
        <div class="col-md-6">Right column</div>
    </div>
</div>
```

**Key Bootstrap Classes Used:**
- `container`, `container-fluid` - Page layout
- `row`, `col-*` - Grid system
- `navbar`, `nav-link` - Navigation
- `btn`, `btn-primary`, `btn-success` - Buttons
- `card`, `card-header`, `card-body` - Content cards
- `form-control`, `form-group` - Form styling
- `alert`, `alert-success`, `alert-danger` - Messages
- `modal`, `modal-dialog` - Popup windows
- `table`, `table-striped` - Data tables

**Form Components:**
```html
<form class="needs-validation" novalidate>
    <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input type="email" class="form-control" id="email" required>
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

**Navigation Bar (from base.html):**
```html
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container">
        <a class="navbar-brand" href="#">Hotel Management</a>
        <ul class="navbar-nav">
            <li class="nav-item">
                <a class="nav-link" href="/dashboard">Dashboard</a>
            </li>
        </ul>
    </div>
</nav>
```

**Cards (used in rooms.html):**
```html
<div class="card">
    <div class="card-header">
        <h5>Room 101</h5>
    </div>
    <div class="card-body">
        <p>Room details...</p>
        <button class="btn btn-primary">Book Now</button>
    </div>
</div>
```

## Day 2: Flask Framework

### Flask Application Structure
```python
from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
```

### Key Flask Concepts Used in Hotel System:

**1. Routing & Methods:**
```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle form submission
        username = request.form['username']
        password = request.form['password']
    return render_template('login.html')

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    return jsonify({'rooms': room_data})
```

**2. Session Management:**
```python
# Login user
session['user_id'] = user_id
session['username'] = username
session['role'] = user_role

# Check if logged in
if 'user_id' not in session:
    return redirect(url_for('login'))

# Logout
session.clear()
```

**3. Template Rendering:**
```python
return render_template('dashboard.html', 
                     rooms=rooms, 
                     user=current_user)
```

**4. Database Integration (MySQL):**
```python
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='hotel_management',
            user='root',
            password='your_password'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def get_rooms():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM room")
    rooms = cursor.fetchall()
    cursor.close()
    connection.close()
    return rooms
```

**5. File Uploads (Room Images):**
```python
@app.route('/upload-room-image', methods=['POST'])
def upload_room_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file'})
    
    file = request.files['file']
    if file.filename != '':
        filename = secure_filename(file.filename)
        file.save(os.path.join('static/images/rooms', filename))
    
    return jsonify({'success': True})
```

**6. Decorators (Role-based Access):**
```python
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'Admin':
            flash('Admin access required', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html')
```

### Jinja2 Templates

**Template Inheritance (base.html):**
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Hotel Management{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

**Child Template:**
```html
{% extends "base.html" %}

{% block title %}Dashboard - Hotel Management{% endblock %}

{% block content %}
<h1>Welcome {{ session.username }}</h1>
{% endblock %}
```

**Template Variables & Logic:**
```html
<!-- Variables -->
<h1>Welcome {{ username }}</h1>

<!-- Loops -->
{% for room in rooms %}
    <div class="card">
        <h5>Room {{ room.room_number }}</h5>
        <p>Status: {{ room.status }}</p>
    </div>
{% endfor %}

<!-- Conditionals -->
{% if session.role == 'Admin' %}
    <button class="btn btn-primary">Admin Panel</button>
{% endif %}

<!-- URL Generation -->
<a href="{{ url_for('rooms') }}">View Rooms</a>
```

**Flash Messages:**
```python
# In Python
flash('Room added successfully!', 'success')
flash('Error: Room not found', 'error')
```

```html
<!-- In Template -->
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="alert alert-{{ category }}">{{ message }}</div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

### JavaScript Integration

**AJAX Requests (used in room management):**
```javascript
fetch('/api/rooms', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json'
    }
})
.then(response => response.json())
.then(data => {
    // Update UI with room data
    console.log(data);
});

// POST request for adding room
fetch('/api/rooms', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        room_number: '101',
        room_type: 'Single',
        price: 100.00
    })
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        alert('Room added successfully!');
    }
});
```

### Project Structure Best Practices

```
hotel_management/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── static/              # Static files
│   ├── css/
│   ├── js/
│   └── images/
├── templates/           # Jinja2 templates
│   ├── base.html       # Base template
│   ├── login.html      # Login page
│   └── dashboard.html  # Dashboard
└── myenv/              # Virtual environment
```

### Common Patterns in Hotel Management System:

**1. CRUD Operations:**
- Create: Add new rooms, customers
- Read: Display room lists, customer info
- Update: Edit room details, update bookings
- Delete: Remove customers, cancel bookings

**2. Form Validation:**
```python
if request.method == 'POST':
    username = request.form.get('username')
    if not username:
        flash('Username is required', 'error')
        return render_template('form.html')
```

**3. Role-Based Views:**
- Admin: Full access to all features
- Staff: Limited access to operations
- Customer: View and book rooms only

**4. Image Upload Handling:**
```python
import uuid
import os

def save_room_image(file):
    if file and file.filename:
        # Generate unique filename
        filename = str(uuid.uuid4()) + '.' + file.filename.split('.')[-1]
        filepath = os.path.join('static/images/rooms', filename)
        file.save(filepath)
        return filename
    return None
```

### Key Dependencies (requirements.txt):
```
Flask==2.3.3
mysql-connector-python==8.1.0
Werkzeug==2.3.7
```

### Development Commands:
```bash
# Create virtual environment
python -m venv myenv

# Activate environment (Windows)
myenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py
```

---

## Summary: Hotel Management System Implementation

This crash course covers the essential technologies used to build the Hotel Management System:

- **HTML**: Structure and content
- **Bootstrap**: Responsive design and UI components
- **Flask**: Backend framework and routing
- **MySQL**: Database operations
- **JavaScript**: Dynamic frontend interactions
- **Jinja2**: Template engine for dynamic content

The system demonstrates real-world application of these technologies in features like:
- User authentication and role-based access
- Room management with image uploads
- Customer portal and booking system
- Admin dashboard and reporting
- Responsive design for all devices
