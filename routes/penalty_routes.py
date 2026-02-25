"""routes/penalty_routes.py - CRUD for PENALTIES.
HR Staff & Admin: full CRUD. Employee: view own records."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import execute_query, execute_one, execute_query as dml
from auth import login_required, role_required

penalty_bp = Blueprint('penalties', __name__)


def _get_employees():
    return execute_query("SELECT employee_id, first_name || ' ' || last_name AS fullname FROM EMPLOYEES ORDER BY first_name")


@penalty_bp.route('/')
@login_required
def list_penalties():
    role = session.get('role')
    if role in ('Admin', 'HR Staff'):
        records = execute_query(
            """SELECT p.penalty_id, p.penalty_level, p.description,
                      TO_CHAR(p.penalty_date,'YYYY-MM-DD') AS penalty_date,
                      e.first_name || ' ' || e.last_name AS emp_name, p.employee_id
               FROM PENALTIES p JOIN EMPLOYEES e ON p.employee_id = e.employee_id
               ORDER BY p.penalty_date DESC"""
        )
    else:
        records = execute_query(
            """SELECT p.penalty_id, p.penalty_level, p.description,
                      TO_CHAR(p.penalty_date,'YYYY-MM-DD') AS penalty_date, p.employee_id
               FROM PENALTIES p
               WHERE p.employee_id IN (SELECT employee_id FROM EMPLOYEES WHERE ROWNUM=1)
               ORDER BY p.penalty_date DESC"""
        )
    return render_template('penalties/list.html', records=records, role=role)


@penalty_bp.route('/new', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'HR Staff')
def create_penalty():
    employees = _get_employees()
    if request.method == 'POST':
        dml(
            """INSERT INTO PENALTIES (penalty_level, description, penalty_date, employee_id)
               VALUES (:lvl, :descr, TO_DATE(:pd,'YYYY-MM-DD'), :eid)""",
            {'lvl': request.form['penalty_level'], 'descr': request.form.get('description','').strip(),
             'pd': request.form['penalty_date'], 'eid': int(request.form['employee_id'])},
            fetch=False
        )
        flash('Penalty added.', 'success')
        return redirect(url_for('penalties.list_penalties'))
    return render_template('penalties/form.html', record=None, employees=employees)


@penalty_bp.route('/<int:pen_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'HR Staff')
def edit_penalty(pen_id):
    record    = execute_one("SELECT * FROM PENALTIES WHERE penalty_id = :id", {'id': pen_id})
    employees = _get_employees()
    if not record:
        flash('Record not found.', 'danger')
        return redirect(url_for('penalties.list_penalties'))
    if request.method == 'POST':
        dml(
            """UPDATE PENALTIES SET penalty_level=:lvl, description=:descr,
               penalty_date=TO_DATE(:pd,'YYYY-MM-DD'), employee_id=:eid WHERE penalty_id=:id""",
            {'lvl': request.form['penalty_level'], 'descr': request.form.get('description','').strip(),
             'pd': request.form['penalty_date'], 'eid': int(request.form['employee_id']), 'id': pen_id},
            fetch=False
        )
        flash('Penalty updated.', 'success')
        return redirect(url_for('penalties.list_penalties'))
    return render_template('penalties/form.html', record=record, employees=employees)


@penalty_bp.route('/<int:pen_id>/delete', methods=['POST'])
@login_required
@role_required('Admin', 'HR Staff')
def delete_penalty(pen_id):
    dml("DELETE FROM PENALTIES WHERE penalty_id = :id", {'id': pen_id}, fetch=False)
    flash('Penalty deleted.', 'success')
    return redirect(url_for('penalties.list_penalties'))
