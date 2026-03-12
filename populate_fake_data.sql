-- ============================================================
-- populate_fake_data.sql
-- Realistic seed data for a small    company (~25 employees)
-- Run AFTER oracledatabase.sql (schema + views already exist)
-- ============================================================

-- ============================================================
-- 0. CLEAR EXISTING DATA (order matters — child tables first)
-- ============================================================
DELETE FROM Yearly_Bonus;
DELETE FROM Recruitment;
DELETE FROM Attendance;
DELETE FROM Penalties;
DELETE FROM Contracts;
DELETE FROM Bonus_Points;
DELETE FROM Employees;
DELETE FROM Positions;
DELETE FROM Departments;
COMMIT;

-- ============================================================
-- 1. DEPARTMENTS  (5 departments — typical small company)
-- ============================================================
INSERT INTO Departments VALUES (1, 'IT');
INSERT INTO Departments VALUES (2, 'Human Resources');
INSERT INTO Departments VALUES (3, 'Sales');
INSERT INTO Departments VALUES (4, 'Finance');
INSERT INTO Departments VALUES (5, 'Operations');

-- ============================================================
-- 2. POSITIONS  (10 roles with realistic Thai-SME salaries, THB/mo)
-- ============================================================
INSERT INTO Positions VALUES (1,  'Software Engineer',         52000.00);
INSERT INTO Positions VALUES (2,  'Senior Software Engineer',  72000.00);
INSERT INTO Positions VALUES (3,  'IT Support Specialist',     35000.00);
INSERT INTO Positions VALUES (4,  'HR Manager',                58000.00);
INSERT INTO Positions VALUES (5,  'HR Officer',                38000.00);
INSERT INTO Positions VALUES (6,  'Sales Manager',             55000.00);
INSERT INTO Positions VALUES (7,  'Sales Executive',           32000.00);
INSERT INTO Positions VALUES (8,  'Financial Analyst',         50000.00);
INSERT INTO Positions VALUES (9,  'Accountant',                42000.00);
INSERT INTO Positions VALUES (10, 'Operations Coordinator',    40000.00);

-- ============================================================
-- 3. EMPLOYEES  (25 people — Thai first/last names)
-- ============================================================
-- IT (6)
INSERT INTO Employees VALUES (101, 'Somchai',   'Jaidee',      'somchai@company.com',   1, 1);
INSERT INTO Employees VALUES (102, 'Mali',      'Suksawat',    'mali@company.com',      1, 1);
INSERT INTO Employees VALUES (103, 'Arthit',    'Wongsai',     'arthit@company.com',    1, 2);
INSERT INTO Employees VALUES (104, 'Napatporn', 'Srisuwan',    'napatporn@company.com', 1, 3);
INSERT INTO Employees VALUES (105, 'Phurit',    'Tangkawee',   'phurit@company.com',    1, 3);
INSERT INTO Employees VALUES (106, 'Kanjana',   'Phromma',     'kanjana@company.com',   1, 1);
-- HR (3)
INSERT INTO Employees VALUES (107, 'Suda',      'Rakngan',     'suda@company.com',      2, 4);
INSERT INTO Employees VALUES (108, 'Wanpen',    'Charoenwong', 'wanpen@company.com',    2, 5);
INSERT INTO Employees VALUES (109, 'Pracha',    'Boonmee',     'pracha@company.com',    2, 5);
-- Sales (7)
INSERT INTO Employees VALUES (110, 'Wichai',    'Maneerat',    'wichai@company.com',    3, 6);
INSERT INTO Employees VALUES (111, 'Nattapong', 'Saengsuk',    'nattapong@company.com', 3, 7);
INSERT INTO Employees VALUES (112, 'Supawit',   'Chaiprasert', 'supawit@company.com',   3, 7);
INSERT INTO Employees VALUES (113, 'Lalita',    'Bunyarit',    'lalita@company.com',    3, 7);
INSERT INTO Employees VALUES (114, 'Komsun',    'Klahan',      'komsun@company.com',    3, 7);
INSERT INTO Employees VALUES (115, 'Parichat',  'Songserm',    'parichat@company.com',  3, 7);
INSERT INTO Employees VALUES (116, 'Teerawut',  'Panya',       'teerawut@company.com',  3, 7);
-- Finance (4)
INSERT INTO Employees VALUES (117, 'Kanokwan',  'Meesum',      'kanokwan@company.com',  4, 8);
INSERT INTO Employees VALUES (118, 'Boonchu',   'Duangrat',    'boonchu@company.com',   4, 9);
INSERT INTO Employees VALUES (119, 'Siriwat',   'Chaiyo',      'siriwat@company.com',   4, 9);
INSERT INTO Employees VALUES (120, 'Patchara',  'Jitmun',      'patchara@company.com',  4, 8);
-- Operations (5)
INSERT INTO Employees VALUES (121, 'Anong',     'Prasit',      'anong@company.com',     5, 10);
INSERT INTO Employees VALUES (122, 'Sunan',     'Kaewkla',     'sunan@company.com',     5, 10);
INSERT INTO Employees VALUES (123, 'Thanit',    'Polsuk',      'thanit@company.com',    5, 10);
INSERT INTO Employees VALUES (124, 'Nipon',     'Sangwan',     'nipon@company.com',     5, 10);
INSERT INTO Employees VALUES (125, 'Ratirat',   'Poolsuk',     'ratirat@company.com',   5, 10);

