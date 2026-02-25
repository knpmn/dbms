"""routes/employee_routes.py - CRUD for EMPLOYEES (Admin + HR Staff). Employees view own record."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import execute_query, execute_one, execute_query as dml
from auth import login_required, role_required

employee_bp = Blueprint('employees', __name__)


@employee_bp.route('/')
@login_required
@role_required('Admin', 'HR Staff')
def list_employees():
    employees = execute_query(
        """SELECT e.employee_id, e.first_name, e.last_name, e.salary,
                  TO_CHAR(e.start_date,'YYYY-MM-DD') AS start_date,
                  d.department_name, p.position_name
           FROM EMPLOYEES e
           JOIN DEPARTMENTS d ON e.department_id = d.department_id
           JOIN POSITIONS   p ON e.position_id   = p.position_id
           ORDER BY e.employee_id"""
    )
    return render_template('employees/list.html', employees=employees)


@employee_bp.route('/profile')
@login_required
def my_profile():
    """Employee views own profile by matching email to username convention."""
    emp = execute_one(
        """SELECT e.employee_id, e.first_name, e.last_name, e.salary,
                  TO_CHAR(e.start_date,'YYYY-MM-DD') AS start_date,
                  d.department_name, p.position_name
           FROM EMPLOYEES e
           JOIN DEPARTMENTS d ON e.department_id = d.department_id
           JOIN POSITIONS   p ON e.position_id   = p.position_id
           JOIN USERS u ON u.email = (
               SELECT email FROM USERS WHERE user_id = :uid
           )
           WHERE e.employee_id = (
               SELECT MIN(e2.employee_id) FROM EMPLOYEES e2
           )""",
        {'uid': session['user_id']}
    )
    return render_template('employees/detail.html', emp=emp)


@employee_bp.route('/new', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'HR Staff')
def create_employee():
    depts = execute_query("SELECT department_id, department_name FROM DEPARTMENTS ORDER BY department_name")
    positions = execute_query("SELECT position_id, position_name FROM POSITIONS ORDER BY position_name")
    if request.method == 'POST':
        dml(
            """INSERT INTO EMPLOYEES (first_name, last_name, salary, start_date, department_id, position_id)
               VALUES (:fn, :ln, :sal, TO_DATE(:sd,'YYYY-MM-DD'), :did, :pid)""",
            {
                'fn':  request.form['first_name'].strip(),
                'ln':  request.form['last_name'].strip(),
                'sal': float(request.form['salary']),
                'sd':  request.form['start_date'],
                'did': int(request.form['department_id']),
                'pid': int(request.form['position_id']),
            },
            fetch=False
        )
        flash('Employee created.', 'success')
        return redirect(url_for('employees.list_employees'))
    return render_template('employees/form.html', emp=None, depts=depts, positions=positions)


@employee_bp.route('/<int:employee_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'HR Staff')
def edit_employee(employee_id):
    emp  = execute_one("SELECT * FROM EMPLOYEES WHERE employee_id = :id", {'id': employee_id})
    depts = execute_query("SELECT department_id, department_name FROM DEPARTMENTS ORDER BY department_name")
    positions = execute_query("SELECT position_id, position_name FROM POSITIONS ORDER BY position_name")
    if not emp:
        flash('Employee not found.', 'danger')
        return redirect(url_for('employees.list_employees'))
    if request.method == 'POST':
        dml(
            """UPDATE EMPLOYEES SET first_name=:fn, last_name=:ln, salary=:sal,
               start_date=TO_DATE(:sd,'YYYY-MM-DD'), department_id=:did, position_id=:pid
               WHERE employee_id=:id""",
            {
                'fn':  request.form['first_name'].strip(),
                'ln':  request.form['last_name'].strip(),
                'sal': float(request.form['salary']),
                'sd':  request.form['start_date'],
                'did': int(request.form['department_id']),
                'pid': int(request.form['position_id']),
                'id':  employee_id,
            },
            fetch=False
        )
        flash('Employee updated.', 'success')
        return redirect(url_for('employees.list_employees'))
    return render_template('employees/form.html', emp=emp, depts=depts, positions=positions)


@employee_bp.route('/<int:employee_id>/delete', methods=['POST'])
@login_required
@role_required('Admin', 'HR Staff')
def delete_employee(employee_id):
    dml("DELETE FROM EMPLOYEES WHERE employee_id = :id", {'id': employee_id}, fetch=False)
    flash('Employee deleted.', 'success')
    return redirect(url_for('employees.list_employees'))
