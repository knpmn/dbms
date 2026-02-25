# Smart HR System

A web-based Human Resource Management System built with **Flask** and **Oracle Database**, featuring role-based access control for Admin, HR Staff, and Employee roles.

## Features

- **Role-Based Access Control** — Three roles: Admin, HR Staff, Employee
- **Employee Management** — Full CRUD for employee records
- **Department & Position Management** — Organize your org structure
- **Attendance Tracking** — Log and view attendance records
- **Bonus Points** — Award and track employee bonus points
- **Yearly Bonus** — Calculate and record annual bonuses
- **Penalties** — Record and manage employee penalties
- **B&P Log** — Combined Bonus & Penalty audit trail
- **User Management** — Admin can manage system users and roles
- **Responsive UI** — Bootstrap 5 + Material Icons

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3 / Flask |
| Database | Oracle DB (via `oracledb`) |
| Frontend | Bootstrap 5, Material Icons, DataTables.js, Chart.js |
| Auth | Flask session-based authentication |

## Prerequisites

- Python 3.10+
- Oracle Database (XE or full)
- Oracle Instant Client (for `oracledb` thick mode, if needed)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/knpmn/dbms.git
cd dbms
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the database

Copy the example config and fill in your Oracle credentials:

```bash
cp config.example.py config.py
```

Edit `config.py`:

```python
DB_HOST     = "localhost"
DB_PORT     = 1521
DB_SERVICE  = "xe"
DB_USER     = "your_username"
DB_PASSWORD = "your_password"
SECRET_KEY  = "your_random_secret_key"
```

### 4. Initialize the database schema

```bash
python setup_db.py
```

### 5. Run the application

```bash
python app.py
```

The app will be available at `http://127.0.0.1:5000`.

## Default Login

After running `setup_db.py`, a default admin account is created:

| Username | Password |
|---|---|
| `admin` | `admin123` |

> ⚠️ Change the default password after your first login.

## Project Structure

```
dbms/
├── app.py                  # Flask app entry point
├── auth.py                 # Login/logout logic
├── db.py                   # Oracle DB connection pool
├── config.py               # DB credentials (not committed)
├── config.example.py       # Config template
├── setup_db.py             # DB schema + seed data
├── schema.sql              # SQL schema
├── requirements.txt        # Python dependencies
├── routes/                 # Blueprint route handlers
│   ├── auth_routes.py
│   ├── employee_routes.py
│   ├── department_routes.py
│   ├── position_routes.py
│   ├── attendance_routes.py
│   ├── bonus_point_routes.py
│   ├── yearly_bonus_routes.py
│   ├── penalty_routes.py
│   ├── bp_routes.py
│   ├── user_routes.py
│   └── role_routes.py
└── templates/              # Jinja2 HTML templates
    ├── base.html
    ├── login.html
    ├── dashboard_admin.html
    ├── dashboard_hr.html
    ├── dashboard_employee.html
    └── [module]/
        ├── list.html
        └── form.html
```

## Team

Developed as a final project for the Database Management Systems course.
