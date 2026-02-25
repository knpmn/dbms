-- =============================================================
--  SMART HR SYSTEM - Oracle SQL Schema
--  Run this script in SQL*Plus or SQL Developer as SYS/SYSTEM
--  or as the HR schema owner.
-- =============================================================

-- -----------------------------------------------
-- DROP tables (safe order: children first)
-- -----------------------------------------------
BEGIN
  FOR t IN (
    SELECT table_name FROM user_tables
    WHERE table_name IN (
      'BP','PENALTIES','YEARLY_BONUS','BONUS_POINTS',
      'ATTENDANCE','EMPLOYEES','POSITIONS','DEPARTMENTS',
      'USERS','ROLES'
    )
  ) LOOP
    EXECUTE IMMEDIATE 'DROP TABLE ' || t.table_name || ' CASCADE CONSTRAINTS';
  END LOOP;
END;
/

-- -----------------------------------------------
-- 1. ROLES
-- -----------------------------------------------
CREATE TABLE ROLES (
    role_id       NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    role_name     VARCHAR2(50)  NOT NULL UNIQUE,
    description   VARCHAR2(255)
);

-- -----------------------------------------------
-- 2. USERS
-- -----------------------------------------------
CREATE TABLE USERS (
    user_id   NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username  VARCHAR2(50)  NOT NULL UNIQUE,
    password  VARCHAR2(255) NOT NULL,   -- stored as hashed value
    email     VARCHAR2(100) NOT NULL UNIQUE,
    role_id   NUMBER NOT NULL,
    CONSTRAINT fk_users_role FOREIGN KEY (role_id) REFERENCES ROLES(role_id)
);

-- -----------------------------------------------
-- 3. DEPARTMENTS
-- -----------------------------------------------
CREATE TABLE DEPARTMENTS (
    department_id   NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    department_name VARCHAR2(100) NOT NULL UNIQUE,
    description     VARCHAR2(255)
);

-- -----------------------------------------------
-- 4. POSITIONS
-- -----------------------------------------------
CREATE TABLE POSITIONS (
    position_id   NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    position_name VARCHAR2(100) NOT NULL UNIQUE,
    base_salary   NUMBER(15,2) NOT NULL
);

-- -----------------------------------------------
-- 5. EMPLOYEES
-- -----------------------------------------------
CREATE TABLE EMPLOYEES (
    employee_id   NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name    VARCHAR2(50)  NOT NULL,
    last_name     VARCHAR2(50)  NOT NULL,
    salary        NUMBER(15,2)  NOT NULL,
    start_date    DATE          NOT NULL,
    department_id NUMBER        NOT NULL,
    position_id   NUMBER        NOT NULL,
    CONSTRAINT fk_emp_dept FOREIGN KEY (department_id) REFERENCES DEPARTMENTS(department_id),
    CONSTRAINT fk_emp_pos  FOREIGN KEY (position_id)   REFERENCES POSITIONS(position_id)
);

-- -----------------------------------------------
-- 6. ATTENDANCE
-- -----------------------------------------------
CREATE TABLE ATTENDANCE (
    attendance_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    date_col      DATE          NOT NULL,
    status        VARCHAR2(20)  NOT NULL
        CHECK (status IN ('Present','Absent','Late','Leave')),
    employee_id   NUMBER        NOT NULL,
    CONSTRAINT fk_att_emp FOREIGN KEY (employee_id) REFERENCES EMPLOYEES(employee_id)
);

-- -----------------------------------------------
-- 7. BONUS_POINTS
-- -----------------------------------------------
CREATE TABLE BONUS_POINTS (
    bonus_point_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    month_col      NUMBER(2)  NOT NULL CHECK (month_col BETWEEN 1 AND 12),
    year_col       NUMBER(4)  NOT NULL,
    points         NUMBER(10) NOT NULL,
    employee_id    NUMBER     NOT NULL,
    CONSTRAINT fk_bp_emp FOREIGN KEY (employee_id) REFERENCES EMPLOYEES(employee_id)
);

-- -----------------------------------------------
-- 8. YEARLY_BONUS
-- -----------------------------------------------
CREATE TABLE YEARLY_BONUS (
    yearly_bonus_id    NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    year_col           NUMBER(4)     NOT NULL,
    total_bonus_point  NUMBER(15,2),
    yearly_bonus_score NUMBER(15,2),
    employee_id        NUMBER        NOT NULL,
    CONSTRAINT fk_yb_emp FOREIGN KEY (employee_id) REFERENCES EMPLOYEES(employee_id)
);

-- -----------------------------------------------
-- 9. PENALTIES
-- -----------------------------------------------
CREATE TABLE PENALTIES (
    penalty_id    NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    penalty_level VARCHAR2(20)  NOT NULL
        CHECK (penalty_level IN ('Low','Medium','High')),
    description   VARCHAR2(255),
    penalty_date  DATE          NOT NULL,
    employee_id   NUMBER        NOT NULL,
    CONSTRAINT fk_pen_emp FOREIGN KEY (employee_id) REFERENCES EMPLOYEES(employee_id)
);

-- -----------------------------------------------
-- 10. BP  (Bonus & Penalty log)
-- -----------------------------------------------
CREATE TABLE BP (
    bp_id         NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    type_col      VARCHAR2(10)  NOT NULL
        CHECK (type_col IN ('Bonus','Penalty')),
    reference_id  NUMBER        NOT NULL,  -- FK to BONUS_POINTS or PENALTIES
    created_date  DATE          DEFAULT SYSDATE NOT NULL,
    employee_id   NUMBER        NOT NULL,
    CONSTRAINT fk_bplog_emp FOREIGN KEY (employee_id) REFERENCES EMPLOYEES(employee_id)
);

-- =============================================================
--  SEED DATA
-- =============================================================

-- Roles
INSERT INTO ROLES (role_name, description) VALUES ('Admin',    'Full system access');
INSERT INTO ROLES (role_name, description) VALUES ('HR Staff', 'Manages employees, attendance, bonus/penalty');
INSERT INTO ROLES (role_name, description) VALUES ('Employee', 'Views own profile and records');

-- Default Admin User  (password: admin123  — hashed with werkzeug pbkdf2:sha256)
-- NOTE: The hash below is computed by werkzeug generate_password_hash('admin123')
--       If it doesn't work, log in and reset via the Users CRUD page.
INSERT INTO USERS (username, password, email, role_id)
VALUES (
    'admin',
    'scrypt:32768:8:1$BO5oXC6qBIcKqByq$4183b829b5cdc904432d2b2bcac9f25cf38385d193440dc380f6dd9a8ebe6e648ef0ccb5bb2641099715ddc89d87d2bb7772b9215c2233908f64ca469b263bc3',
    'admin@hrapp.com',
    1
);

-- Sample Departments
INSERT INTO DEPARTMENTS (department_name, description) VALUES ('Human Resources', 'Manages HR operations');
INSERT INTO DEPARTMENTS (department_name, description) VALUES ('Engineering',     'Software development team');
INSERT INTO DEPARTMENTS (department_name, description) VALUES ('Finance',         'Financial operations');

-- Sample Positions
INSERT INTO POSITIONS (position_name, base_salary) VALUES ('HR Manager',       8000000);
INSERT INTO POSITIONS (position_name, base_salary) VALUES ('Software Engineer', 12000000);
INSERT INTO POSITIONS (position_name, base_salary) VALUES ('Accountant',        7000000);

COMMIT;

-- =============================================================
--  Quick verification
-- =============================================================
SELECT * FROM ROLES;
SELECT * FROM USERS;
SELECT * FROM DEPARTMENTS;
SELECT * FROM POSITIONS;
