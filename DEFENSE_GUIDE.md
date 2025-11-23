# HotelHQ Defense Guide

## Project Overview
**Project Name:** HotelHQ - Hotel Management System  
**Framework:** Flask (Python Web Framework)  
**Architecture:** MVT (Model-View-Template)  
**Database:** MySQL with SQLAlchemy ORM  
**Frontend:** Tailwind CSS, HTML5, Jinja2 Templates  

---

## 1. ARCHITECTURE & DESIGN PATTERNS

### MVT Pattern Explanation
**Q: Explain the MVT architecture used in your project.**

**A:** Our project follows the Model-View-Template (MVT) pattern:

- **Model** (`app/models.py`): Defines database structure
  - `User` model: Stores user information (customers, staff, admin)
  - `Room` model: Manages hotel room data
  - `Booking` model: Handles reservations with foreign keys to User and Room

- **View** (Routes in `app/*/routes.py`): Business logic and request handling
  - `app/admin/routes.py`: Admin operations (CRUD for users, rooms, bookings)
  - `app/customer/routes.py`: Customer operations (booking, profile, documents)
  - `app/staff/routes.py`: Staff operations (booking management, payment verification)
  - `app/auth/routes.py`: Authentication (login, register, password change)

- **Template** (`app/templates/`): HTML presentation layer
  - Jinja2 templates for dynamic content rendering
  - Base template with inheritance for consistent UI
  - Partials (navbar, footer) for reusable components

### Blueprint Architecture
**Q: Why did you use Flask Blueprints?**

**A:** Blueprints provide modular organization:
- Separate concerns (auth, admin, customer, staff)
- Each module has its own routes, forms, and templates
- Easier maintenance and scalability
- Team can work on different modules simultaneously

---

## 2. DATABASE & ORM

### Database Schema
**Q: Explain your database relationships.**

**A:**
```
User (1) ----< (M) Booking (M) >---- (1) Room
```

**Relationships:**
- One User can have many Bookings (One-to-Many)
- One Room can have many Bookings (One-to-Many)
- Booking has Foreign Keys: `user_id`, `room_id`

**Key Fields:**
- User: `user_id` (PK), `username`, `email`, `password_hash`, `role`, `contact`, `address`
- Room: `room_id` (PK), `room_number`, `room_type`, `price_per_night`, `is_available`, `features`, `image_url`
- Booking: `booking_id` (PK), `user_id` (FK), `room_id` (FK), `check_in_date`, `check_out_date`, `total_price`, `status`, `payment_status`, `document_path`

### SQLAlchemy ORM
**Q: Why use ORM instead of raw SQL?**

**A:**
- **Security**: Protection against SQL injection
- **Abstraction**: Database-agnostic code
- **Productivity**: Python objects instead of SQL strings
- **Relationships**: Automatic foreign key handling
- **Migrations**: Easy schema updates with Flask-Migrate

**Example:**
```python
# Instead of: SELECT * FROM users WHERE user_id = 1
user = User.query.get(1)

# Instead of: INSERT INTO bookings (user_id, room_id, ...)
booking = Booking(user_id=1, room_id=5, ...)
db.session.add(booking)
db.session.commit()
```

---

## 3. AUTHENTICATION & AUTHORIZATION

### Flask-Login Implementation
**Q: How does your authentication system work?**

**A:**
- **Password Hashing**: Werkzeug's `generate_password_hash()` and `check_password_hash()`
- **Session Management**: Flask-Login maintains user sessions
- **User Loader**: `@login_manager.user_loader` decorator loads user from session
- **Protected Routes**: `@login_required` decorator restricts access

### Role-Based Access Control (RBAC)
**Q: How do you implement different user roles?**

**A:** Three roles with custom decorators:
- **Admin**: Full system access (user management, room management, all bookings)
- **Staff**: Booking management, payment verification, walk-in bookings
- **Customer**: Room browsing, booking creation, document upload, profile management

**Custom Decorators** (`app/decorators.py`):
```python
@admin_required  # Only allows role == 'admin'
@staff_required  # Only allows role == 'staff'
```

---

