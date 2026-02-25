"""routes/bp_routes.py - CRUD for BP (Bonus & Penalty log).
HR Staff & Admin: full CRUD. Employee: view own records."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import execute_query, execute_one, execute_query as dml
from auth import login_required, role_required

bp_log_bp = Blueprint('bp', __name__)


def _get_employees():
    return execute_query("SELECT employee_id, first_name || ' ' || last_name AS fullname FROM EMPLOYEES ORDER BY first_name")


@bp_log_bp.route('/')
@login_required
def list_bp():
    role = session.get('role')
    if role in ('Admin', 'HR Staff'):
        records = execute_query(
            """SELECT b.bp_id, b.type_col, b.reference_id,
                      TO_CHAR(b.created_date,'YYYY-MM-DD') AS created_date,
                      e.first_name || ' ' || e.last_name AS emp_name, b.employee_id
               FROM BP b JOIN EMPLOYEES e ON b.employee_id = e.employee_id
               ORDER BY b.created_date DESC"""
        )
    else:
        records = execute_query(
            """SELECT b.bp_id, b.type_col, b.reference_id,
                      TO_CHAR(b.created_date,'YYYY-MM-DD') AS created_date, 
                      e.first_name || ' ' || e.last_name AS emp_name, b.employee_id
               FROM BP b JOIN EMPLOYEES e ON b.employee_id = e.employee_id
               WHERE b.employee_id IN (SELECT employee_id FROM EMPLOYEES WHERE ROWNUM=1)
               ORDER BY b.created_date DESC"""
        )
    return render_template('bp/list.html', records=records, role=role)


@bp_log_bp.route('/new', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'HR Staff')
def create_bp():
    employees = _get_employees()
    if request.method == 'POST':
        dml(
            """INSERT INTO BP (type_col, reference_id, created_date, employee_id)
               VALUES (:t, :ref, TO_DATE(:cd,'YYYY-MM-DD'), :eid)""",
            {'t': request.form['type_col'], 'ref': int(request.form['reference_id']),
             'cd': request.form['created_date'], 'eid': int(request.form['employee_id'])},
            fetch=False
        )
        flash('BP log entry added.', 'success')
        return redirect(url_for('bp.list_bp'))
    return render_template('bp/form.html', record=None, employees=employees)


@bp_log_bp.route('/<int:bp_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'HR Staff')
def edit_bp(bp_id):
    record    = execute_one("SELECT * FROM BP WHERE bp_id = :id", {'id': bp_id})
    employees = _get_employees()
    if not record:
        flash('Record not found.', 'danger')
        return redirect(url_for('bp.list_bp'))
    if request.method == 'POST':
        dml(
            """UPDATE BP SET type_col=:t, reference_id=:ref,
               created_date=TO_DATE(:cd,'YYYY-MM-DD'), employee_id=:eid WHERE bp_id=:id""",
            {'t': request.form['type_col'], 'ref': int(request.form['reference_id']),
             'cd': request.form['created_date'], 'eid': int(request.form['employee_id']), 'id': bp_id},
            fetch=False
        )
        flash('BP log entry updated.', 'success')
        return redirect(url_for('bp.list_bp'))
    return render_template('bp/form.html', record=record, employees=employees)


@bp_log_bp.route('/<int:bp_id>/delete', methods=['POST'])
@login_required
@role_required('Admin', 'HR Staff')
def delete_bp(bp_id):
    dml("DELETE FROM BP WHERE bp_id = :id", {'id': bp_id}, fetch=False)
    flash('BP log entry deleted.', 'success')
    return redirect(url_for('bp.list_bp'))
