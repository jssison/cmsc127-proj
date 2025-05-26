import mariadb
import sys
from . import create
from . import populate
from . import views

#NOTES:
# use cur.execute(<query>) to run SQL queries
# use conn.commit() to commit changes to the database
# remember to edit in credentials to connect

# Connect to mariadb
try:
    # Connection credentials
    # Connect to mariadb via conn
    conn = mariadb.connect(
        user = 'root',          #Change if desired
        password = 'cootart99',          #Password for desired user
        host = 'localhost',
        database = 'proj'           #Insert 127 database here
    )
except mariadb.Error as e:
    print(f'Error connect to MariaDB: {e}')
    sys.exit(1)

#Get cursor
cur = conn.cursor()

#Create tables
create.create_org(cur, conn)
create.create_mem(cur, conn)
create.create_fee(cur, conn)
create.create_orghasmem(cur, conn)
create.create_mempaysfee(cur, conn)

#Populate database
populate.insert_to_org(cur, conn)
populate.insert_to_mem(cur, conn)
populate.insert_to_fee(cur, conn)
populate.insert_to_orghasmem(cur, conn)
populate.insert_to_mempaysfee(cur, conn)

#Views Testing
# views.view_members_by(cur, conn, '`Gender`')

#Commit changes
conn.commit()

#Sucess message
print('Successfully created and populated tables.')