# HotelHQ - Hotel Room Booking Web App

![License: GK-OSNC 1.0](https://img.shields.io/badge/License-GK--OSNC%201.0-blue.svg)
![Commercial License](https://img.shields.io/badge/Commercial-License%20Available-orange.svg)
![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)
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

## ⚠️ Database Notice

The MySQL database required for HotelHQ is **not included** in this repository.  
Because the database schema and data are **proprietary**, they are not publicly provided at this time.  
As a result, the application **cannot be run locally** without the required database setup.

The database files will be **provided soon**, or updates will be made to support a public development setup.

In the meantime, you can view the **Live Demo** linked above.

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

## 📜 License

This project uses a dual-license model:

### 🟦 GK-OSNC License 1.0 (Free, Non-Commercial)

You may:

- View, study, and learn from the source code  
- Run and modify the software locally  
- Submit contributions (PRs)

You may *not*:

- Use it commercially  
- Redistribute the software  
- Host it online  
- Publicly fork or mirror it  
- Include it in closed-source products  
- Share modified versions publicly  

This license protects the project while keeping it open to the community.

Read the full license in `LICENSE.md`.

---

### 🟧 Commercial License (Paid)

A commercial license is required if you want to:

- Use the software in a business environment  
- Host or deploy it publicly (SaaS, API, website)  
- Integrate it into closed-source products  
- Redistribute the software in any form  
- Keep modifications private  

To obtain a commercial license, contact:  
📧 **gauravkathayat945@gmail.com**

---

## FAQ

**Q: How do I reset the admin password?** A: Run `python change_admin_password.py` and follow the prompts.

**Q: How do I bulk update room images?** A: Use `python bulk_update_room_images.py` and provide the required image files.

---
For more technical details, see `DEFENSE_GUIDE.md`. For change history, see `CHANGELOG.md`.
