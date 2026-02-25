import oracledb
import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
import db

def get_db_connection():
    try:
        if db._pool is None:
            db.init_pool()
        return db.get_connection()
    except Exception as e:
        print(f"Error connecting to DB: {e}")
        return None

def dml(query, binds={}, fetch=True):
    con = get_db_connection()
    if not con: return []
    cur = con.cursor()
    try:
        cur.execute(query, binds)
        if fetch:
            try:
                columns = [col[0].lower() for col in cur.description]
                cur.rowfactory = lambda *args: dict(zip(columns, args))
                res = cur.fetchall()
            except: res = []
        else:
            con.commit()
            res = True
        return res
    except Exception as e:
        con.rollback()
        raise e
    finally:
        cur.close()
        db.release_connection(con)

def execute_many(query, list_of_binds):
    con = get_db_connection()
    if not con: return
    cur = con.cursor()
    try:
        cur.executemany(query, list_of_binds)
        con.commit()
    except Exception as e:
        con.rollback()
        raise e
    finally:
        cur.close()
        db.release_connection(con)

print("1. Purging Database...")
tables_to_purge = ['BP', 'PENALTIES', 'YEARLY_BONUS', 'BONUS_POINTS', 'ATTENDANCE', 'USERS', 'EMPLOYEES', 'POSITIONS', 'DEPARTMENTS', 'ROLES']
for t in tables_to_purge:
    try:
        dml(f"DELETE FROM {t}", fetch=False)
        print(f" -> Cleared {t}")
    except Exception as e: pass

print("2. Generating Data...")

# ROLES
roles = [
    ('Admin', 'Full system access'), 
    ('HR Staff', 'Manages HR'), 
    ('Employee', 'View own profile'),
    ('Manager', 'Department Manager'),
    ('Supervisor', 'Team Supervisor'),
    ('Auditor', 'System and Financial Auditor'),
    ('Payroll Specialist', 'Handles Employee Payroll')
]
execute_many("INSERT INTO ROLES (role_name, description) VALUES (:1, :2)", roles)
roles_db = {r['role_name']: r['role_id'] for r in dml("SELECT role_id, role_name FROM ROLES")}

# ADMIN USER
admin_pw = generate_password_hash('admin123')
dml("INSERT INTO USERS (username, password, email, role_id) VALUES (:1, :2, :3, :4)", ('admin', admin_pw, 'admin@hrapp.com', roles_db['Admin']), fetch=False)

# DEPARTMENTS (15)
departments = ['HR', 'Engineering', 'Finance', 'Marketing', 'Sales', 'Support', 'IT', 'Legal', 'Product', 'R&D', 'QA', 'Design', 'Data Science', 'BizDev', 'Operations']
execute_many("INSERT INTO DEPARTMENTS (department_name, description) VALUES (:1, :2)", [(d, f'{d} Department') for d in departments])
dept_ids = [d['department_id'] for d in dml("SELECT department_id FROM DEPARTMENTS")]

# POSITIONS (20)
positions = [
    ('HR Manager', 8000000), ('Software Engineer', 12000000), ('Senior Engineer', 18000000), 
    ('Accountant', 7000000), ('Marketing Mgr', 10000000), ('Sales Exec', 5000000),
    ('Support Agent', 4500000), ('SysAdmin', 9500000), ('Legal Counsel', 15000000),
    ('Product Mgr', 14000000), ('QA Tester', 6500000), ('UX Designer', 9000000),
    ('Data Scientist', 16000000), ('Director', 30000000), ('VP', 40000000),
    ('Analyst', 6000000), ('Coordinator', 4000000), ('Manager', 12000000),
    ('Specialist', 5500000), ('Consultant', 11000000)
]
execute_many("INSERT INTO POSITIONS (position_name, base_salary) VALUES (:1, :2)", positions)
pos_db = dml("SELECT position_id, base_salary FROM POSITIONS")
pos_ids = [p['position_id'] for p in pos_db]
pos_dict = {p['position_id']: p['base_salary'] for p in pos_db}