## 4. SECURITY FEATURES

### CSRF Protection
**Q: How do you prevent CSRF attacks?**

**A:** Flask-WTF provides CSRF tokens:
- Every form includes `{{ form.hidden_tag() }}` or `{{ form.csrf_token }}`
- Server validates token on POST requests
- Prevents unauthorized form submissions

### SQL Injection Prevention
**Q: How do you prevent SQL injection?**

**A:** 
- SQLAlchemy ORM parameterizes all queries automatically
- No raw SQL string concatenation
- User input is sanitized through form validation

### File Upload Security
**Q: How do you secure file uploads?**

**A:**
- **Filename Sanitization**: `secure_filename()` from Werkzeug
- **Unique Naming**: UUID-based filenames prevent collisions
- **Extension Validation**: Only allowed extensions (.jpg, .jpeg, .png, .pdf)
- **Storage Location**: Files stored in `app/static/uploads/`

---

## 5. FORMS & VALIDATION

### Flask-WTF Forms
**Q: Explain your form handling approach.**

**A:** All forms inherit from `FlaskForm`:

**Example:** `RoomForm` in `app/admin/forms.py`:
```python
class RoomForm(FlaskForm):
    room_number = StringField('Room Number', validators=[DataRequired()])
    room_type = SelectField('Room Type', choices=[...], validators=[DataRequired()])
    price_per_night = DecimalField('Price per Night', validators=[DataRequired()])
    # ...
```

**Validation Process:**
1. User submits form
2. `form.validate_on_submit()` checks CSRF and field validators
3. If valid: process data, redirect with flash message
4. If invalid: re-render form with error messages

---

## 6. FRONTEND & UI

### Tailwind CSS
**Q: Why Tailwind CSS?**

**A:**
- **Utility-First**: Rapid styling with predefined classes
- **Responsive**: Built-in breakpoint system
- **Consistent**: Design system with standardized spacing/colors
- **No Custom CSS**: Minimal custom stylesheet needed

### Template Inheritance
**Q: How do you maintain consistent UI?**

**A:** Base template pattern:
```jinja2
{# base.html #}
<!DOCTYPE html>
<html>
<head>...</head>
<body>
    {% include 'partials/navbar.html' %}
    <main>
        {% block content %}{% endblock %}
    </main>
    {% include 'partials/footer.html' %}
</body>
</html>

{# child template #}
{% extends 'base.html' %}
{% block content %}
    <!-- Page-specific content -->
{% endblock %}
```

### Animations & UX
**Q: How did you enhance user experience?**

**A:**
- **Logo Splash Screen**: Fade-in animation on site load
- **Hover Effects**: Transform scale, shadow elevation on buttons/cards
- **Transitions**: Smooth 200-300ms duration for all interactive elements
- **Flash Messages**: Color-coded feedback (green=success, red=error)

---

## 7. FILE STRUCTURE & ORGANIZATION

```
hotelhq/
├── app/
│   ├── __init__.py          # Flask app factory, extensions initialization
│   ├── models.py            # Database models (User, Room, Booking)
│   ├── config.py            # Configuration (database, secret key, upload folder)
│   ├── decorators.py        # Custom decorators (admin_required, staff_required)
│   ├── admin/               # Admin blueprint
│   │   ├── routes.py        # Admin routes
│   │   └── forms.py         # Admin forms
│   ├── customer/            # Customer blueprint
│   ├── staff/               # Staff blueprint
│   ├── auth/                # Authentication blueprint
│   ├── static/              # Static files
│   │   ├── css/
│   │   ├── js/
│   │   ├── images/
│   │   └── uploads/
│   └── templates/           # Jinja2 templates
│       ├── base.html
│       ├── admin/
│       ├── customer/
│       ├── staff/
│       └── partials/
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── first_run_setup.py       # Database initialization
└── README.md
```

---

## 8. KEY FEATURES IMPLEMENTATION

### Room Booking System
**Q: Walk through the booking process.**

**A:**
1. Customer views available rooms (`/customer/rooms`)
2. Clicks "Book Now" → redirects to booking form
3. Form validates dates, calculates total price
4. Creates Booking record with status="Pending"
5. Room marked as unavailable (`is_available=False`)
6. Redirect to "My Bookings" with success message

