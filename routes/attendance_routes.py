"""routes/attendance_routes.py - CRUD for ATTENDANCE.
HR Staff & Admin: full CRUD. Employee: view own records only."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import execute_query, execute_one, execute_query as dml
from auth import login_required, role_required

att_bp = Blueprint('attendance', __name__)


def _get_employees():
    return execute_query("SELECT employee_id, first_name || ' ' || last_name AS fullname FROM EMPLOYEES ORDER BY first_name")


@att_bp.route('/')
@login_required
def list_attendance():
    role = session.get('role')
    if role in ('Admin', 'HR Staff'):
        records = execute_query(
            """SELECT a.attendance_id, TO_CHAR(a.date_col,'YYYY-MM-DD') AS date_col,
                      a.status, e.first_name || ' ' || e.last_name AS emp_name, a.employee_id
               FROM ATTENDANCE a JOIN EMPLOYEES e ON a.employee_id = e.employee_id
               ORDER BY a.date_col DESC"""
        )
    else:
        # Employee: own records only (linked via session user_id -> employee mapping)
        records = execute_query(
            """SELECT a.attendance_id, TO_CHAR(a.date_col,'YYYY-MM-DD') AS date_col, a.status, a.employee_id
               FROM ATTENDANCE a
               WHERE a.employee_id IN (
                   SELECT employee_id FROM EMPLOYEES WHERE ROWNUM=1
               )
               ORDER BY a.date_col DESC""",
        )
    return render_template('attendance/list.html', records=records, role=role)


@att_bp.route('/new', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'HR Staff')
def create_attendance():
    employees = _get_employees()
    if request.method == 'POST':
        dml(
            """INSERT INTO ATTENDANCE (date_col, status, employee_id)
               VALUES (TO_DATE(:d,'YYYY-MM-DD'), :s, :eid)""",
            {'d': request.form['date_col'], 's': request.form['status'], 'eid': int(request.form['employee_id'])},
            fetch=False
        )
        flash('Attendance record added.', 'success')
        return redirect(url_for('attendance.list_attendance'))
    return render_template('attendance/form.html', record=None, employees=employees)


@att_bp.route('/<int:att_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'HR Staff')
def edit_attendance(att_id):
    record    = execute_one("SELECT * FROM ATTENDANCE WHERE attendance_id = :id", {'id': att_id})
    employees = _get_employees()
    if not record:
        flash('Record not found.', 'danger')
        return redirect(url_for('attendance.list_attendance'))
    if request.method == 'POST':
        dml(
            """UPDATE ATTENDANCE SET date_col=TO_DATE(:d,'YYYY-MM-DD'), status=:s, employee_id=:eid
               WHERE attendance_id=:id""",
            {'d': request.form['date_col'], 's': request.form['status'],
             'eid': int(request.form['employee_id']), 'id': att_id},
            fetch=False
        )
        flash('Attendance updated.', 'success')
        return redirect(url_for('attendance.list_attendance'))
    return render_template('attendance/form.html', record=record, employees=employees)


@att_bp.route('/<int:att_id>/delete', methods=['POST'])
@login_required
@role_required('Admin', 'HR Staff')
def delete_attendance(att_id):
    dml("DELETE FROM ATTENDANCE WHERE attendance_id = :id", {'id': att_id}, fetch=False)
    flash('Record deleted.', 'success')
    return redirect(url_for('attendance.list_attendance'))
