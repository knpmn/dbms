import oracledb
import config
import re

def drop_tables(cursor):
    drop_stmt = """
    BEGIN
      FOR t IN (
        SELECT table_name FROM user_tables
        WHERE table_name IN (
          'BP','PENALTIES','YEARLY_BONUS','BONUS_POINTS',
          'ATTENDANCE','EMPLOYEES','POSITIONS','DEPARTMENTS',
          'USERS','ROLES'
        )
      ) LOOP
        EXECUTE IMMEDIATE 'DROP TABLE "' || t.table_name || '" CASCADE CONSTRAINTS';
      END LOOP;
    END;
    """
    try:
        cursor.execute(drop_stmt)
        print("Dropped old tables.")
    except Exception as e:
        print("Drop encountered an issue (safe to ignore if first run):", e)

def run_setup():
    dsn = f"{config.DB_HOST}:{config.DB_PORT}/{config.DB_SERVICE}"
    print(f"Connecting to {config.DB_USER}@{dsn} ...")
    try:
        with oracledb.connect(user=config.DB_USER, password=config.DB_PASSWORD, dsn=dsn) as connection:
            with connection.cursor() as cursor:
                drop_tables(cursor)

                with open('schema.sql', 'r', encoding='utf-8') as f:
                    content = f.read()

                # Find all logical CREATE TABLE and INSERT statements separately
                creates = re.findall(r'CREATE TABLE \w+\s*\([\s\S]*?\);', content)
                for stmt in creates:
                    sql = stmt.rstrip(';')
                    print("Executing:", sql.strip().split('\n')[0])
                    cursor.execute(sql)
                
                inserts = re.findall(r'INSERT INTO [\s\S]*?\([\s\S]*?\)\s*VALUES\s*\([\s\S]*?\);', content)
                for stmt in inserts:
                    sql = stmt.rstrip(';')
                    print("Executing:", sql.strip().split('\n')[0][:60] + "...")
                    cursor.execute(sql)

                connection.commit()
                print("Database tables and seed data setup successfully.")
    except Exception as e:
        print("Database setup failed.")
        print(f"Error: {e}")

if __name__ == '__main__':
    run_setup()
