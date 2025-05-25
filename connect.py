import mariadb
import sys

# Connect to mariadb
try:
    # Credentials
    conn = mariadb.connect(
        user = 'root',
        password = '',
        host = 'localhost',
        database = ''
    )
except mariadb.Error as e:
    print(f'Error connect to MariaDB: {e}')
    sys.exit(1)

#Get cursor
cur = conn.cursor()
print(conn)
print(cur)