-- ============================================================
-- 4. CONTRACTS
-- ============================================================
-- Full-time — established staff
INSERT INTO Contracts VALUES (1,  101, 'Full-time', DATE '2027-06-30');
INSERT INTO Contracts VALUES (2,  102, 'Full-time', DATE '2027-03-31');
INSERT INTO Contracts VALUES (3,  103, 'Full-time', DATE '2026-12-31');
INSERT INTO Contracts VALUES (4,  104, 'Full-time', DATE '2027-01-15');
INSERT INTO Contracts VALUES (5,  106, 'Full-time', DATE '2026-09-30');
INSERT INTO Contracts VALUES (6,  107, 'Full-time', DATE '2027-06-30');
INSERT INTO Contracts VALUES (7,  108, 'Full-time', DATE '2026-12-31');
INSERT INTO Contracts VALUES (8,  110, 'Full-time', DATE '2027-03-31');
INSERT INTO Contracts VALUES (9,  111, 'Full-time', DATE '2026-10-31');
INSERT INTO Contracts VALUES (10, 117, 'Full-time', DATE '2027-06-30');
INSERT INTO Contracts VALUES (11, 118, 'Full-time', DATE '2026-11-30');
INSERT INTO Contracts VALUES (12, 121, 'Full-time', DATE '2027-03-31');
INSERT INTO Contracts VALUES (13, 122, 'Full-time', DATE '2026-12-31');
-- Probation — newer hires (some expiring soon!)
INSERT INTO Contracts VALUES (14, 105, 'Probation', DATE '2026-04-01');  -- 19 days left
INSERT INTO Contracts VALUES (15, 109, 'Probation', DATE '2026-04-15');
INSERT INTO Contracts VALUES (16, 112, 'Probation', DATE '2026-05-30');
INSERT INTO Contracts VALUES (17, 113, 'Probation', DATE '2026-06-30');
INSERT INTO Contracts VALUES (18, 119, 'Probation', DATE '2026-03-20');  -- 7 days left!
INSERT INTO Contracts VALUES (19, 123, 'Probation', DATE '2026-05-01');
INSERT INTO Contracts VALUES (20, 124, 'Probation', DATE '2026-04-30');
-- Part-time
INSERT INTO Contracts VALUES (21, 114, 'Part-time', DATE '2026-08-31');
INSERT INTO Contracts VALUES (22, 115, 'Part-time', DATE '2026-07-31');
INSERT INTO Contracts VALUES (23, 116, 'Part-time', DATE '2026-09-30');
INSERT INTO Contracts VALUES (24, 120, 'Part-time', DATE '2026-10-31');
INSERT INTO Contracts VALUES (25, 125, 'Part-time', DATE '2026-06-30');

-- ============================================================
-- 5. BONUS POINTS  (Jan 2025 – Feb 2026, 14 months, PL/SQL loop)
--    Uses deterministic formula to fake "random" variety
-- ============================================================
DECLARE
    v_id     NUMBER := 1;
    TYPE t_ids   IS TABLE OF NUMBER;
    TYPE t_dates IS TABLE OF DATE;

    emps  t_ids   := t_ids(101,102,103,104,105,106,107,108,109,110,
                           111,112,113,114,115,116,117,118,119,120,
                           121,122,123,124,125);

    months t_dates := t_dates(
        DATE '2025-01-15', DATE '2025-02-15', DATE '2025-03-15',
        DATE '2025-04-15', DATE '2025-05-15', DATE '2025-06-15',
        DATE '2025-07-15', DATE '2025-08-15', DATE '2025-09-15',
        DATE '2025-10-15', DATE '2025-11-15', DATE '2025-12-15',
        DATE '2026-01-15', DATE '2026-02-15'
    );

    v_pts   NUMBER;
    v_rel   NUMBER; -- relative emp index (1-based)
