# Smart Parking Management System

## 1. Project Overview

Smart Parking Management System is a desktop application developed to manage parking operations efficiently. It helps administrators and staff manage vehicles, parking spaces, parking sessions, and payments through a graphical user interface.

## 2. Main Features

- User login and authentication.
- Vehicle registration and management.
- Parking space management.
- Vehicle entry and exit registration.
- Automatic parking fee calculation.
- Payment registration and tracking.
- Revenue reports.
- Dashboard displaying parking statistics.

## 3. Technologies Used

- **Programming Language:** Python
- **Database:** MySQL
- **GUI Framework:** PySide6
- **Database Connector:** MySQL Connector/Python
- **Environment Variables:** python-dotenv

## 4. Project Structure

```text
Smart_Parking/
│
├── ui/
│   ├── __init__.py
│   ├── login.py
│   └── dashboard.py
│
├── tests/
│   ├── __init__.py
│   └── Test files
│
├── db.py
├── users.py
├── vehicles.py
├── parking_spaces.py
├── parking_sessions.py
├── payments.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

**Note:** The `.env` file must be created locally to configure the database connection. It is not included in the repository.

## 5. Installation

1. Clone the repository.
2. Create a virtual environment.
3. Activate the virtual environment.
4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

5. Configure the database connection variables in the `.env` file.
6. Create the MySQL database and required tables.

## 6. Running the Application

Run the following command from the project directory:

```bash
python -m ui.login
```

## 7. Database

The application uses MySQL to store and manage:

- Users
- Vehicles
- Parking Spaces
- Parking Sessions
- Payments

## 8. Security

- Database credentials are stored in environment variables.
- The `.env` file is excluded from Git tracking.
- User passwords are stored as hashed values.

## 9. Project Purpose

This project was developed as an academic project in Software Engineering to apply programming, database design, and software development concepts in a practical system.