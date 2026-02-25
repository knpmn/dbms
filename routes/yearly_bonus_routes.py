"""routes/yearly_bonus_routes.py - CRUD for YEARLY_BONUS.
HR Staff & Admin: full CRUD. Employee: view own records."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import execute_query, execute_one, execute_query as dml
from auth import login_required, role_required

yb_bp = Blueprint('yearly_bonus', __name__)


def _get_employees():
    return execute_query("SELECT employee_id, first_name || ' ' || last_name AS fullname FROM EMPLOYEES ORDER BY first_name")


@yb_bp.route('/')
@login_required
def list_yearly_bonus():
    role = session.get('role')
    if role in ('Admin', 'HR Staff'):
        records = execute_query(
            """SELECT yb.yearly_bonus_id, yb.year_col, yb.total_bonus_point,
                      yb.yearly_bonus_score, e.first_name || ' ' || e.last_name AS emp_name, yb.employee_id
               FROM YEARLY_BONUS yb JOIN EMPLOYEES e ON yb.employee_id = e.employee_id
               ORDER BY yb.year_col DESC"""
        )
    else:
        records = execute_query(
            """SELECT yb.yearly_bonus_id, yb.year_col, yb.total_bonus_point, yb.yearly_bonus_score, yb.employee_id
               FROM YEARLY_BONUS yb
               WHERE yb.employee_id IN (SELECT employee_id FROM EMPLOYEES WHERE ROWNUM=1)
               ORDER BY yb.year_col DESC"""
        )
    return render_template('yearly_bonus/list.html', records=records, role=role)


@yb_bp.route('/new', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'HR Staff')
def create_yearly_bonus():
    employees = _get_employees()
    if request.method == 'POST':
        dml(
            """INSERT INTO YEARLY_BONUS (year_col, total_bonus_point, yearly_bonus_score, employee_id)
               VALUES (:y, :tbp, :ybs, :eid)""",
            {'y': int(request.form['year_col']), 'tbp': float(request.form['total_bonus_point']),
             'ybs': float(request.form['yearly_bonus_score']), 'eid': int(request.form['employee_id'])},
            fetch=False
        )
        flash('Yearly bonus added.', 'success')
        return redirect(url_for('yearly_bonus.list_yearly_bonus'))
    return render_template('yearly_bonus/form.html', record=None, employees=employees)


@yb_bp.route('/<int:yb_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'HR Staff')
def edit_yearly_bonus(yb_id):
    record    = execute_one("SELECT * FROM YEARLY_BONUS WHERE yearly_bonus_id = :id", {'id': yb_id})
    employees = _get_employees()
    if not record:
        flash('Record not found.', 'danger')
        return redirect(url_for('yearly_bonus.list_yearly_bonus'))
    if request.method == 'POST':
        dml(
            """UPDATE YEARLY_BONUS SET year_col=:y, total_bonus_point=:tbp,
               yearly_bonus_score=:ybs, employee_id=:eid WHERE yearly_bonus_id=:id""",
            {'y': int(request.form['year_col']), 'tbp': float(request.form['total_bonus_point']),
             'ybs': float(request.form['yearly_bonus_score']), 'eid': int(request.form['employee_id']), 'id': yb_id},
            fetch=False
        )
        flash('Yearly bonus updated.', 'success')
        return redirect(url_for('yearly_bonus.list_yearly_bonus'))
    return render_template('yearly_bonus/form.html', record=record, employees=employees)


@yb_bp.route('/<int:yb_id>/delete', methods=['POST'])
@login_required
@role_required('Admin', 'HR Staff')
def delete_yearly_bonus(yb_id):
    dml("DELETE FROM YEARLY_BONUS WHERE yearly_bonus_id = :id", {'id': yb_id}, fetch=False)
    flash('Record deleted.', 'success')
    return redirect(url_for('yearly_bonus.list_yearly_bonus'))
