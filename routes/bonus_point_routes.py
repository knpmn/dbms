"""routes/bonus_point_routes.py - CRUD for BONUS_POINTS.
HR Staff & Admin: full CRUD. Employee: view own records."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import execute_query, execute_one, execute_query as dml
from auth import login_required, role_required

bonus_bp = Blueprint('bonus_points', __name__)


def _get_employees():
    return execute_query("SELECT employee_id, first_name || ' ' || last_name AS fullname FROM EMPLOYEES ORDER BY first_name")


@bonus_bp.route('/')
@login_required
def list_bonus_points():
    role = session.get('role')
    if role in ('Admin', 'HR Staff'):
        records = execute_query(
            """SELECT bp.bonus_point_id, bp.month_col, bp.year_col, bp.points,
                      e.first_name || ' ' || e.last_name AS emp_name, bp.employee_id
               FROM BONUS_POINTS bp JOIN EMPLOYEES e ON bp.employee_id = e.employee_id
               ORDER BY bp.year_col DESC, bp.month_col DESC"""
        )
    else:
        records = execute_query(
            """SELECT bp.bonus_point_id, bp.month_col, bp.year_col, bp.points, bp.employee_id
               FROM BONUS_POINTS bp
               WHERE bp.employee_id IN (SELECT employee_id FROM EMPLOYEES WHERE ROWNUM=1)
               ORDER BY bp.year_col DESC, bp.month_col DESC"""
        )
    return render_template('bonus_points/list.html', records=records, role=role)


@bonus_bp.route('/new', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'HR Staff')
def create_bonus_point():
    employees = _get_employees()
    if request.method == 'POST':
        dml(
            "INSERT INTO BONUS_POINTS (month_col, year_col, points, employee_id) VALUES (:m, :y, :p, :eid)",
            {'m': int(request.form['month_col']), 'y': int(request.form['year_col']),
             'p': int(request.form['points']), 'eid': int(request.form['employee_id'])},
            fetch=False
        )
        flash('Bonus point added.', 'success')
        return redirect(url_for('bonus_points.list_bonus_points'))
    return render_template('bonus_points/form.html', record=None, employees=employees)


@bonus_bp.route('/<int:bp_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'HR Staff')
def edit_bonus_point(bp_id):
    record    = execute_one("SELECT * FROM BONUS_POINTS WHERE bonus_point_id = :id", {'id': bp_id})
    employees = _get_employees()
    if not record:
        flash('Record not found.', 'danger')
        return redirect(url_for('bonus_points.list_bonus_points'))
    if request.method == 'POST':
        dml(
            "UPDATE BONUS_POINTS SET month_col=:m, year_col=:y, points=:p, employee_id=:eid WHERE bonus_point_id=:id",
            {'m': int(request.form['month_col']), 'y': int(request.form['year_col']),
             'p': int(request.form['points']), 'eid': int(request.form['employee_id']), 'id': bp_id},
            fetch=False
        )
        flash('Bonus point updated.', 'success')
        return redirect(url_for('bonus_points.list_bonus_points'))
    return render_template('bonus_points/form.html', record=record, employees=employees)


@bonus_bp.route('/<int:bp_id>/delete', methods=['POST'])
@login_required
@role_required('Admin', 'HR Staff')
def delete_bonus_point(bp_id):
    dml("DELETE FROM BONUS_POINTS WHERE bonus_point_id = :id", {'id': bp_id}, fetch=False)
    flash('Record deleted.', 'success')
    return redirect(url_for('bonus_points.list_bonus_points'))
