"""routes/auth_routes.py - Login, logout, and dashboard routing."""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import execute_one, execute_query
from auth import verify_password

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('auth.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = execute_one(
            """SELECT u.user_id, u.username, u.password, u.email, r.role_name
               FROM USERS u JOIN ROLES r ON u.role_id = r.role_id
               WHERE u.username = :username""",
            {'username': username}
        )

        if user and verify_password(password, user['password']):
            session['user_id']  = user['user_id']
            session['username'] = user['username']
            session['email']    = user['email']
            session['role']     = user['role_name']
            flash(f"Welcome, {user['username']}!", 'success')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    role = session.get('role')
    
    if role == 'Admin':
        stats = {
            'users': execute_one("SELECT COUNT(*) AS c FROM USERS")['c'],
            'roles': execute_one("SELECT COUNT(*) AS c FROM ROLES")['c'],
            'employees': execute_one("SELECT COUNT(*) AS c FROM EMPLOYEES")['c'],
            'departments': execute_one("SELECT COUNT(*) AS c FROM DEPARTMENTS")['c']
        }
        dept_data = execute_query("""
            SELECT d.department_name, (SELECT COUNT(*) FROM EMPLOYEES e WHERE e.department_id = d.department_id) as emp_count
            FROM DEPARTMENTS d
        """)
        return render_template('dashboard_admin.html', stats=stats, dept_data=dept_data)
        
    elif role == 'HR Staff':
        stats = {
            'employees': execute_one("SELECT COUNT(*) AS c FROM EMPLOYEES")['c'],
            'departments': execute_one("SELECT COUNT(*) AS c FROM DEPARTMENTS")['c'],
            'positions': execute_one("SELECT COUNT(*) AS c FROM POSITIONS")['c'],
            'penalties': execute_one("SELECT COUNT(*) AS c FROM PENALTIES")['c']
        }
        dept_data = execute_query("""
            SELECT d.department_name, (SELECT COUNT(*) FROM EMPLOYEES e WHERE e.department_id = d.department_id) as emp_count
            FROM DEPARTMENTS d
        """)
        return render_template('dashboard_hr.html', stats=stats, dept_data=dept_data)
        
    else:
        # Dummy matching logic for employee dashboard based on previous profile logic
        emp_id_res = execute_one("SELECT MIN(employee_id) as min_id FROM EMPLOYEES")
        emp_id = emp_id_res['min_id'] if emp_id_res else 0
        
        stats = {
            'attendance': execute_one("SELECT COUNT(*) AS c FROM ATTENDANCE WHERE employee_id = :e", {'e': emp_id})['c'] if emp_id else 0,
            'bonus': execute_one("SELECT COUNT(*) AS c FROM BONUS_POINTS WHERE employee_id = :e", {'e': emp_id})['c'] if emp_id else 0,
            'penalties': execute_one("SELECT COUNT(*) AS c FROM PENALTIES WHERE employee_id = :e", {'e': emp_id})['c'] if emp_id else 0
        }
        return render_template('dashboard_employee.html', stats=stats)
