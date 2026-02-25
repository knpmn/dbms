"""routes/position_routes.py - CRUD for POSITIONS (Admin + HR Staff)."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import execute_query, execute_one, execute_query as dml
from auth import login_required, role_required

pos_bp = Blueprint('positions', __name__)


@pos_bp.route('/')
@login_required
@role_required('Admin', 'HR Staff')
def list_positions():
    positions = execute_query("SELECT * FROM POSITIONS ORDER BY position_id")
    return render_template('positions/list.html', positions=positions)


@pos_bp.route('/new', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'HR Staff')
def create_position():
    if request.method == 'POST':
        dml(
            "INSERT INTO POSITIONS (position_name, base_salary) VALUES (:n, :s)",
            {'n': request.form['position_name'].strip(), 's': float(request.form['base_salary'])},
            fetch=False
        )
        flash('Position created.', 'success')
        return redirect(url_for('positions.list_positions'))
    return render_template('positions/form.html', pos=None)


@pos_bp.route('/<int:position_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'HR Staff')
def edit_position(position_id):
    pos = execute_one("SELECT * FROM POSITIONS WHERE position_id = :id", {'id': position_id})
    if not pos:
        flash('Position not found.', 'danger')
        return redirect(url_for('positions.list_positions'))
    if request.method == 'POST':
        dml(
            "UPDATE POSITIONS SET position_name=:n, base_salary=:s WHERE position_id=:id",
            {'n': request.form['position_name'].strip(), 's': float(request.form['base_salary']), 'id': position_id},
            fetch=False
        )
        flash('Position updated.', 'success')
        return redirect(url_for('positions.list_positions'))
    return render_template('positions/form.html', pos=pos)


@pos_bp.route('/<int:position_id>/delete', methods=['POST'])
@login_required
@role_required('Admin', 'HR Staff')
def delete_position(position_id):
    dml("DELETE FROM POSITIONS WHERE position_id = :id", {'id': position_id}, fetch=False)
    flash('Position deleted.', 'success')
    return redirect(url_for('positions.list_positions'))
