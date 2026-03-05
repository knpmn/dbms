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


@auth_bp.route('/employee-lookup', methods=['POST'])
def employee_lookup():
    """Look up an employee by first and last name (no password required)."""
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()

    if not first_name or not last_name:
        flash('Please enter both first and last name.', 'danger')
        return redirect(url_for('auth.login', tab='employee'))

    matches = execute_query(
        """SELECT e.employee_id, e.first_name, e.last_name,
                  d.department_name, p.position_name
           FROM EMPLOYEES e
           JOIN DEPARTMENTS d ON e.department_id = d.department_id
           JOIN POSITIONS   p ON e.position_id   = p.position_id
           WHERE UPPER(e.first_name) = UPPER(:fn)
             AND UPPER(e.last_name)  = UPPER(:ln)""",
        {'fn': first_name, 'ln': last_name}
    )

    if not matches:
        flash(f'No employee found with name "{first_name} {last_name}".', 'danger')
        return redirect(url_for('auth.login', tab='employee'))

    if len(matches) == 1:
        emp = matches[0]
        session['emp_id'] = emp['employee_id']
        session['emp_name'] = f"{emp['first_name']} {emp['last_name']}"
        session['role'] = 'Employee'
        return redirect(url_for('auth.employee_dashboard'))

    # Multiple matches — pick the first one (simplest approach)
    emp = matches[0]
    session['emp_id'] = emp['employee_id']
    session['emp_name'] = f"{emp['first_name']} {emp['last_name']}"
    session['role'] = 'Employee'
    return redirect(url_for('auth.employee_dashboard'))


@auth_bp.route('/employee-dashboard')
def employee_dashboard():
    """Self-service dashboard for employees who logged in by name."""
    if 'emp_id' not in session:
        flash('Please look up your profile first.', 'warning')
        return redirect(url_for('auth.login', tab='employee'))

    emp_id = session['emp_id']

    emp = execute_one(
        """SELECT e.employee_id, e.first_name, e.last_name, e.salary,
                  TO_CHAR(e.start_date,'YYYY-MM-DD') AS start_date,
                  d.department_name, p.position_name
           FROM EMPLOYEES e
           JOIN DEPARTMENTS d ON e.department_id = d.department_id
           JOIN POSITIONS   p ON e.position_id   = p.position_id
           WHERE e.employee_id = :eid""",
        {'eid': emp_id}
    )

    if not emp:
        session.clear()
        flash('Employee record not found.', 'danger')
        return redirect(url_for('auth.login', tab='employee'))

    stats = {
        'attendance': execute_one("SELECT COUNT(*) AS c FROM ATTENDANCE WHERE employee_id = :e", {'e': emp_id})['c'],
        'bonus': execute_one("SELECT COUNT(*) AS c FROM BONUS_POINTS WHERE employee_id = :e", {'e': emp_id})['c'],
        'penalties': execute_one("SELECT COUNT(*) AS c FROM PENALTIES WHERE employee_id = :e", {'e': emp_id})['c']
    }

    recent_attendance = execute_query(
        """SELECT * FROM (
               SELECT TO_CHAR(date_col, 'YYYY-MM-DD') AS date_col, status
               FROM ATTENDANCE WHERE employee_id = :e
               ORDER BY date_col DESC
           ) WHERE ROWNUM <= 10""",
        {'e': emp_id}
    )

    return render_template('employee_self.html', emp=emp, stats=stats,
                           recent_attendance=recent_attendance)