### Document Upload
**Q: How does document upload work?**

**A:**
1. Customer uploads document from "My Bookings"
2. File validated (extension, size)
3. Secure filename generated with UUID
4. File saved to `static/uploads/`
5. `document_path` updated in Booking record
6. Staff can view/download document during payment verification

### Payment Verification
**Q: Explain the payment flow.**

**A:**
1. Staff views all bookings with "Pending" status
2. Clicks "Verify Payment" for a booking
3. Reviews booking details and uploaded document
4. Changes `payment_status` to "Paid"
5. System sends confirmation (flash message)

---

## 9. COMMON DEFENSE QUESTIONS

### Q: How would you change a button's color?

**A:** Multiple approaches:

**1. Tailwind Utility Classes (Recommended):**
```html
<!-- Change from blue to green -->
<button class="bg-green-500 hover:bg-green-600 text-white...">Submit</button>
```

**2. Custom CSS in template:**
```html
<style>
    .custom-button {
        background-color: #10b981; /* green-500 */
    }
</style>
<button class="custom-button">Submit</button>
```

**3. Inline styles (Not recommended):**
```html
<button style="background-color: #10b981;">Submit</button>
```

### Q: How would you add a new field to a model?

**A:**
1. Update model in `models.py`:
```python
class Booking(db.Model):
    # ... existing fields
    special_requests = db.Column(db.Text, nullable=True)
```

2. Create migration:
```bash
flask db migrate -m "Add special_requests to Booking"
flask db upgrade
```

3. Update forms in `forms.py`:
```python
special_requests = TextAreaField('Special Requests')
```

4. Update templates to display/edit field

### Q: How would you add a new route?

**A:**
1. Add route in appropriate blueprint:
```python
@customer.route('/special-offers')
@login_required
def special_offers():
    # Logic here
    return render_template('customer/special_offers.html')
```

2. Create template: `templates/customer/special_offers.html`

3. Add navigation link in navbar

### Q: Explain your error handling.

**A:**
- **Form Validation**: WTForms validators catch input errors
- **Database Errors**: Try-except blocks with rollback
- **404 Errors**: `abort(404)` for not found resources
- **403 Errors**: `abort(403)` for unauthorized access
- **Flash Messages**: User-friendly error notifications
- **Debug Mode**: Werkzeug debugger in development

### Q: How would you optimize database queries?

**A:**
- **Eager Loading**: Use `joinedload()` to prevent N+1 queries
```python
bookings = Booking.query.options(
    db.joinedload(Booking.user),
    db.joinedload(Booking.room)
).all()
```
- **Pagination**: Limit results per page
- **Indexes**: Add indexes on frequently queried columns
- **Query Filtering**: Only fetch needed columns

---

## 10. POSSIBLE MODIFICATIONS (Practice These!)

### Change Navigation Bar Color
**File:** `app/templates/partials/navbar.html`
```html
<!-- Change from blue-600 to purple-600 -->
<nav class="bg-purple-600 text-white...">
```

### Add Tax to Bookings
**File:** `app/templates/customer/bill.html`
```html
<tr>
    <td>Tax (10%)</td>
    <td>${{ "%.2f"|format(booking.total_price|float * 0.10) }}</td>
</tr>
```

### Change Logo Size
**File:** `app/templates/base.html`
```css
#logo-splash .logo-image {
    max-width: 500px; /* Change from 400px */
    max-height: 500px;
}
```

### Add Email Validation
**File:** `app/admin/forms.py`
```python
from wtforms.validators import Email

email = StringField('Email', validators=[DataRequired(), Email()])
```

### Change Dashboard Card Hover Effect
**File:** Any dashboard template
```html
<!-- Change scale from 1.05 to 1.1 -->
<div class="... hover:scale-110 transition...">
```

---

## 11. TECHNICAL TERMS TO KNOW

