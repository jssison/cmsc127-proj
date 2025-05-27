from admin import connect

#Get member rows from ohm x member
def get_member(org_id):
    print("\n========== Edit a Member ==========")
    mem_id = input("Enter the Member ID to edit: ")
    connect.cur.execute("SELECT * FROM organization_has_member ohm JOIN member m ON ohm.mem_id = m.mem_id WHERE ohm.mem_id = ? AND ohm.org_id = ?", (mem_id, org_id))
    member = connect.cur.fetchone()

    return member, mem_id

#Get fee rows from mpf x fee
def get_fee(org_id, mem_id):
    fee_refnum = input("Enter the Fee Reference Number to edit: ")
    connect.cur.execute("""
        SELECT * FROM member_pays_fee mpf JOIN fee f ON mpf.fee_refnum = f.fee_refnum
        WHERE mpf.mem_id = ? AND f.org_id = ? AND mpf.fee_refnum = ?""", (mem_id, org_id, fee_refnum))
    fee = connect.cur.fetchone()

    return fee, fee_refnum

#Add fee for a member
def add_mem_fees(org_id):
    member, mem_id = get_member(org_id)
    if member:
        print(f"\n========== Add Fee for Member {mem_id} ==========")
        amount = input("Enter Amount: ")
        due_date = input("Enter Due Date (YYYY-MM-DD): ")
        category = input("Enter Category: ")
        sem = input("Enter Semester (e.g., 1st Semester, 2nd Semester): ")

        #Check if the semester is valid
        if sem not in ['1st Semester', '2nd Semester']:
            print("Invalid semester. Please enter '1st Semester' or '2nd Semester'.")
        else:
            academic_year = input("Enter Academic Year (e.g., 2024-2025): ")
            #Insert into fee table
            connect.cur.execute("""
                INSERT INTO fee ( org_id, amount, due_date, category)
                VALUES (?, ?, STR_TO_DATE(?, '%Y-%m-%d'), ?)
            """, (org_id, amount, due_date, category))
            
            connect.conn.commit()

            #Get the last inserted fee_refnum
            connect.cur.execute("SELECT LAST_INSERT_ID()")
            fee_refnum = connect.cur.fetchone()[0]

            #Insert into member_pays_fee table
            connect.cur.execute("""
                INSERT INTO member_pays_fee (mem_id, fee_refnum, academic_year, semester, date_of_payment, payment_status)
                VALUES (?, ?, ?, ?, NULL, 'Not Paid')
            """, (mem_id, fee_refnum, sem, academic_year))

            connect.conn.commit()
            print(f"Fee {fee_refnum} added for member {mem_id} successfully.")
    else:
        print('No such member found under this organization.')    

#Edit fee for a member
def edit_mem_fees(org_id):
    member, mem_id = get_member(org_id)

    if member:
        fee, fee_refnum = get_fee(org_id, mem_id)
        if fee:
            print(f"\n========== Edit Fee Details ==========")
            print(f"[1] Edit Status and Date of Payment")
            print(f"[2] Edit Amount")
            print(f"[3] Edit Due Date")
            print(f"[4] Edit Category")
            print(f"[5] Back to Edit Member Menu")
            choice = input("Enter choice: ")
        
            match choice:
                # Edit Status and Date of Payment
                case '1':
                    date_of_payment = input("Enter new date of payment (YYYY-MM-DD): ")
                    new_status = input("Enter new payment status (Paid/Not Paid): ")

                    # Validate payment status
                    if new_status not in ['Paid', 'Not Paid']:
                        print("Invalid payment status. Please enter 'Paid' or 'Not Paid'.")
                    else:
                        connect.cur.execute("""
                            UPDATE member_pays_fee
                            SET date_of_payment = STR_TO_DATE(?, '%Y-%m-%d'), payment_status = ?
                            WHERE mem_id = ? AND fee_refnum = ?""",
                            (date_of_payment, new_status, mem_id, fee_refnum))  
                        connect.conn.commit()
                        print(f"Fee {fee_refnum} for member {mem_id} updated successfully.")
                    
                # Edit Amount
                case '2':
                    new_amount = input("Enter new amount: ")
                    # Validate if the new amount is a valid number
                    try:
                        new_amount = float(new_amount)
                        connect.cur.execute("""
                            UPDATE fee
                            SET amount = ?
                            WHERE fee_refnum = ? AND org_id = ?""", (new_amount, fee_refnum, org_id))
                        connect.conn.commit()
                        print(f"Fee {fee_refnum} amount updated successfully.")
                    except ValueError:
                        print("Invalid amount. Please enter a valid number.")
                
                # Edit Due Date
                case '3':
                    new_due_date = input("Enter new due date (YYYY-MM-DD): ")
                    connect.cur.execute("""
                        UPDATE fee
                        SET due_date = STR_TO_DATE(?, '%Y-%m-%d')
                        WHERE fee_refnum = ? AND org_id = ?""", (new_due_date, fee_refnum, org_id))
                    connect.conn.commit()
                    print(f"Fee {fee_refnum} due date updated successfully.")
                
                # Edit Category
                case '4':
                    new_category = input("Enter new category: ")
                    connect.cur.execute("""
                        UPDATE fee
                        SET category = ?
                        WHERE fee_refnum = ? AND org_id = ?""", (new_category, fee_refnum, org_id))
                    connect.conn.commit()
                    print(f"Fee {fee_refnum} category updated successfully.")
                    
                case '5':
                    return
                case _:
                    print("Invalid choice. Please try again.")
                    

        else:
            print("No fee found for this member under this organization.")
    else:
        print('No such member found under this organization.')

