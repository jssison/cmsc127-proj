import mariadb
import sys
import create
import populate

# Connect to mariadb
try:
    # Credentials
    conn = mariadb.connect(
        user = 'root',          #Change if desired
        password = '', #Password for desired user
        host = 'localhost',
        database = ''       #Insert 127 database here
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

#Commit changes
conn.commit()

print('Successfully created and populated tables.')