- **ORM**: Object-Relational Mapping
- **CRUD**: Create, Read, Update, Delete
- **CSRF**: Cross-Site Request Forgery
- **FK**: Foreign Key
- **PK**: Primary Key
- **MVT**: Model-View-Template
- **Blueprint**: Flask's modular application component
- **Decorator**: Function wrapper (@login_required, @admin_required)
- **Session**: Server-side storage for user state
- **Migration**: Database schema version control
- **Jinja2**: Python template engine
- **Werkzeug**: WSGI utility library (password hashing, file handling)
- **SQLAlchemy**: Python SQL toolkit and ORM

---

## 12. DEMO SCRIPT

**Suggested Flow:**
1. Show splash screen animation
2. Register new customer account
3. Login as customer → browse rooms → book a room
4. Upload document for booking
5. Login as staff → view bookings → verify payment
6. Login as admin → manage users → add new room → view all bookings
7. Show responsive design (resize browser)
8. Demonstrate form validation (submit empty form)
9. Show CSRF protection (explain hidden token)
10. View bill with tax calculation

---

## 13. QUESTIONS TO PREPARE

1. Why did you choose Flask over Django?
2. What is the purpose of `__init__.py` in the app folder?
3. How does `current_user` work in Flask-Login?
4. What happens when you delete a room that has bookings?
5. How would you deploy this to production?
6. What testing strategies would you implement?
7. How would you add email notifications?
8. Explain the difference between GET and POST requests in your app.
9. How would you implement a search feature for rooms?
10. What security vulnerabilities should you be concerned about?

---

## 14. DEPENDENCIES (requirements.txt)

```
Flask==3.1.2
Flask-Login==0.6.3
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.2.2
mysql-connector-python==9.1.0
SQLAlchemy==2.0.44
WTForms==3.2.1
Werkzeug==3.1.3
Flask-Migrate==4.0.5
```

**Key Dependencies Explanation:**
- **Flask**: Core web framework
- **Flask-Login**: User session management
- **Flask-SQLAlchemy**: Database ORM integration
- **Flask-WTF**: Form handling and CSRF protection
- **mysql-connector-python**: MySQL database driver
- **Flask-Migrate**: Database migration tool

---

## 15. QUICK FIXES REFERENCE

### "Cannot import name 'X' from 'Y'"
- Check `__init__.py` imports
- Ensure circular imports are avoided
- Verify model definitions come before routes

### "CSRF token missing"
- Add `{{ form.hidden_tag() }}` or `{{ form.csrf_token }}` to forms
- Check `SECRET_KEY` is set in config

### "IntegrityError: foreign key constraint"
- Check foreign key relationships
- Ensure referenced records exist before creating dependent records
- Use cascading deletes for cleanup

### "Template not found"
- Verify template path matches route
- Check file exists in correct folder
- Ensure blueprint prefix is correct

### "AttributeError: 'User' object has no attribute 'id'"
- Use correct attribute name (`user_id` not `id`)
- Check model definition

---

## Additional Features & FAQ (Added)

### Notifications
- In-app notifications for users (see models and templates for implementation).

### Bulk Update Room Images
- Use `bulk_update_room_images.py` to update room images in bulk. Images should be placed in `app/static/images/`.

### Sample Data Seeding
- Use `seed_sample_data.py` to quickly populate the database for testing/demo.

### Password Reset & Admin Password Change
- Run `change_admin_password.py` to reset the admin password securely.
- Password reset for users is available via the authentication routes and templates.

### Responsive UI
- All templates use Tailwind CSS for mobile-friendly layouts.

### Testing
- Unit tests are located in the `tests/` folder. Run with your preferred test runner (e.g., pytest).

---

## Quick Reference: Setup & Usage

1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd hotelhq
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Configure database in `app/config.py`.
4. Run initial setup:
   ```sh
   python first_run_setup.py
   ```
5. (Optional) Seed sample data:
   ```sh
   python seed_sample_data.py
   ```
6. Start the application:
   ```sh
   python run.py
   ```

---

## Cross-References
- For setup and usage, see `README.md`.
- For change history, see `CHANGELOG.md`.

---

**Good luck with your defense! Know your code, understand the concepts, and be confident in explaining your design decisions.**
