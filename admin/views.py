import mariadb

#TODO: Implement views 2-9

#NOTES: (param passing)
# cur (in connect.py) is the same as cursor (in functions)
# conn (in connect.py) is the same as connection (in functions)

#View members by the specified ordering type
def view_members_by(cursor, connection, order):
    #Allowable ordering types
    ordering_types = ['`Role`', '`Status`', '`Gender`', '`Degree Program`', '`Batch year`', '`Committee`']

    #Only create a view if ordering type selected is valid
    if(order in ordering_types):
        try:
            cursor.execute(f"""
            CREATE OR REPLACE VIEW members_by_details AS
                SELECT mem.mem_id AS `Membership ID`, 
                CASE
                    WHEN mem.mname IS NOT NULL AND mem.mname != ''
                        THEN CONCAT(mem.fname, ' ', mem.mname, ' ', mem.lname)
                    ELSE CONCAT(mem.fname, ' ', mem.lname)
                END AS `Full Name`, 
                orgmem.org_role AS `Role`,
                orgmem.mem_status AS `Status`, 
                mem.gender AS `Gender`, 
                mem.degprog AS `Degree Program`, 
                orgmem.batch_year AS `Batch year`, 
                orgmem.committee AS `Committee`
                FROM member AS mem JOIN organization_has_member AS orgmem ON 
                mem.mem_id = orgmem.mem_id
                ORDER BY {order};
            """)
        except mariadb.Error as e:
            print(f'Error generating view {e}')
        
        connection.commit()
        #Notify user of view creation success
        print('Successfully created desired view.')
    else:
        #Else print a message to notify user
        print('Invalid ordering type.')

#2
def view_unpaid_members(cursor, connection, sem, acad_yr):
    try:
        cursor.execute()
    except mariadb.Error as e:
        print(f'Error generating view {e}')

    connection.commit()

#3
def view_unpaid_fees(cursor, connection, member):
    try:
        cursor.execute()
    except mariadb.Error as e:
        print(f'Error generating view {e}')

    connection.commit()

#4
def view_executive_members(cursor, connection, org, sem, acad_yr):
    try:
        cursor.execute()
    except mariadb.Error as e:
        print(f'Error generating view {e}')

    connection.commit()

#5
def view_role(cursor, connection, role, org):
    try:
        cursor.execute()
    except mariadb.Error as e:
        print(f'Error generating view {e}')

    connection.commit()

#6
def view_late_payments(cursor, connection, org, sem, acad_yr):
    try:
        cursor.execute()
    except mariadb.Error as e:
        print(f'Error generating view {e}')

    connection.commit()

#7
def view_percentage(cursor, connection, org, num_of_sems):
    try:
        cursor.execute()
    except mariadb.Error as e:
        print(f'Error generating view {e}')

    connection.commit()

#8
def view_alumni(cursor, connection, org, given_date):
    try:
        cursor.execute()
    except mariadb.Error as e:
        print(f'Error generating view {e}')

    connection.commit()

#9
def view_total_fees(cursor, connection, org, given_date):
    try:
        cursor.execute()
    except mariadb.Error as e:
        print(f'Error generating view {e}')

    connection.commit()

#10
def view_unpaid(cursor, connection, sem, acad_yr):
    try:
        cursor.execute()
    except mariadb.Error as e:
        print(f'Error generating view {e}')

    connection.commit()