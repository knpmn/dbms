"""routes/user_routes.py - CRUD for USERS table (Admin only)."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import execute_query, execute_one, execute_query as dml
from auth import login_required, role_required, hash_password

user_bp = Blueprint('users', __name__)


@user_bp.route('/')
@login_required
@role_required('Admin')
def list_users():
    users = execute_query(
        """SELECT u.user_id, u.username, u.email, r.role_name
           FROM USERS u JOIN ROLES r ON u.role_id = r.role_id
           ORDER BY u.user_id"""
    )
    return render_template('users/list.html', users=users)


@user_bp.route('/new', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def create_user():
    roles = execute_query("SELECT role_id, role_name FROM ROLES ORDER BY role_id")
    employees = execute_query("SELECT employee_id, first_name || ' ' || last_name AS fullname FROM EMPLOYEES ORDER BY first_name")
    if request.method == 'POST':
        username    = request.form['username'].strip()
        password    = hash_password(request.form['password'])
        email       = request.form.get('email', '').strip()
        role_id     = int(request.form['role_id'])
        employee_id = request.form.get('employee_id')
        employee_id = int(employee_id) if employee_id else None

        dml(
            """INSERT INTO USERS (username, password, email, role_id, employee_id)
               VALUES (:username, :password, :email, :role_id, :employee_id)""",
            {'username': username, 'password': password, 'email': email, 'role_id': role_id, 'employee_id': employee_id},
            fetch=False
        )
        flash('User created successfully.', 'success')
        return redirect(url_for('users.list_users'))
    return render_template('users/form.html', user=None, roles=roles, employees=employees)


@user_bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def edit_user(user_id):
    roles = execute_query("SELECT role_id, role_name FROM ROLES ORDER BY role_id")
    employees = execute_query("SELECT employee_id, first_name || ' ' || last_name AS fullname FROM EMPLOYEES ORDER BY first_name")
    user  = execute_one("SELECT * FROM USERS WHERE user_id = :id", {'id': user_id})
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('users.list_users'))

    if request.method == 'POST':
        username = request.form['username'].strip()
        email       = request.form.get('email', '').strip()
        role_id     = int(request.form['role_id'])
        employee_id = request.form.get('employee_id')
        employee_id = int(employee_id) if employee_id else None
        new_pw      = request.form.get('password', '').strip()
        
        if new_pw:
            dml(
                """UPDATE USERS SET username=:u, email=:e, role_id=:r, employee_id=:emp, password=:p
                   WHERE user_id=:id""",
                {'u': username, 'e': email, 'r': role_id, 'emp': employee_id, 'p': hash_password(new_pw), 'id': user_id},
                fetch=False
            )
        else:
            dml(
                "UPDATE USERS SET username=:u, email=:e, role_id=:r, employee_id=:emp WHERE user_id=:id",
                {'u': username, 'e': email, 'r': role_id, 'emp': employee_id, 'id': user_id},
                fetch=False
            )
        flash('User updated.', 'success')
        return redirect(url_for('users.list_users'))
    return render_template('users/form.html', user=user, roles=roles, employees=employees)


@user_bp.route('/<int:user_id>/delete', methods=['POST'])
@login_required
@role_required('Admin')
def delete_user(user_id):
    dml("DELETE FROM USERS WHERE user_id = :id", {'id': user_id}, fetch=False)
    flash('User deleted.', 'success')
    return redirect(url_for('users.list_users'))
