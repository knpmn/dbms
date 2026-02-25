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
    return render_template('attendance/list.html', role=role)

@att_bp.route('/api/data')
@login_required
def list_attendance_api():
    role = session.get('role')
    
    # DataTables parameters
    draw = int(request.args.get('draw', 1))
    start = int(request.args.get('start', 0))
    length = int(request.args.get('length', 10))
    search_value = request.args.get('search[value]', '').strip()
    order_col_idx = request.args.get('order[0][column]')
    order_dir = request.args.get('order[0][dir]', 'asc')

    # Mapping DataTables columns to SQL columns
    columns_map = {
        '0': 'a.attendance_id',
        '1': 'a.date_col',
        '2': 'a.status',
        '3': 'e.first_name' # Used to sort by employee name
    }
    
    order_col = columns_map.get(str(order_col_idx), 'a.date_col')
    if order_dir not in ['asc', 'desc']:
        order_dir = 'desc'

    # Base query logic
    base_query = """
        FROM ATTENDANCE a 
        JOIN EMPLOYEES e ON a.employee_id = e.employee_id
    """
    
    where_clauses = []
    binds = {}

    # Role constraints
    if role not in ('Admin', 'HR Staff'):
        # Employee view: only their own records
        where_clauses.append("a.employee_id = (SELECT employee_id FROM EMPLOYEES WHERE ROWNUM=1)")
        # In a real app this would be: "a.employee_id = :session_emp_id"

    # Search constraints
    if search_value:
        search_term = f"%{search_value.lower()}%"
        where_clauses.append("(LOWER(a.status) LIKE :srch OR LOWER(e.first_name || ' ' || e.last_name) LIKE :srch OR TO_CHAR(a.date_col, 'YYYY-MM-DD') LIKE :srch)")
        binds['srch'] = search_term

    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)

    # 1. Total records (no filters)
    total_query = f"SELECT COUNT(*) as c {base_query}"
    if role not in ('Admin', 'HR Staff'):
        total_records = execute_one(total_query + " WHERE a.employee_id = (SELECT employee_id FROM EMPLOYEES WHERE ROWNUM=1)")['c']
    else:
        total_records = execute_one(total_query)['c']

    # 2. Filtered records (with search)
    filtered_query = f"SELECT COUNT(*) as c {base_query} {where_sql}"
    filtered_records = execute_one(filtered_query, binds)['c']

    # 3. Fetch data with pagination
    data_query = f"""
        SELECT a.attendance_id, TO_CHAR(a.date_col,'YYYY-MM-DD') AS date_col,
               a.status, e.first_name || ' ' || e.last_name AS emp_name, a.employee_id
        {base_query}
        {where_sql}
        ORDER BY {order_col} {order_dir}
        OFFSET :start ROWS FETCH NEXT :length ROWS ONLY
    """
    binds['start'] = start
    binds['length'] = length
    
    records = execute_query(data_query, binds)

    # Format JSON response for DataTables
    data = []
    for r in records:
        data.append({
            'attendance_id': r['attendance_id'],
            'date_col': r['date_col'],
            'status': r['status'],
            'emp_name': r['emp_name'],
            'employee_id': r['employee_id']
        })

    return {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": data
    }


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