BEGIN
    FOR mi IN 1 .. months.COUNT LOOP
        FOR ei IN 1 .. emps.COUNT LOOP
            v_rel := emps(ei) - 100;   -- 1–25
            -- Skip ~20 % of records (sparse, like real bonuses)
            IF MOD(v_rel * mi + mi, 5) != 0 THEN
                -- Points 20–95, different per employee and month
                v_pts := 20 + MOD(v_rel * 37 + mi * 53 + v_rel + mi, 76);
                INSERT INTO Bonus_Points VALUES (v_id, emps(ei), v_pts, months(mi));
                v_id := v_id + 1;
            END IF;
        END LOOP;
    END LOOP;
END;
/

-- ============================================================
-- 6. ATTENDANCE  (1 Jan – today, weekdays only — PL/SQL loop)
--    Realistic split: ~87 % Present, ~8 % Absent, ~5 % Leave
-- ============================================================
DECLARE
    v_id     NUMBER := 1;
    v_date   DATE   := DATE '2026-01-01';
    v_end    DATE   := TRUNC(SYSDATE);
    v_dow    NUMBER;
    v_rand   NUMBER;
    v_status VARCHAR2(20);
    TYPE t_ids IS TABLE OF NUMBER;
    emps t_ids := t_ids(101,102,103,104,105,106,107,108,109,110,
                        111,112,113,114,115,116,117,118,119,120,
                        121,122,123,124,125);
BEGIN
    WHILE v_date <= v_end LOOP
        v_dow := TO_NUMBER(TO_CHAR(v_date, 'D')); -- 1=Sun, 7=Sat (NLS-safe)
        IF v_dow BETWEEN 2 AND 6 THEN             -- Mon–Fri
            FOR ei IN 1 .. emps.COUNT LOOP
                v_rand := MOD(emps(ei) * TO_NUMBER(TO_CHAR(v_date,'DDD')) + ei * 19, 100);
                IF    v_rand < 87 THEN v_status := 'Present';
                ELSIF v_rand < 95 THEN v_status := 'Absent';
                ELSE                   v_status := 'Take a day off';
                END IF;
                INSERT INTO Attendance VALUES (v_id, emps(ei), v_date, v_status);
                v_id := v_id + 1;
            END LOOP;
        END IF;
        v_date := v_date + 1;
    END LOOP;
END;
/

-- ============================================================
-- 7. PENALTIES  (10 disciplinary records across 3 months)
--    Progressive escalation for repeat offenders
-- ============================================================
INSERT INTO Penalties VALUES (1,  105, DATE '2025-07-22', 'Warning');
INSERT INTO Penalties VALUES (2,  112, DATE '2025-09-03', 'Warning');
INSERT INTO Penalties VALUES (3,  116, DATE '2025-09-15', 'Warning');
INSERT INTO Penalties VALUES (4,  114, DATE '2025-10-15', 'Warning');
INSERT INTO Penalties VALUES (5,  119, DATE '2025-10-28', 'Warning');
INSERT INTO Penalties VALUES (6,  114, DATE '2025-11-20', 'Salary Reduction');  -- 2nd offense
INSERT INTO Penalties VALUES (7,  122, DATE '2025-12-01', 'Warning');
INSERT INTO Penalties VALUES (8,  116, DATE '2025-12-10', 'Salary Reduction');  -- 2nd offense
INSERT INTO Penalties VALUES (9,  114, DATE '2026-01-08', 'Suspension');         -- 3rd offense
INSERT INTO Penalties VALUES (10, 124, DATE '2026-02-20', 'Warning');

-- ============================================================
-- 8. RECRUITMENT  (5 open positions currently being filled)
-- ============================================================
INSERT INTO Recruitment VALUES (1, 1, 1,  'recruit.it@company.com');      -- Software Engineer
INSERT INTO Recruitment VALUES (2, 1, 2,  'recruit.it@company.com');      -- Senior Software Eng.
INSERT INTO Recruitment VALUES (3, 3, 7,  'recruit.sales@company.com');   -- Sales Executive
INSERT INTO Recruitment VALUES (4, 4, 9,  'recruit.finance@company.com'); -- Accountant
INSERT INTO Recruitment VALUES (5, 5, 10, 'recruit.ops@company.com');     -- Ops Coordinator

