"""routes/department_routes.py - CRUD for DEPARTMENTS (Admin + HR Staff)."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import execute_query, execute_one, execute_query as dml
from auth import login_required, role_required

dept_bp = Blueprint('departments', __name__)


@dept_bp.route('/')
@login_required
@role_required('Admin', 'HR Staff')
def list_departments():
    depts = execute_query("SELECT * FROM DEPARTMENTS ORDER BY department_id")
    return render_template('departments/list.html', depts=depts)


@dept_bp.route('/new', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'HR Staff')
def create_department():
    if request.method == 'POST':
        dml(
            "INSERT INTO DEPARTMENTS (department_name, description) VALUES (:n, :d)",
            {'n': request.form['department_name'].strip(), 'd': request.form.get('description','').strip()},
            fetch=False
        )
        flash('Department created.', 'success')
        return redirect(url_for('departments.list_departments'))
    return render_template('departments/form.html', dept=None)


@dept_bp.route('/<int:department_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'HR Staff')
def edit_department(department_id):
    dept = execute_one("SELECT * FROM DEPARTMENTS WHERE department_id = :id", {'id': department_id})
    if not dept:
        flash('Department not found.', 'danger')
        return redirect(url_for('departments.list_departments'))
    if request.method == 'POST':
        dml(
            "UPDATE DEPARTMENTS SET department_name=:n, description=:d WHERE department_id=:id",
            {'n': request.form['department_name'].strip(), 'd': request.form.get('description','').strip(), 'id': department_id},
            fetch=False
        )
        flash('Department updated.', 'success')
        return redirect(url_for('departments.list_departments'))
    return render_template('departments/form.html', dept=dept)


@dept_bp.route('/<int:department_id>/delete', methods=['POST'])
@login_required
@role_required('Admin', 'HR Staff')
def delete_department(department_id):
    dml("DELETE FROM DEPARTMENTS WHERE department_id = :id", {'id': department_id}, fetch=False)
    flash('Department deleted.', 'success')
    return redirect(url_for('departments.list_departments'))
