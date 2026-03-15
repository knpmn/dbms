-- ==========================================
-- 1. DROP EXISTING TABLES (Ignore errors on first run)
-- ==========================================
BEGIN
   EXECUTE IMMEDIATE 'DROP VIEW vw_department_headcount';
   EXECUTE IMMEDIATE 'DROP VIEW vw_monthly_bonus_summary';
   EXECUTE IMMEDIATE 'DROP VIEW vw_top_performance_bonus';
   EXECUTE IMMEDIATE 'DROP VIEW vw_employee_directory';
   EXECUTE IMMEDIATE 'DROP VIEW vw_contract_expiry_alert';
   EXECUTE IMMEDIATE 'DROP VIEW vw_penalty_history';
   EXECUTE IMMEDIATE 'DROP VIEW vw_today_attendance_status';
   EXECUTE IMMEDIATE 'DROP VIEW vw_monthly_attendance_summary';
   EXECUTE IMMEDIATE 'DROP VIEW vw_active_recruitment';
   EXECUTE IMMEDIATE 'DROP VIEW vw_yearly_bonus_overview';
EXCEPTION WHEN OTHERS THEN NULL; END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE Yearly_Bonus CASCADE CONSTRAINTS';
   EXECUTE IMMEDIATE 'DROP TABLE Recruitment CASCADE CONSTRAINTS';
   EXECUTE IMMEDIATE 'DROP TABLE Attendance CASCADE CONSTRAINTS';
   EXECUTE IMMEDIATE 'DROP TABLE Penalties CASCADE CONSTRAINTS';
   EXECUTE IMMEDIATE 'DROP TABLE Contracts CASCADE CONSTRAINTS';
   EXECUTE IMMEDIATE 'DROP TABLE Bonus_Points CASCADE CONSTRAINTS';
   EXECUTE IMMEDIATE 'DROP TABLE Employees CASCADE CONSTRAINTS';
   EXECUTE IMMEDIATE 'DROP TABLE Positions CASCADE CONSTRAINTS';
   EXECUTE IMMEDIATE 'DROP TABLE Departments CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL; END;
/

-- ==========================================
-- 2. CREATE TABLES
-- ==========================================
CREATE TABLE Departments (
    department_id NUMBER PRIMARY KEY,
    department_name VARCHAR2(100)
);

CREATE TABLE Positions (
    position_id NUMBER PRIMARY KEY,
    position_name VARCHAR2(100),
    base_salary NUMBER(10, 2)
);

CREATE TABLE Employees (
    employee_id NUMBER PRIMARY KEY,
    first_name VARCHAR2(50),
    last_name VARCHAR2(50),
    email VARCHAR2(100),
    department_id NUMBER,
    position_id NUMBER,
    FOREIGN KEY (department_id) REFERENCES Departments(department_id),
    FOREIGN KEY (position_id) REFERENCES Positions(position_id)
);