-- ============================================================
-- 9. YEARLY BONUS  (2024 proven performers + full 2025 cycle)
-- ============================================================
-- 2024 — only staff who were employed that year
INSERT INTO Yearly_Bonus VALUES (1,  101, 2024, 8.5,  85.0);
INSERT INTO Yearly_Bonus VALUES (2,  102, 2024, 7.2,  72.0);
INSERT INTO Yearly_Bonus VALUES (3,  103, 2024, 9.1,  91.0);
INSERT INTO Yearly_Bonus VALUES (4,  104, 2024, 6.8,  68.0);
INSERT INTO Yearly_Bonus VALUES (5,  106, 2024, 7.5,  75.0);
INSERT INTO Yearly_Bonus VALUES (6,  107, 2024, 9.0,  90.0);
INSERT INTO Yearly_Bonus VALUES (7,  108, 2024, 8.0,  80.0);
INSERT INTO Yearly_Bonus VALUES (8,  110, 2024, 7.8,  78.0);
INSERT INTO Yearly_Bonus VALUES (9,  111, 2024, 6.5,  65.0);
INSERT INTO Yearly_Bonus VALUES (10, 117, 2024, 8.3,  83.0);
INSERT INTO Yearly_Bonus VALUES (11, 118, 2024, 7.0,  70.0);
INSERT INTO Yearly_Bonus VALUES (12, 121, 2024, 7.6,  76.0);
INSERT INTO Yearly_Bonus VALUES (13, 122, 2024, 8.1,  81.0);
-- 2025 — all 25 employees (penalized ones score lower)
INSERT INTO Yearly_Bonus VALUES (14, 101, 2025, 9.0,  90.0);
INSERT INTO Yearly_Bonus VALUES (15, 102, 2025, 8.2,  82.0);
INSERT INTO Yearly_Bonus VALUES (16, 103, 2025, 9.5,  95.0);
INSERT INTO Yearly_Bonus VALUES (17, 104, 2025, 7.0,  70.0);
INSERT INTO Yearly_Bonus VALUES (18, 105, 2025, 5.5,  55.0);
INSERT INTO Yearly_Bonus VALUES (19, 106, 2025, 8.4,  84.0);
INSERT INTO Yearly_Bonus VALUES (20, 107, 2025, 9.2,  92.0);
INSERT INTO Yearly_Bonus VALUES (21, 108, 2025, 8.0,  80.0);
INSERT INTO Yearly_Bonus VALUES (22, 109, 2025, 6.8,  68.0);
INSERT INTO Yearly_Bonus VALUES (23, 110, 2025, 8.8,  88.0);
INSERT INTO Yearly_Bonus VALUES (24, 111, 2025, 7.5,  75.0);
INSERT INTO Yearly_Bonus VALUES (25, 112, 2025, 7.0,  70.0);
INSERT INTO Yearly_Bonus VALUES (26, 113, 2025, 7.8,  78.0);
INSERT INTO Yearly_Bonus VALUES (27, 114, 2025, 4.5,  45.0);  -- 3 penalties, low score
INSERT INTO Yearly_Bonus VALUES (28, 115, 2025, 6.5,  65.0);
INSERT INTO Yearly_Bonus VALUES (29, 116, 2025, 5.0,  50.0);  -- 2 penalties, low score
INSERT INTO Yearly_Bonus VALUES (30, 117, 2025, 8.6,  86.0);
INSERT INTO Yearly_Bonus VALUES (31, 118, 2025, 7.8,  78.0);
INSERT INTO Yearly_Bonus VALUES (32, 119, 2025, 6.2,  62.0);
INSERT INTO Yearly_Bonus VALUES (33, 120, 2025, 8.1,  81.0);
INSERT INTO Yearly_Bonus VALUES (34, 121, 2025, 7.9,  79.0);
INSERT INTO Yearly_Bonus VALUES (35, 122, 2025, 7.2,  72.0);
INSERT INTO Yearly_Bonus VALUES (36, 123, 2025, 8.3,  83.0);
INSERT INTO Yearly_Bonus VALUES (37, 124, 2025, 6.0,  60.0);
INSERT INTO Yearly_Bonus VALUES (38, 125, 2025, 6.8,  68.0);

COMMIT;

-- ============================================================
-- DONE — summary of what was inserted:
--   Departments : 5
--   Positions   : 10
--   Employees   : 25
--   Contracts   : 25  (13 full-time, 7 probation, 5 part-time)
--   Bonus_Points: ~280 rows (14 months, sparse)
--   Attendance  : ~25 × ~52 weekdays ≈ 1,300+ rows
--   Penalties   : 10 (progressive escalation for repeat offenders)
--   Recruitment : 5  (open positions)
--   Yearly_Bonus: 38 (2024 + 2025)
-- ============================================================
