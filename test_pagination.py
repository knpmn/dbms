import os
from dotenv import load_dotenv
import db

def test_query():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    load_dotenv(dotenv_path=env_path)
    db.init_pool()
    
    # Try the pagination query
    sql = """
        SELECT a.attendance_id, TO_CHAR(a.date_col,'YYYY-MM-DD') AS date_col,
               a.status, e.first_name || ' ' || e.last_name AS emp_name, a.employee_id
        FROM ATTENDANCE a 
        JOIN EMPLOYEES e ON a.employee_id = e.employee_id
        ORDER BY a.date_col desc
        OFFSET :v_offset ROWS FETCH NEXT :v_limit ROWS ONLY
    """
    binds = {'v_offset': 0, 'v_limit': 10}
    
    try:
        rows = db.execute_query(sql, binds)
        print("Success! Fetched", len(rows), "rows")
    except Exception as e:
        print("Error:", e)
        
if __name__ == '__main__':
    test_query()