@auth_bp.route('/employee-logout')
def employee_logout():
    """Clear employee self-service session."""
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
            'departments': execute_one("SELECT COUNT(*) AS c FROM DEPARTMENTS")['c'],
            'positions': execute_one("SELECT COUNT(*) AS c FROM POSITIONS")['c'],
            'attendance': execute_one("SELECT COUNT(*) AS c FROM ATTENDANCE")['c'],
            'bonus_points': execute_one("SELECT COUNT(*) AS c FROM BONUS_POINTS")['c'],
            'yearly_bonus': execute_one("SELECT COUNT(*) AS c FROM YEARLY_BONUS")['c'],
            'penalties': execute_one("SELECT COUNT(*) AS c FROM PENALTIES")['c'],
            'bp_log': execute_one("SELECT COUNT(*) AS c FROM BP")['c']
        }
        dept_data = execute_query("""
            SELECT d.department_name, (SELECT COUNT(*) FROM EMPLOYEES e WHERE e.department_id = d.department_id) as emp_count
            FROM DEPARTMENTS d
        """)
        recent_activity = execute_query("""
            SELECT * FROM (
                SELECT b.type_col, b.created_date, e.first_name, e.last_name 
                FROM BP b JOIN EMPLOYEES e ON b.employee_id = e.employee_id 
                ORDER BY b.created_date DESC
            ) WHERE ROWNUM <= 10
        """)
        top_performers = execute_query("""
            SELECT * FROM (
                SELECT e.first_name, e.last_name, y.yearly_bonus_score 
                FROM YEARLY_BONUS y JOIN EMPLOYEES e ON y.employee_id = e.employee_id 
                ORDER BY y.yearly_bonus_score DESC
            ) WHERE ROWNUM <= 5
        """)
        attendance_today = execute_query("""
            SELECT status, COUNT(*) as count FROM ATTENDANCE 
            WHERE TRUNC(date_col) = TRUNC(SYSDATE) GROUP BY status
        """)
        salary_data = execute_query("""
            SELECT d.department_name, NVL(SUM(e.salary), 0) as total_salary 
            FROM DEPARTMENTS d LEFT JOIN EMPLOYEES e ON d.department_id = e.department_id 
            GROUP BY d.department_name
        """)
        return render_template('dashboard_admin.html', stats=stats, dept_data=dept_data, 
                               recent_activity=recent_activity, top_performers=top_performers,
                               attendance_today=attendance_today, salary_data=salary_data)
        
    elif role == 'HR Staff':
        stats = {
            'users': execute_one("SELECT COUNT(*) AS c FROM USERS")['c'],
            'roles': execute_one("SELECT COUNT(*) AS c FROM ROLES")['c'],
            'employees': execute_one("SELECT COUNT(*) AS c FROM EMPLOYEES")['c'],
            'departments': execute_one("SELECT COUNT(*) AS c FROM DEPARTMENTS")['c'],
            'positions': execute_one("SELECT COUNT(*) AS c FROM POSITIONS")['c'],
            'attendance': execute_one("SELECT COUNT(*) AS c FROM ATTENDANCE")['c'],
            'bonus_points': execute_one("SELECT COUNT(*) AS c FROM BONUS_POINTS")['c'],
            'yearly_bonus': execute_one("SELECT COUNT(*) AS c FROM YEARLY_BONUS")['c'],
            'penalties': execute_one("SELECT COUNT(*) AS c FROM PENALTIES")['c'],
            'bp_log': execute_one("SELECT COUNT(*) AS c FROM BP")['c']
        }
        dept_data = execute_query("""
            SELECT d.department_name, (SELECT COUNT(*) FROM EMPLOYEES e WHERE e.department_id = d.department_id) as emp_count
            FROM DEPARTMENTS d
        """)
        recent_activity = execute_query("""
            SELECT * FROM (
                SELECT b.type_col, b.created_date, e.first_name, e.last_name 
                FROM BP b JOIN EMPLOYEES e ON b.employee_id = e.employee_id 
                ORDER BY b.created_date DESC
            ) WHERE ROWNUM <= 10
        """)
        top_performers = execute_query("""
            SELECT * FROM (
                SELECT e.first_name, e.last_name, y.yearly_bonus_score 
                FROM YEARLY_BONUS y JOIN EMPLOYEES e ON y.employee_id = e.employee_id 
                ORDER BY y.yearly_bonus_score DESC
            ) WHERE ROWNUM <= 5
        """)
        attendance_today = execute_query("""
            SELECT status, COUNT(*) as count FROM ATTENDANCE 
            WHERE TRUNC(date_col) = TRUNC(SYSDATE) GROUP BY status
        """)
        salary_data = execute_query("""
            SELECT d.department_name, NVL(SUM(e.salary), 0) as total_salary 
            FROM DEPARTMENTS d LEFT JOIN EMPLOYEES e ON d.department_id = e.department_id 
            GROUP BY d.department_name
        """)
        return render_template('dashboard_hr.html', stats=stats, dept_data=dept_data,
                               recent_activity=recent_activity, top_performers=top_performers,
                               attendance_today=attendance_today, salary_data=salary_data)
        
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