# EMPLOYEES (500)
print(" -> Generating Employees...")
first_names = ['James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph', 'Thomas', 'Charles', 'Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan', 'Jessica', 'Sarah', 'Karen', 'Nancy', 'Lisa', 'Betty', 'Margaret', 'Sandra', 'Ashley', 'Kimberly', 'Emily', 'Donna', 'Michelle', 'Carol', 'Amanda', 'Melissa', 'Deborah', 'Stephanie', 'Rebecca', 'Sharon', 'Laura', 'Cynthia', 'Kathleen']
last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores']
emp_binds = []
now = datetime.now()
for i in range(500):
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    pid = random.choice(pos_ids)
    sal = pos_dict[pid] * random.uniform(0.9, 1.2)
    sd = now - timedelta(days=random.randint(30, 1800))
    emp_binds.append((fn, ln, sal, sd, random.choice(dept_ids), pid))

execute_many("INSERT INTO EMPLOYEES (first_name, last_name, salary, start_date, department_id, position_id) VALUES (:1, :2, :3, :4, :5, :6)", emp_binds)
emps_db_data = dml("SELECT employee_id, first_name, last_name FROM EMPLOYEES")
emp_ids = [e['employee_id'] for e in emps_db_data]

# USERS (For 50 employees)
print(" -> Generating Users...")
user_binds = []
pw = generate_password_hash('password123')
selected_emps = random.sample(emps_db_data, 100) # give 100 random users accounts
used_usernames = set(['admin'])

for e in selected_emps:
    eid = e['employee_id']
    base_username = f"{e['first_name'][0].lower()}.{e['last_name'].lower().replace(' ', '')}"
    username = base_username
    counter = 1
    while username in used_usernames:
        username = f"{base_username}{counter}"
        counter += 1
    used_usernames.add(username)
    user_binds.append((username, pw, f'{username}@hrapp.com', roles_db['Employee']))
    
execute_many("INSERT INTO USERS (username, password, email, role_id) VALUES (:1, :2, :3, :4)", user_binds)

# ATTENDANCE (30 days for 500 employees = ~15,000 records)
print(" -> Generating Attendance...")
att_binds = []
statuses = ['Present'] * 80 + ['Absent'] * 5 + ['Late'] * 10 + ['Leave'] * 5
for eid in emp_ids:
    for i in range(30):
        # random chance to skip generating for this day to keep DB size manageable, though we want ~500 minimum per entity.
        if random.random() < 0.9:
            att_binds.append((now - timedelta(days=i), random.choice(statuses), eid))
for i in range(0, len(att_binds), 5000):
    execute_many("INSERT INTO ATTENDANCE (date_col, status, employee_id) VALUES (:1, :2, :3)", att_binds[i:i+5000])

# BONUS_POINTS & PENALTIES
print(" -> Generating Bonus/Penalties...")
bp_binds = []
pen_binds = []
levels = ['Low', 'Medium', 'High']
for eid in random.sample(emp_ids, 200):
    bp_binds.append((now.month, now.year, random.randint(10, 100), eid))
for eid in random.sample(emp_ids, 100):
    pen_binds.append((random.choice(levels), 'Violation', now - timedelta(days=random.randint(1, 30)), eid))

execute_many("INSERT INTO BONUS_POINTS (month_col, year_col, points, employee_id) VALUES (:1, :2, :3, :4)", bp_binds)
execute_many("INSERT INTO PENALTIES (penalty_level, description, penalty_date, employee_id) VALUES (:1, :2, :3, :4)", pen_binds)

# BP LOG
print(" -> Syncing BP Log...")
bonus_ids = dml("SELECT bonus_point_id, employee_id FROM BONUS_POINTS")
penalty_ids = dml("SELECT penalty_id, employee_id FROM PENALTIES")
log_binds = []
for b in bonus_ids:
    log_binds.append(('Bonus', b['bonus_point_id'], b['employee_id']))
for p in penalty_ids:
    log_binds.append(('Penalty', p['penalty_id'], p['employee_id']))
execute_many("INSERT INTO BP (type_col, reference_id, employee_id) VALUES (:1, :2, :3)", log_binds)

# YEARLY BONUS
print(" -> Generating Yearly Bonus...")
yb_binds = []
for eid in random.sample(emp_ids, 150):
    # Generates a pseudo yearly bonus based on random bonus point score and random bonus amount (e.g. 5M - 20M)
    total_points = random.randint(50, 300)
    bonus_score = random.uniform(1.0, 3.5) * 10000000 # Score translated to money for the system
    yb_binds.append((now.year - 1, total_points, bonus_score, eid))

execute_many("INSERT INTO YEARLY_BONUS (year_col, total_bonus_point, yearly_bonus_score, employee_id) VALUES (:1, :2, :3, :4)", yb_binds)

print("✅ Data successfully seeded!")
