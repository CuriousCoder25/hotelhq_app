
# 🏨 HotelHQ - Hotel Management System

A comprehensive web-based hotel management system built with Flask and MySQL, featuring role-based access control, real-time room tracking, and integrated billing functionality.

## ✨ Features

### 🔐 Role-Based Access Control
- **Admin**: Full system access, staff management, comprehensive dashboard
- **Staff**: Customer management, room bookings, document verification
- **Customer**: Personal portal, room booking, bill payments, document uploads

### 🏢 Core Functionality
- **Room Management**: Real-time availability tracking, room status updates
- **Customer Management**: Registration, profile management, document verification
- **Billing System**: Automated bill generation, payment processing
- **Staff Management**: Employee records, access control, performance tracking
- **Document Management**: Secure customer document storage and verification

### 📊 Dashboard & Reporting
- Real-time statistics and analytics
- Revenue tracking and reporting
- Occupancy rate monitoring
- Staff performance metrics

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed
- MySQL Server running
- Git installed

### 1. Clone the Repository
```bash
git clone https://github.com/CuriousCoder25/hotelhq_app.git
cd hotelhq_app
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv myenv

# Activate virtual environment
# For Windows:
myenv\Scripts\activate
# For Linux/Mac:
source myenv/bin/activate
```

### 3. Install Dependencies
```bash
pip install flask mysql-connector-python werkzeug
```

### 4. Database Setup
1. **Create Database:**
   ```sql
   CREATE DATABASE hotel_management;
   ```

2. **Import Database Schema:**
   ```bash
   mysql -u root -p hotel_management < "the database/hotel_management_new.sql"
   ```

3. **Configure Database Connection:**
   - Open `app.py`
   - Update the `DB_CONFIG` section with your MySQL credentials:
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'database': 'hotel_management',
       'user': 'your_mysql_username',
       'password': 'your_mysql_password',
       'charset': 'utf8mb4',
       'collation': 'utf8mb4_unicode_ci'
   }
   ```

### 5. Run the Application
```bash
python app.py
```

The application will be available at: `http://127.0.0.1:5000`

## 👥 Default User Accounts

### Admin Account
- **Username**: `admin`
- **Password**: `password`
- **Access**: Full system administration

### Staff Account
- **Username**: `staff01`
- **Password**: `password`
- **Access**: Customer and room management

### Creating Additional Users
Visit `http://127.0.0.1:5000/create_test_user` to create additional test accounts.

## 📁 Project Structure
```
hotelhq_app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/               # Static assets
│   ├── css/
│   ├── js/
│   ├── images/rooms/     # Room images
│   └── documents/customers/ # Customer documents
├── templates/            # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── rooms.html
│   ├── customers.html
│   ├── billing.html
│   ├── staff_management.html
│   └── customer_portal.html
└── the database/         # SQL schema files
    └── hotel_management_new.sql
```

## 🔧 Configuration

### Environment Variables
For production deployment, create a `.env` file:
```env
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DB_HOST=localhost
DB_NAME=hotel_management
DB_USER=your_username
DB_PASSWORD=your_password
```

### Security Settings
- Change the default `secret_key` in `app.py` for production
- Update default user passwords
- Configure HTTPS for production deployment

## 🌐 API Endpoints

### Authentication
- `POST /login` - User authentication
- `GET /logout` - User logout
- `POST /signup` - Customer registration

### Room Management (Admin)
- `GET /rooms` - Room management interface
- `POST /api/room/add` - Add new room
- `PUT /api/room/<id>/update` - Update room details
- `DELETE /api/room/<id>/delete` - Delete room

### Customer Management (Admin/Staff)
- `GET /customers` - Customer management interface
- `POST /api/customer/add` - Add new customer
- `DELETE /api/customer/<id>/remove` - Remove customer

### Staff Management (Admin)
- `GET /staff_management` - Staff management interface
- `POST /api/staff/add` - Add new staff member
- `PUT /api/staff/<id>/toggle` - Toggle staff status
- `DELETE /api/staff/<id>/delete` - Remove staff member

### Billing
- `GET /billing` - Billing management interface
- `POST /api/bill/add` - Create new bill
- `POST /api/bill/<id>/pay` - Process payment

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error:**
- Verify MySQL is running
- Check database credentials in `app.py`
- Ensure database exists and schema is imported

**Module Not Found:**
- Activate virtual environment: `myenv\Scripts\activate`
- Install dependencies: `pip install flask mysql-connector-python`

**KeyError in Staff Management:**
- Ensure database schema is up to date
- Run the latest SQL file from `the database/` folder

**Permission Denied:**
- Check user roles and permissions
- Verify login with correct credentials

### Development Mode
For development with auto-reload:
```bash
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows
python app.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Gaurav Kathayat**
- GitHub: [@CuriousCoder25](https://github.com/CuriousCoder25)
- Project: [HotelHQ](https://github.com/CuriousCoder25/hotelhq_app)

## 🙏 Acknowledgments

- Flask framework for web development
- MySQL for database management
- Bootstrap for responsive UI components
- All contributors and testers