# Edit organization membership details for a member
def edit_org_membership(org_id):
    member, mem_id = get_member(org_id)

    if member:
        # Loop to edit organization membership details
        while True:
            print(f"\n========== Edit Member Details ==========")
            print(f"[1] Edit Committee")
            print(f"[2] Edit Role")
            print(f"[3] Edit Status")
            print(f"[4] Edit Academic Year")
            print(f"[5] Edit Semester")
            print(f"[6] Edit Batch Year")
            print(f"[7] Edit Batch Name")
            print(f"[8] Back to Edit Member Menu")
            choice = input("Enter choice: ")

            match choice:
                # Edit Committee
                case '1':
                    new_committee = input("Enter new committee: ")
                    connect.cur.execute("""
                        UPDATE organization_has_member
                        SET committee = ?
                        WHERE mem_id = ? AND org_id = ?""", (new_committee, mem_id, org_id))
                    connect.conn.commit()
                    print(f"Member {mem_id} committee updated successfully.")

                # Edit Role
                case '2':
                    new_role = input("Enter new role: ")
                    connect.cur.execute("""
                        UPDATE organization_has_member
                        SET org_role = ?
                        WHERE mem_id = ? AND org_id = ?""", (new_role, mem_id, org_id))
                    connect.conn.commit()
                    print(f"Member {mem_id} role updated successfully.")
                
                # Edit Status
                case '3':
                    new_status = input("Enter new status (Active/Inactive/Alumni/Suspended): ")
                    if(new_status not in ['Active', 'Inactive', 'Alumni', 'Suspended']):
                        print("Invalid status.")
                    else:
                        connect.cur.execute("""
                            UPDATE organization_has_member
                            SET mem_status = ?
                            WHERE mem_id = ? AND org_id = ?""", (new_status, mem_id, org_id))
                        connect.conn.commit()
                        print(f"Member {mem_id} status updated successfully.")
                    
                # Edit Academic Year
                case '4':
                    new_academic_year = input("Enter new academic year (e.g., 2024-2025): ")
                    connect.cur.execute("""
                        UPDATE organization_has_member
                        SET academic_year = ?
                        WHERE mem_id = ? AND org_id = ?""", (new_academic_year, mem_id, org_id))
                    connect.conn.commit()
                    print(f"Member {mem_id} academic year updated successfully.")

                # Edit Semester
                case '5':
                    new_semester = input("Enter new semester (e.g 1st Semester): ")
                    if new_semester.trim() not in ['1st Semester', '2nd Semester']:
                        print("Invalid semester. Please enter '1st Semester' or '2nd Semester'.")
                    else:
                        connect.cur.execute("""
                            UPDATE organization_has_member
                            SET semester = ?
                            WHERE mem_id = ? AND org_id = ?""", (new_semester.trim(), mem_id, org_id))
                        connect.conn.commit()
                        print(f"Member {mem_id} semester updated successfully.")
                
                # Edit Batch Year
                case '6':
                    new_batch_year = input("Enter new batch year: ")
                    connect.cur.execute("""
                        UPDATE organization_has_member
                        SET batch_year = ?
                        WHERE mem_id = ? AND org_id = ?""", (new_batch_year, mem_id, org_id))
                    connect.conn.commit()
                    print(f"Member {mem_id} batch year updated successfully.")

                # Edit Batch Name
                case '7':
                    new_batch_name = input("Enter new batch name: ")
                    if (int(new_batch_name) < 0 or int(new_batch_name) > 9999):
                        print("Invalid batch name. Please enter a valid year (e.g., 2024).")
                    else:
                        connect.cur.execute("""
                            UPDATE organization_has_member
                            SET batch_name = ?
                            WHERE mem_id = ? AND org_id = ?""", (int(new_batch_name), mem_id, org_id))
                        connect.conn.commit()
                        print(f"Member {mem_id} batch name updated successfully.")
                case '8':
                    return
                case _:
                    print("Invalid choice. Please try again.")

    else:
        print('No such member found under this organization.')

