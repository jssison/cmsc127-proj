from admin import connect

def add_member(org_id):
    print("\n========== Add a New Member ==========")

    try:
        # Get member details
        mem_id = input("Enter Member ID: ")
        username = input("Username: ")
        password = input("Password: ")
        fname = input("First name: ")
        mname = input("Middle name (press Enter to skip): ")
        lname = input("Last name: ")
        degprog = input("Degree Program (e.g BSSTAT): ")
        gender = input("Gender (M/F): ").upper()

        # Insert into member
        connect.cur.execute("""
            INSERT INTO member (mem_id, mem_uname, mem_pword, fname, mname, lname, degprog, gender)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (mem_id, username, password, fname, mname if mname else None, lname, degprog, gender))

        # Org member details
        academic_year = input("Academic Year (e.g., 2024-2025): ")
        semester = input("Semester (e.g 1st Semester): ")
        committee = input("Committee: ")
        org_role = input("Role: ")
        batch_year = input("Batch Year: ")
        batch_name = input("Batch Name: ")
        mem_status = input("Status (Active/Inactive/Alumni/Suspended): ")

        # Insert into organization_has_member
        connect.cur.execute("""
            INSERT INTO organization_has_member (
                org_id, mem_id, academic_year, committee,
                semester, org_role, batch_year, batch_name, mem_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (org_id, mem_id, academic_year, committee, semester, org_role, batch_year, batch_name, mem_status))

        
        #Add fee obligations for this member based on active fees
        #connect.cur.execute("SELECT fee_refnum, due_date FROM fee WHERE org_id = ?", (org_id,))
        #fees = connect.cur.fetchall()

        #for fee_ref, due_date in fees:
        #    connect.cur.execute("""
        #        INSERT INTO member_pays_fee (
        #            mem_id, fee_refnum, academic_year, semester,
        #            date_of_payment, payment_status
        #        )
        #        VALUES (?, ?, ?, ?, NULL, 'Not Paid')
         #   """, (mem_id, fee_ref, academic_year, semester))
        #'''

        connect.conn.commit()
        print(f"Member {fname} {lname} has been added successfully.")

    except Exception as e:
        print(f"Error adding member: {e}")
