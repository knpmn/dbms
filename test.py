import oracledb

connection = oracledb.connect(
    user="system",
    password="minecaft",
    dsn="localhost:1521/xe"
)

cursor = connection.cursor()
cursor.execute("SELECT 'connected!' FROM dual")
print(cursor.fetchone())