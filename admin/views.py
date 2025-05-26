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
        cursor.execute("SELECT * FROM members_by_details")
        return cursor.fetchall()

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
        WHERE mpf.payment_status = 'Not Paid' AND ohm.org_id = {org_id} AND mpf.semester = '{sem}' AND mpf.academic_year = '{acad_yr}';
        """)

    except mariadb.Error as e:
        print(f'Error generating view {e}')

    connection.commit()

    cursor.execute("SELECT * FROM member_with_unpaid_membership_fees")
    return cursor.fetchall()
#3
def view_unpaid_fees(cursor, connection, member):
    try:
        cursor.execute(f"""
        CREATE OR REPLACE VIEW unpaid_member_fees AS	
            SELECT fee.fee_refnum AS `Fee reference number`, 
                fee.category AS `Category`, 
                fee.due_date AS `Due date`, 
                fee.amount AS `Amount`, 
                org.org_name AS `Organization Name`, 
                mem_fee.academic_year AS `Academic Year`, 
                mem_fee.semester AS `Semester`, 
                mem_fee.payment_status AS `Payment Status` 
            FROM  member AS mem JOIN member_pays_fee AS mem_fee 
            ON mem.mem_id = mem_fee.mem_id
            JOIN fee ON mem_fee.fee_refnum = fee.fee_refnum
            JOIN organization AS org
            ON fee.org_id = org.org_id
            WHERE mem_fee.payment_status = 'Not Paid';
        """)
    except mariadb.Error as e:
        print(f'Error generating view {e}')

    connection.commit()

    cursor.execute("SELECT * FROM unpaid_member_fees")
    return cursor.fetchall()

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
        
    except mariadb.Error as e:
        print(f'Error generating view {e}')

    connection.commit()

    cursor.execute("SELECT * FROM executive_committee_members")
    return cursor.fetchall()

#5
def view_role(cursor, connection, role, org_id):
    try:
        cursor.execute(f"""
        CREATE OR REPLACE VIEW presidents AS
            SELECT mem.mem_id AS `Membership ID`,
            CASE
            WHEN mem.mname IS NOT NULL AND mem.mname != ''
            THEN CONCAT(mem.fname, ' ', mem.mname, ' ', mem.lname)
            ELSE CONCAT(mem.fname, ' ', mem.lname)
            END AS `Full Name`,  
                orgmem.org_role AS `Role`,
                org.org_name AS `Organization name`,
                orgmem.academic_year AS `Academic year`
            FROM member AS mem JOIN organization_has_member AS orgmem
            ON mem.mem_id = orgmem.mem_id
            JOIN organization AS org
            ON orgmem.org_id = org.org_id
            WHERE orgmem.org_role = '{role}' AND orgmem.org_id = {org_id}
            ORDER BY orgmem.academic_year DESC;
        """)
    except mariadb.Error as e:
        print(f'Error generating view {e}')

    connection.commit()
    #Notify user of view creation success

    cursor.execute("SELECT * FROM presidents")
    return cursor.fetchall()
#6
def view_late_payments(cursor, connection, org_id, sem, acad_yr):
    try:
        cursor.execute(f"""
        CREATE OR REPLACE VIEW late_payments_view AS
            SELECT 
                m.mem_id AS `Membership ID`,
                CONCAT(m.fname, ' ', IFNULL(m.mname, ''), IF(m.mname IS NOT NULL, ' ', ''), m.lname) AS `Full Name`,
                m.degprog AS `Degree Program`,
                m.gender AS `Gender`,
                ohm.org_id AS `Organization ID`,
                mpf.academic_year AS `Academic Year`,
                mpf.semester AS `Semester`,
                f.fee_refnum AS `Fee Reference`,
                f.due_date AS `Due Date`,
                mpf.date_of_payment AS `Date of Payment`,
                mpf.payment_status AS `Payment Status`
            FROM member m
            JOIN organization_has_member ohm
            ON m.mem_id = ohm.mem_id
            JOIN member_pays_fee mpf
            ON m.mem_id = mpf.mem_id
            JOIN fee f
            ON mpf.fee_refnum = f.fee_refnum
            WHERE mpf.date_of_payment > f.due_date AND ohm.org_id = {org_id} AND mpf.semester = '{sem}' AND mpf.academic_year = '{acad_yr}';
        """)
    except mariadb.Error as e:
        print(f'Error generating view {e}')

    connection.commit()

    cursor.execute("SELECT * FROM late_payments_view")
    return cursor.fetchall()

#7
def view_percentage(cursor, connection, org, num_of_sems):
    try:
        cursor.execute(f"""
        CREATE OR REPLACE VIEW active_vs_inactive_percentage AS 
        SELECT academic_year,
            semester,
            COUNT(*) AS total_members,
            SUM(mem_status = 'Active') AS active_count,
            SUM(mem_status = 'Inactive') AS inactive_count,
            ROUND((SUM(mem_status = 'Active') / COUNT(*)) * 100, 2) AS active_percentage,
            ROUND((SUM(mem_status = 'Inactive') / COUNT(*)) * 100, 2) AS inactive_percentage
        FROM organization_has_member
        WHERE organization_id = organization_id
        GROUP BY academic_year, semester
        ORDER BY academic_year DESC, semester DESC;
        """)
    except mariadb.Error as e:
        print(f'Error generating view {e}')

    connection.commit()

    cursor.execute("SELECT * FROM active_vs_inactive_percentage")
    return cursor.fetchall()

#8
def view_alumni(cursor, connection, org, given_date):
    try:
        cursor.execute(f"""
        CREATE OR REPLACE VIEW alumni_members AS
            SELECT mem.mem_id AS `Membership ID`,
            CASE WHEN 
                mem.mname IS NOT NULL AND mem.mname != ''
            THEN CONCAT(mem.fname, ' ', mem.mname, ' ', mem.lname)
            ELSE CONCAT(mem.fname, ' ', mem.lname)
            END AS `Full Name`,
                org.org_name AS `Organization Name`
            FROM member AS mem JOIN organization_has_member AS orgmem 
            ON mem.mem_id = orgmem.mem_id 
            JOIN organization AS org 
            ON orgmem.org_id = org.org_id 
            WHERE orgmem.mem_status = 'Alumni';
        """)
    except mariadb.Error as e:
        print(f'Error generating view {e}')

    connection.commit()

    cursor.execute("SELECT * FROM alumni_members")
    return cursor.fetchall()


#9
def view_total_fees(cursor, connection, org, given_date):
    try:
        cursor.execute(f"""
        CREATE OR REPLACE VIEW total_unpaid AS
            SELECT o.org_name,
                Total Paid Amount (before or on today)
                COALESCE(SUM(
                    CASE WHEN mpf.payment_status = 'Paid' AND mpf.date_of_payment <= CURRENT_DATE THEN f.amount
                    ELSE 0 END), 0) AS total_paid_amount,    
                        COALESCE(SUM(
                            CASE WHEN f.due_date <= CURRENT_DATE AND 
                                (mpf.payment_status = 'Not Paid' OR mpf.date_of_payment > CURRENT_DATE)
                            THEN f.amount
                            ELSE 0 END), 0) AS total_unpaid_amount
            FROM organization o
            JOIN fee f ON o.org_id = f.org_id
            JOIN member_pays_fee mpf ON f.fee_refnum = mpf.fee_refnum
            GROUP BY o.org_name;
        """)
    except mariadb.Error as e:
        print(f'Error generating view {e}')

    connection.commit()

    cursor.execute("SELECT * FROM total_unpaid")
    return cursor.fetchall()

#10
def view_unpaid(cursor, connection, sem, acad_yr):
    try:
        cursor.execute(f"""
        CREATE OR REPLACE VIEW highest_debt 
            SELECT m.mem_id,
                m.fname,
                m.lname,
            SUM(CASE
            WHEN mpf.payment_status != 'Paid' THEN f.amount ELSE 0 END) AS unpaid_amount
            FROM member m
            JOIN member_pays_fee mpf ON m.mem_id = mpf.mem_id
            JOIN fee f ON mpf.fee_refnum = f.fee_refnum
            WHERE f.org_id = given_organization_id
            And mpf.semester = given_semester
            GROUP BY m.mem_id, m.fname,m.lname
            ORDER BY unpaid_amount DESC	;
        """)
    except mariadb.Error as e:
        print(f'Error generating view {e}')

    connection.commit()

    cursor.execute("SELECT * FROM highest_debt")
    return cursor.fetchall()