# Edit member details
def edit_member_details(org_id):
    member, mem_id = get_member(org_id)

    if member:
        #Print member details
        if(member[13] is None):
            middle = ' '
        else:
            middle = ' ' + member[13] + ' '
        print(f"Current details for Member ID {mem_id}:")
        print(f"Name: {member[12]}{middle}{member[14]}")
        print(f"Username: {member[10]}")
        print(f"Degree Program: {member[15]}")
        print(f"Gender: {member[16]}")

        # Loop to edit member details
        while True:
            print(f"\n========== Edit Member Details ==========")
            print(f"[1] Edit Name")
            print(f"[2] Edit Username")
            print(f"[3] Edit Degree Program")
            print(f"[4] Edit Gender")
            print(f"[5] Back to Edit Member Menu")
            choice = input("Enter choice: ")

            match choice:
                # Edit Name
                case '1':
                    new_fname = input("Enter new first name: ")
                    new_mname = input("Enter new middle name (press Enter to skip): ")
                    new_lname = input("Enter new last name: ")
                    connect.cur.execute("""
                        UPDATE member SET fname = ?, mname = ?, lname = ?
                        WHERE mem_id = ? """, (new_fname, new_mname if new_mname else None, new_lname, mem_id))
                    connect.conn.commit()
                    
                    print(f"Member {mem_id} name updated successfully.")
                
                # Edit Username
                case '2':
                    new_username = input("Enter new username: ")
                    connect.cur.execute("""
                        UPDATE member SET mem_uname = ? 
                        WHERE mem_id = ? """, (new_username, mem_id))
                    connect.conn.commit()
                    print(f"Member {mem_id} username updated successfully.")

                # Edit Degree Program
                case '3':
                    new_degprog = input("Enter new degree program: ")
                    connect.cur.execute("""
                        UPDATE member SET degprog = ? 
                        WHERE mem_id = ? """, (new_degprog, mem_id))
                    connect.conn.commit()
                    print(f"Member {mem_id} degree program updated successfully.")

                # Edit Gender   
                case '4':
                    new_gender = input('Enter new gender (M/F): ').upper()
                    if(new_gender not in ['M', 'F']):
                        print("Invalid gender.")
                    else:
                        connect.cur.execute("""
                            UPDATE member SET gender = ?
                            WHERE mem_id = ? """, (new_gender, mem_id))
                        connect.conn.commit()
                        print(f"Member {mem_id} gender updated successfully.")
                    
                case '5':
                    return
                case _:
                    print("Invalid choice. Please try again.")
                    continue

    else:
        print("No such member found.")
        return
    

def edit_member_menu(org_id):
    #Main menu for editing member details
    while True:
        print("\n========== EDIT MEMBER MENU ==========")
        print("[1] Edit Member Details")
        print("[2] Edit Organization Membership")
        print("[3] Add Member Fees")
        print("[4] Edit Member Fees")
        print("[5] Back to Main Menu")
        choice = input("Enter choice: ")

        match choice:
            case '1':
                edit_member_details(org_id)
            case '2':
                edit_org_membership(org_id)
            case '3':
                add_mem_fees(org_id)
            case '4':
                edit_mem_fees(org_id)
            case '5':
                return
            case _:
                print("Invalid choice. Please try again.")
    