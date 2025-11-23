# HotelHQ - Hotel Room Booking Web App

![License: AGPL v3 + Commercial](https://img.shields.io/badge/License-AGPL--3.0-orange)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-Framework-green)

HotelHQ is a full-featured web application for booking and managing hotel rooms, built with Flask and MySQL.

## Demo

[Live Demo](#) <!-- Replace # with your demo URL when available -->

## Features

- **User Roles**: Customer, Staff, and Admin roles with different permissions.
- **Authentication**: Secure user registration, login, logout, and password management.
- **Room Management**: Admins can add, edit, and delete rooms.
- **Booking System**: Customers can book rooms, view booking history, and upload documents.
- **Staff Dashboard**: Staff can manage bookings and verify payments.
- **Admin Dashboard**: Admins have full control over rooms, users, and system settings.
- **Notifications**: In-app notifications for users.
- **Responsive UI**: Built with Tailwind CSS.
- **Bulk Update Room Images**: Script for updating room images in bulk.
- **Sample Data Seeding**: Script to seed sample data for testing.

## Project Structure

```
hotelhq/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── config.py
│   ├── utils.py
│   ├── decorators.py
│   ├── auth/
│   ├── customer/
│   ├── staff/
│   ├── admin/
│   ├── templates/
│   └── static/
├── migrations/
├── tests/
├── first_run_setup.py
├── seed_sample_data.py
├── run.py
├── requirements.txt
└── README.md
```

## Setup and Installation

### Prerequisites

- Python 3.8+
- XAMPP with MySQL
- Git

### Installation Steps

1.  **Clone the Repository**

    ```bash
    git clone <repository-url>
    cd hotelhq
    ```

2.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Database**

    -   Start MySQL server (e.g., via XAMPP)
    -   Update `app/config.py` with your database credentials

4.  **Run Initial Setup**

    ```bash
    python first_run_setup.py
    ```

5.  **Seed Sample Data (Optional)**

    ```bash
    python seed_sample_data.py
    ```

6.  **Start the Application**

    ```bash
    python run.py
    ```

## Usage

-   Access the admin, staff, and customer dashboards via the web interface.
-   Manage rooms, bookings, users, and payments.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License & Credit

This project is available under **two licenses**:

1. **AGPL-3.0 (Open Source)**
   - You can use, modify, and share this software for free.
   - **You must give proper credit**:
     - Keep this notice in the code files.
     - Mention the original repository in your documentation or README.
   - You must release any modifications under the same license if you host it publicly.

2. **Commercial / Proprietary License (Paid)**
   - Allows closed-source, private, or commercial use.
   - You must **contact <gauravkathayat945@gmail.com> for a commercial license**.
   - The license agreement will include credit requirements and other terms.


## FAQ

**Q: How do I reset the admin password?** A: Run `python change_admin_password.py` and follow the prompts.

**Q: How do I bulk update room images?** A: Use `python bulk_update_room_images.py` and provide the required image files.

---
For more technical details, see `DEFENSE_GUIDE.md`. For change history, see `CHANGELOG.md`.
