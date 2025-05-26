import mariadb

#TODO: Implement views 2-9

#NOTES: (param passing)
# cur (in connect.py) is the same as cursor (in functions)
# conn (in connect.py) is the same as connection (in functions)

#View members by the specified ordering type
def view_members_by(cursor, connection, order, org_id):
    #Allowable ordering types
    ordering_types = ['`Role`', '`Status`', '`Gender`', '`Degree Program`', '`Batch year`', '`Committee`']

    if(org_id is None):
        print('Organization ID is required to create the view.')
        return
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
                WHERE orgmem.org_id = ?
                ORDER BY {order};
            """, (org_id,))
        except mariadb.Error as e:
            print(f'Error generating view {e}')
        
        connection.commit()
        #Notify user of view creation success
        print('Successfully created desired view.')
    else:
        #Else print a message to notify user
        print('Invalid ordering type.')

#2
def view_unpaid_members(cursor, connection, org_id, sem, acad_yr):
    try:
        cursor.execute(f"""
        CREATE OR REPLACE VIEW member_with_unpaid_membership_fees AS
        SELECT 
            m.mem_id AS `Membership ID`,
            CONCAT(m.fname, ' ', IFNULL(m.mname, ''), IF(m.mname IS NOT NULL, ' ', ''), m.lname) AS `Full Name`,
            m.degprog AS `Degree Program`,
            m.gender AS `Gender`,
            ohm.org_id AS `Organization`,
            mpf.academic_year AS `Academic Year`,
            mpf.semester AS `Semester`
        FROM member m
        JOIN organization_has_member ohm
            ON m.mem_id = ohm.mem_id
        JOIN member_pays_fee mpf
            ON m.mem_id = mpf.mem_id
        WHERE mpf.payment_status = 'Not Paid' AND ohm.org_id = ? AND mpf.semester = ? AND mpf.academic_year = ?;
        """, (org_id, sem, acad_yr))

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
def view_executive_members(cursor, connection, org_id, acad_yr):
    try:
        cursor.execute(f"""
        CREATE OR REPLACE VIEW executive_committee_members AS
            SELECT mem.mem_id AS `Membership ID`,
            CASE
                WHEN mem.mname IS NOT NULL AND mem.mname != ''
                    THEN CONCAT(mem.fname, ' ', mem.mname, ' ', mem.lname)
                ELSE CONCAT(mem.fname, ' ', mem.lname)
            END AS `Full Name`, 
            org.org_name AS `Organization name`, 
            orgmem.academic_year AS `Academic year`
            FROM member AS mem JOIN organization_has_member AS orgmem
            ON mem.mem_id = orgmem.mem_id 
            JOIN organization AS org 
            ON orgmem.org_id = org.org_id
            WHERE orgmem.committee = 'Executive' AND org.org_id = {org_id} AND orgmem.academic_year = '{acad_yr}';
        """)

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