CREATE TABLE Bonus_Points (
    bonus_id NUMBER PRIMARY KEY,
    employee_id NUMBER,
    points NUMBER,
    bonus_date DATE,
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

CREATE TABLE Contracts (
    contract_id NUMBER PRIMARY KEY,
    employee_id NUMBER,
    contract_type VARCHAR2(50),
    end_date DATE,
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

CREATE TABLE Penalties (
    penalty_id NUMBER PRIMARY KEY,
    employee_id NUMBER,
    penalty_date DATE,
    penalty_level VARCHAR2(50),
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

CREATE TABLE Attendance (
    attendance_id NUMBER PRIMARY KEY,
    employee_id NUMBER,
    attendance_date DATE,
    status VARCHAR2(50),
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

CREATE TABLE Recruitment (
    recruitment_id NUMBER PRIMARY KEY,
    department_id NUMBER,
    position_id NUMBER,
    contact_email VARCHAR2(100),
    FOREIGN KEY (department_id) REFERENCES Departments(department_id),
    FOREIGN KEY (position_id) REFERENCES Positions(position_id)
);

CREATE TABLE Yearly_Bonus (
    yearly_bonus_id NUMBER PRIMARY KEY,
    employee_id NUMBER,
    bonus_year NUMBER,
    yearly_bonus_score NUMBER(5, 2),
    total_bonus_score NUMBER(5, 2),
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

-- ==========================================
-- 3. INSERT PSEUDO DATA
-- ==========================================
INSERT INTO Departments VALUES (1, 'IT');
INSERT INTO Departments VALUES (2, 'HR');
INSERT INTO Departments VALUES (3, 'Sales');

INSERT INTO Positions VALUES (1, 'Software Engineer', 50000.00);
INSERT INTO Positions VALUES (2, 'HR Manager', 60000.00);
INSERT INTO Positions VALUES (3, 'Sales Executive', 35000.00);

INSERT INTO Employees VALUES (101, 'Somchai', 'Jaidee', 'somchai@company.com', 1, 1);
INSERT INTO Employees VALUES (102, 'Suda', 'Rakngan', 'suda@company.com', 2, 2);
INSERT INTO Employees VALUES (103, 'Wichai', 'Maneerat', 'wichai@company.com', 3, 3);
INSERT INTO Employees VALUES (104, 'Mali', 'Suksawat', 'mali@company.com', 1, 1);

INSERT INTO Bonus_Points VALUES (1, 101, 50, DATE '2026-02-15');
INSERT INTO Bonus_Points VALUES (2, 101, 30, DATE '2026-02-20');
INSERT INTO Bonus_Points VALUES (3, 102, 100, DATE '2026-02-18');
INSERT INTO Bonus_Points VALUES (4, 103, 80, DATE '2026-03-05');

INSERT INTO Contracts VALUES (1, 101, 'Full-time', DATE '2026-12-31');
INSERT INTO Contracts VALUES (2, 103, 'Probation', DATE '2026-04-15');

INSERT INTO Penalties VALUES (1, 104, DATE '2026-01-10', 'Warning');

INSERT INTO Attendance VALUES (1, 101, SYSDATE, 'Present');
INSERT INTO Attendance VALUES (2, 102, SYSDATE, 'Absent');
INSERT INTO Attendance VALUES (3, 103, SYSDATE, 'Present');
INSERT INTO Attendance VALUES (4, 104, SYSDATE, 'Take a day off');
INSERT INTO Attendance VALUES (5, 101, DATE '2026-03-01', 'Present');
INSERT INTO Attendance VALUES (6, 101, DATE '2026-03-02', 'Absent');

INSERT INTO Recruitment VALUES (1, 1, 1, 'jobs@company.com');

INSERT INTO Yearly_Bonus VALUES (1, 101, 2025, 8.5, 85.0);
INSERT INTO Yearly_Bonus VALUES (2, 102, 2025, 9.0, 90.0);

COMMIT;

-- -- ==========================================
-- -- 4. CREATE THE 10 VIEWS
-- -- ==========================================

-- -- View 1
-- CREATE VIEW vw_department_headcount AS
-- SELECT d.department_id, d.department_name, COUNT(e.employee_id) AS total_employees
-- FROM Departments d
-- LEFT JOIN Employees e ON d.department_id = e.department_id
-- GROUP BY d.department_id, d.department_name;

-- -- View 2: Using TO_CHAR to extract month/year as numbers without EXTRACT
-- CREATE VIEW vw_monthly_bonus_summary AS
-- SELECT e.employee_id, e.first_name, e.last_name, 
--        TO_NUMBER(TO_CHAR(b.bonus_date, 'MM')) AS bonus_month, 
--        TO_NUMBER(TO_CHAR(b.bonus_date, 'YYYY')) AS bonus_year, 
--        SUM(b.points) AS total_monthly_points
-- FROM Employees e
-- JOIN Bonus_Points b ON e.employee_id = b.employee_id
-- GROUP BY e.employee_id, e.first_name, e.last_name, 
--          TO_NUMBER(TO_CHAR(b.bonus_date, 'MM')), 
--          TO_NUMBER(TO_CHAR(b.bonus_date, 'YYYY'));

-- -- View 3
-- CREATE VIEW vw_top_performance_bonus AS
-- SELECT e.employee_id, e.first_name, e.last_name, SUM(b.points) AS total_accumulated_points
-- FROM Employees e
-- JOIN Bonus_Points b ON e.employee_id = b.employee_id
-- GROUP BY e.employee_id, e.first_name, e.last_name;

-- -- View 4
-- CREATE VIEW vw_employee_directory AS
-- SELECT e.employee_id, e.first_name, e.last_name, e.email, d.department_name, p.position_name, p.base_salary
-- FROM Employees e
-- LEFT JOIN Departments d ON e.department_id = d.department_id
-- LEFT JOIN Positions p ON e.position_id = p.position_id;

-- -- View 5: Direct date subtraction in Oracle yields days (no DATEDIFF needed)
-- CREATE VIEW vw_contract_expiry_alert AS
-- SELECT e.employee_id, e.first_name, e.last_name, c.contract_id, c.contract_type, c.end_date, 
--        ROUND(c.end_date - SYSDATE) AS days_remaining
-- FROM Employees e
-- JOIN Contracts c ON e.employee_id = c.employee_id;

-- -- View 6
-- CREATE VIEW vw_penalty_history AS
-- SELECT p.penalty_id, e.employee_id, e.first_name, e.last_name, p.penalty_date, p.penalty_level
-- FROM Employees e
-- JOIN Penalties p ON e.employee_id = p.employee_id;

-- -- View 7: Formatting SYSDATE to drop the time component for a clean match
-- CREATE VIEW vw_today_attendance_status AS
-- SELECT e.employee_id, e.first_name, e.last_name, a.attendance_date, a.status
-- FROM Employees e
-- JOIN Attendance a ON e.employee_id = a.employee_id
-- WHERE TO_CHAR(a.attendance_date, 'YYYY-MM-DD') = TO_CHAR(SYSDATE, 'YYYY-MM-DD');

-- -- View 8
-- CREATE VIEW vw_monthly_attendance_summary AS
-- SELECT e.employee_id, e.first_name, e.last_name, 
--        TO_NUMBER(TO_CHAR(a.attendance_date, 'MM')) AS attendance_month, 
--        TO_NUMBER(TO_CHAR(a.attendance_date, 'YYYY')) AS attendance_year,
--        SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) AS total_present,
--        SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) AS total_absent,
--        SUM(CASE WHEN a.status = 'Take a day off' THEN 1 ELSE 0 END) AS total_leave
-- FROM Employees e
-- JOIN Attendance a ON e.employee_id = a.employee_id
-- GROUP BY e.employee_id, e.first_name, e.last_name, 
--          TO_NUMBER(TO_CHAR(a.attendance_date, 'MM')), 
--          TO_NUMBER(TO_CHAR(a.attendance_date, 'YYYY'));

-- -- View 9
-- CREATE VIEW vw_active_recruitment AS
-- SELECT d.department_name, p.position_name, r.contact_email
-- FROM Recruitment r
-- JOIN Departments d ON r.department_id = d.department_id
-- JOIN Positions p ON r.position_id = p.position_id;

-- -- View 10
-- CREATE VIEW vw_yearly_bonus_overview AS
-- SELECT yb.yearly_bonus_id, e.employee_id, e.first_name, e.last_name, yb.bonus_year, yb.yearly_bonus_score, yb.total_bonus_score
-- FROM Employees e
-- JOIN Yearly_Bonus yb ON e.employee_id = yb.employee_id;



-- ==========================================
-- 4. CREATE THE 10 VIEWS (Oracle (+) join syntax)
-- ==========================================

-- View 1
CREATE VIEW vw_department_headcount AS
SELECT d.department_id, d.department_name, COUNT(e.employee_id) AS total_employees
FROM Departments d, Employees e
WHERE d.department_id = e.department_id(+)
GROUP BY d.department_id, d.department_name;

-- View 2
CREATE VIEW vw_monthly_bonus_summary AS
SELECT e.employee_id, e.first_name, e.last_name,
       TO_NUMBER(TO_CHAR(b.bonus_date, 'MM')) AS bonus_month,
       TO_NUMBER(TO_CHAR(b.bonus_date, 'YYYY')) AS bonus_year,
       SUM(b.points) AS total_monthly_points
FROM Employees e, Bonus_Points b
WHERE e.employee_id = b.employee_id
GROUP BY e.employee_id, e.first_name, e.last_name,
         TO_NUMBER(TO_CHAR(b.bonus_date, 'MM')),
         TO_NUMBER(TO_CHAR(b.bonus_date, 'YYYY'));

-- View 3
CREATE VIEW vw_top_performance_bonus AS
SELECT e.employee_id, e.first_name, e.last_name, SUM(b.points) AS total_accumulated_points
FROM Employees e, Bonus_Points b
WHERE e.employee_id = b.employee_id
GROUP BY e.employee_id, e.first_name, e.last_name;

-- View 4
CREATE VIEW vw_employee_directory AS
SELECT e.employee_id, e.first_name, e.last_name, e.email,
       d.department_name, p.position_name, p.base_salary
FROM Employees e, Departments d, Positions p
WHERE e.department_id = d.department_id(+)
  AND e.position_id   = p.position_id(+);

-- View 5
CREATE VIEW vw_contract_expiry_alert AS
SELECT e.employee_id, e.first_name, e.last_name,
       c.contract_id, c.contract_type, c.end_date,
       ROUND(c.end_date - SYSDATE) AS days_remaining
FROM Employees e, Contracts c
WHERE e.employee_id = c.employee_id;

-- View 6
CREATE VIEW vw_penalty_history AS
SELECT p.penalty_id, e.employee_id, e.first_name, e.last_name,
       p.penalty_date, p.penalty_level
FROM Employees e, Penalties p
WHERE e.employee_id = p.employee_id;

-- View 7
CREATE VIEW vw_today_attendance_status AS
SELECT e.employee_id, e.first_name, e.last_name,
       a.attendance_date, a.status
FROM Employees e, Attendance a
WHERE e.employee_id = a.employee_id
  AND TO_CHAR(a.attendance_date, 'YYYY-MM-DD') = TO_CHAR(SYSDATE, 'YYYY-MM-DD');

-- View 8
CREATE VIEW vw_monthly_attendance_summary AS
SELECT e.employee_id, e.first_name, e.last_name,
       TO_NUMBER(TO_CHAR(a.attendance_date, 'MM'))   AS attendance_month,
       TO_NUMBER(TO_CHAR(a.attendance_date, 'YYYY')) AS attendance_year,
       SUM(CASE WHEN a.status = 'Present'        THEN 1 ELSE 0 END) AS total_present,
       SUM(CASE WHEN a.status = 'Absent'         THEN 1 ELSE 0 END) AS total_absent,
       SUM(CASE WHEN a.status = 'Take a day off' THEN 1 ELSE 0 END) AS total_leave
FROM Employees e, Attendance a
WHERE e.employee_id = a.employee_id
GROUP BY e.employee_id, e.first_name, e.last_name,
         TO_NUMBER(TO_CHAR(a.attendance_date, 'MM')),
         TO_NUMBER(TO_CHAR(a.attendance_date, 'YYYY'));

-- View 9
CREATE VIEW vw_active_recruitment AS
SELECT d.department_name, p.position_name, r.contact_email
FROM Recruitment r, Departments d, Positions p
WHERE r.department_id = d.department_id
  AND r.position_id   = p.position_id;

-- View 10
CREATE VIEW vw_yearly_bonus_overview AS
SELECT yb.yearly_bonus_id, e.employee_id, e.first_name, e.last_name,
       yb.bonus_year, yb.yearly_bonus_score, yb.total_bonus_score
FROM Employees e, Yearly_Bonus yb
WHERE e.employee_id = yb.employee_id;









-- NEW VIEW แก้



-- View 2
CREATE OR REPLACE VIEW vw_monthly_bonus_summary AS
SELECT e.employee_id, e.first_name, e.last_name,
       TO_NUMBER(TO_CHAR(b.bonus_date, 'MM'))   AS bonus_month,
       TO_NUMBER(TO_CHAR(b.bonus_date, 'YYYY')) AS bonus_year,
       LEAST(SUM(b.points), 10)                 AS total_monthly_points
FROM Employees e, Bonus_Points b
WHERE e.employee_id = b.employee_id
GROUP BY e.employee_id, e.first_name, e.last_name,
         TO_NUMBER(TO_CHAR(b.bonus_date, 'MM')),
         TO_NUMBER(TO_CHAR(b.bonus_date, 'YYYY'));

-- View 3
CREATE OR REPLACE VIEW vw_top_performance_bonus AS
WITH monthly_capped AS (
    SELECT
        e.employee_id,
        e.first_name,
        e.last_name,
        TO_NUMBER(TO_CHAR(b.bonus_date, 'YYYY')) AS bonus_year,
        TO_NUMBER(TO_CHAR(b.bonus_date, 'MM'))   AS bonus_month,
        LEAST(SUM(b.points), 10)                 AS capped_points
    FROM Employees e, Bonus_Points b
    WHERE e.employee_id = b.employee_id
    GROUP BY
        e.employee_id, e.first_name, e.last_name,
        TO_NUMBER(TO_CHAR(b.bonus_date, 'YYYY')),
        TO_NUMBER(TO_CHAR(b.bonus_date, 'MM'))
)
SELECT
    employee_id,
    first_name,
    last_name,
    SUM(capped_points) AS total_accumulated_points
FROM monthly_capped
GROUP BY employee_id, first_name, last_name;

-- View 10
CREATE OR REPLACE VIEW vw_yearly_bonus_overview AS
WITH monthly_capped AS (
    SELECT
        e.employee_id,
        e.first_name,
        e.last_name,
        TO_NUMBER(TO_CHAR(b.bonus_date, 'YYYY')) AS bonus_year,
        TO_NUMBER(TO_CHAR(b.bonus_date, 'MM'))   AS bonus_month,
        LEAST(SUM(b.points), 10)                 AS capped_points
    FROM Employees e, Bonus_Points b
    WHERE e.employee_id = b.employee_id
    GROUP BY
        e.employee_id, e.first_name, e.last_name,
        TO_NUMBER(TO_CHAR(b.bonus_date, 'YYYY')),
        TO_NUMBER(TO_CHAR(b.bonus_date, 'MM'))
),
yearly_agg AS (
    SELECT
        employee_id,
        first_name,
        last_name,
        bonus_year,
        SUM(capped_points) AS total_bonus_score
    FROM monthly_capped
    GROUP BY employee_id, first_name, last_name, bonus_year
)
SELECT
    ROW_NUMBER() OVER (ORDER BY bonus_year DESC, total_bonus_score DESC) AS yearly_bonus_id,
    employee_id,
    first_name,
    last_name,
    bonus_year,
    total_bonus_score
FROM yearly_agg;