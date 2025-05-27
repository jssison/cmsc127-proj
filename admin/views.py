import mariadb

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
                WHERE orgmem.org_id = {org_id}
                ORDER BY {order};
            """)
        except mariadb.Error as e:
            print(f'Error generating view {e}')
        
        connection.commit()
        #Notify user of view creation success
        cursor.execute("SELECT * FROM members_by_details")
        return cursor.fetchall()

# create or replace a view for viewing all members of the organization with unpaid fees
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
    
# for the function of viewing the member's specific unpaid fees (MEMBER's pov)
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

# for showing all the members in executive committee based on the chosen academic year
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

# showing the list of past and current members in position (position is specified by the user)
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
    
# for all members with late payments
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
            WHERE mpf.date_of_payment > f.due_date AND mpf.date_of_payment != '0000-00-00' AND ohm.org_id = {org_id} AND mpf.semester = '{sem}' AND mpf.academic_year = '{acad_yr}';
        """)

    except mariadb.Error as e:
        print(f'Error generating view {e}')

    connection.commit()

    cursor.execute("SELECT * FROM late_payments_view")
    return cursor.fetchall()

# shows the percentage of active and inactive members from the past n semesters
def view_percentage(cursor, connection, org_id, num_of_sems):
    try:
        #getting the last no. of semesters
        cursor.execute(f"""
            SELECT DISTINCT academic_year, semester
            FROM organization_has_member
            WHERE org_id = {org_id}
            ORDER BY academic_year DESC, semester DESC
            LIMIT {num_of_sems}
        """)
        recent_sems = cursor.fetchall()

        #for filtering all the included sems based on the input (useful for counting total members)
        acad_sem = " OR ".join(
            f"(academic_year = '{year}' AND semester = '{sem}')" for year, sem in recent_sems
        )

        cursor.execute(f"""
            CREATE OR REPLACE VIEW active_vs_inactive_percentage AS
            SELECT 
                COUNT(*) AS total_members,
                SUM(mem_status = 'Active') AS active_count,
                SUM(mem_status = 'Inactive') AS inactive_count,
                ROUND((SUM(mem_status = 'Active') / COUNT(*)) * 100, 2) AS active_percentage,
                ROUND((SUM(mem_status = 'Inactive') / COUNT(*)) * 100, 2) AS inactive_percentage
            FROM organization_has_member
            WHERE org_id = {org_id} AND ({acad_sem});
        """)

        cursor.execute("SELECT * FROM active_vs_inactive_percentage")
        return cursor.fetchall()

    except mariadb.Error as e:
        print(f'Error generating view: {e}')

    connection.commit()

# alumni as of given date
def view_alumni(cursor, connection, org_id, given_date):
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
            WHERE orgmem.mem_status = 'Alumni' AND CAST(SUBSTRING('{given_date}',1,4) as INT) >= CAST(SUBSTRING(orgmem.academic_year,1,4) AS INT) AND org.org_id = {org_id};
        """)

    except mariadb.Error as e:
        print(f'Error generating view {e}')

    connection.commit()

    cursor.execute("SELECT * FROM alumni_members")
    return cursor.fetchall()

# shows the total paid and unpaid amount of the org(total of the members' fees)
def view_total_fees(cursor, connection, org_id, given_date):
    try:
        cursor.execute(f"""
        CREATE OR REPLACE VIEW total_unpaid AS
            SELECT
                COALESCE(SUM(CASE WHEN mpf.payment_status = 'Paid' AND DATEDIFF('{given_date}', mpf.date_of_payment) >= 0
                    THEN f.amount
                    ELSE 0 END), 0) AS `Total Paid Amount`,    
                COALESCE(SUM(CASE WHEN mpf.payment_status = 'Not Paid' OR DATEDIFF('{given_date}', mpf.date_of_payment) < 0
                    THEN f.amount
                    ELSE 0 END), 0) AS `Total Unpaid Amount`
            FROM organization org
            JOIN fee f ON org.org_id = f.org_id
            JOIN member_pays_fee mpf ON f.fee_refnum = mpf.fee_refnum
            WHERE org.org_id = {org_id} AND DATEDIFF('{given_date}', f.due_date) >= 0;
        """)
    except mariadb.Error as e:
        print(f'Error generating view {e}')

    connection.commit()

    cursor.execute("SELECT * FROM total_unpaid")
    return cursor.fetchall()

# shows the member/s with highest unpaid fee or debt
def view_unpaid(cursor, connection, org_id, sem):
    try:
        cursor.execute(f"""
        CREATE OR REPLACE VIEW highest_debt AS
            SELECT mem.mem_id AS "Membership ID",
                CASE WHEN 
                    mem.mname IS NOT NULL AND mem.mname != ''
                THEN CONCAT(mem.fname, ' ', mem.mname, ' ', mem.lname)
                ELSE CONCAT(mem.fname, ' ', mem.lname)
                END AS `Full Name`,
            SUM(CASE WHEN 
                    mpf.payment_status != 'Paid' THEN f.amount 
                ELSE 0 END) AS `Unpaid Amount`
            FROM member mem
            JOIN member_pays_fee mpf ON mem.mem_id = mpf.mem_id
            JOIN fee f ON mpf.fee_refnum = f.fee_refnum
            WHERE f.org_id = {org_id} AND mpf.semester = '{sem}'
            GROUP BY mem.mem_id, mem.fname,mem.lname
            HAVING `Unpaid Amount` > 0 AND `Unpaid Amount` = (SELECT MAX(total_unpaid) FROM(SELECT mem1.mem_id, SUM(CASE WHEN 
                mpf1.payment_status != 'Paid' THEN f1.amount 
                ELSE 0 END) AS total_unpaid FROM member mem1
                JOIN member_pays_fee mpf1 ON mem1.mem_id = mpf1.mem_id
                JOIN fee f1 ON mpf1.fee_refnum = f1.fee_refnum
                WHERE f1.org_id = {org_id} AND mpf1.semester = '{sem}'
                GROUP BY mem1.mem_id
            ) AS high_debt
        );
        """)
    except mariadb.Error as e:
        print(f'Error generating view {e}')

    connection.commit()

    cursor.execute("SELECT * FROM highest_debt")
    return cursor.fetchall()
