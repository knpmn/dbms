"""routes/role_routes.py - CRUD for ROLES table (Admin only)."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import execute_query, execute_one, execute_query as dml
from auth import login_required, role_required

role_bp = Blueprint('roles', __name__)


@role_bp.route('/')
@login_required
@role_required('Admin')
def list_roles():
    roles = execute_query("SELECT * FROM ROLES ORDER BY role_id")
    return render_template('roles/list.html', roles=roles)


@role_bp.route('/new', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def create_role():
    if request.method == 'POST':
        role_name   = request.form['role_name'].strip()
        description = request.form.get('description', '').strip()
        dml(
            "INSERT INTO ROLES (role_name, description) VALUES (:n, :d)",
            {'n': role_name, 'd': description},
            fetch=False
        )
        flash('Role created.', 'success')
        return redirect(url_for('roles.list_roles'))
    return render_template('roles/form.html', role=None)


@role_bp.route('/<int:role_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def edit_role(role_id):
    role = execute_one("SELECT * FROM ROLES WHERE role_id = :id", {'id': role_id})
    if not role:
        flash('Role not found.', 'danger')
        return redirect(url_for('roles.list_roles'))
    if request.method == 'POST':
        dml(
            "UPDATE ROLES SET role_name=:n, description=:d WHERE role_id=:id",
            {'n': request.form['role_name'].strip(), 'd': request.form.get('description','').strip(), 'id': role_id},
            fetch=False
        )
        flash('Role updated.', 'success')
        return redirect(url_for('roles.list_roles'))
    return render_template('roles/form.html', role=role)


@role_bp.route('/<int:role_id>/delete', methods=['POST'])
@login_required
@role_required('Admin')
def delete_role(role_id):
    dml("DELETE FROM ROLES WHERE role_id = :id", {'id': role_id}, fetch=False)
    flash('Role deleted.', 'success')
    return redirect(url_for('roles.list_roles'))
