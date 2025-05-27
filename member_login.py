from admin import connect

def member_login(mem_id):
    # First: display the member and org details (as before)
    connect.cur.execute("""
        SELECT 
            m.fname, m.mname, m.lname, m.degprog, m.gender,
            o.org_name,
            ohm.committee, ohm.semester, ohm.batch_name, ohm.mem_status, ohm.batch_year
        FROM member m
        JOIN organization_has_member ohm ON m.mem_id = ohm.mem_id
        JOIN organization o ON ohm.org_id = o.org_id
        WHERE m.mem_id = ?
    """, (mem_id,))
    
    rows = connect.cur.fetchall()

    if rows:
        print("\n========== Member Dashboard ==========")
        for row in rows:
            fname, mname, lname, degprog, gender, org_name, committee, semester, batch_name, mem_status, batch_year = row
            full_name = f"{fname} {mname + ' ' if mname else ''}{lname}"
            print(f"Name         : {full_name}")
            print(f"Degree Prog  : {degprog}")
            print(f"Gender       : {gender}")
            print(f"Org Name     : {org_name}")
            print(f"Committee    : {committee}")
            print(f"Semester     : {semester}")
            print(f"Batch Name   : {batch_name}")
            print(f"Member Status: {mem_status}")
            print(f"Batch Year   : {batch_year}")
            print("-" * 40)

        # use view
        try:
            connect.cur.execute(f"""
                CREATE OR REPLACE VIEW unpaid_member_fees AS
                SELECT fee.fee_refnum AS `Fee reference number`,
                    fee.category AS `Category`,
                    fee.due_date AS `Due date`,
                    fee.amount AS `Amount`,
                    org.org_name AS `Organization Name`,
                    mem_fee.academic_year AS `Academic Year`,
                    mem_fee.semester AS `Semester`,
                    mem_fee.payment_status AS `Payment Status`
                FROM member mem
                JOIN member_pays_fee mem_fee ON mem.mem_id = mem_fee.mem_id
                JOIN fee ON mem_fee.fee_refnum = fee.fee_refnum
                JOIN organization org ON fee.org_id = org.org_id
                WHERE mem.mem_id = '{mem_id}' AND mem_fee.payment_status = 'Not Paid';
            """)
            connect.conn.commit()

            connect.cur.execute("SELECT * FROM unpaid_member_fees")
            unpaid_fees = connect.cur.fetchall()

            if unpaid_fees:
                print("\n📌 Unpaid Fees:")
                total = 0
                for fee in unpaid_fees:
                    ref, cat, due, amt, org, acad_yr, sem, status = fee
                    print(f"{cat} - ₱{amt} | Due: {due} | Org: {org} | AY: {acad_yr}, {sem}")
                    total += amt
                print(f"\n Total Unpaid Fees: ₱{total}")
            else:
                print("\nYehey! You have no unpaid fees!")

        except Exception as e:
            print(f"Error displaying unpaid fees: {e}")
    else:
        print("\nNo membership or organization data found.")
