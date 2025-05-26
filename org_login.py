from admin import connect
import login
from admin import views

def org_login(org_id):
    while True:
        print('\n========== VIEW ==========')
        print('[1] Organization Members')
        print('[2] Organization Fees')
        print('[3] Back to Main Menu')
        choice = input('Enter choice: ')

        match choice:
            case '1':
                while True:
                    print('\n[1] Members of the Organization')
                    print('[2] Executive Members')
                    print('[3] Alumni Members')
                    print('[4] List of Past and Present Presidents')
                    print('[5] Back to View Menu')
                    choice1 = input('Enter choice: ')

                    match choice1:
                        case '1':
                            views.view_members_by(connect.cur, connect.conn, '`Role`', org_id)
                            connect.cur.execute("SELECT * FROM members_by_details")
                            rows = connect.cur.fetchall()

                            #Print the results
                            for row in rows:
                                print(row)

                        case '2':
                            acad_year = input("Enter academic year (e.g., 2024–2025): ")
                            views.view_executive_members(connect.cur, connect.conn, org_id, acad_year)
                            connect.cur.execute("SELECT * FROM executive_committee_members")
                            rows = connect.cur.fetchall()

                    for row in rows:
                        print(row)

                        case '5':
                            break
                        
                        case _:
                            print("Invalid choice.")
            
            case '2':
                while True:
                    print('\n[1] List of Unpaid Members')
                    print('[2] Late Payments by all Members')
                    print('[3] Highest Member/s with Unpaid Fees')
                    print('[4] Total Unpaid and Paid Fees')
                    print('[5] Back to View Menu')
                    choice2 = input('Enter choice: ')

                    match choice2:
                        case '1':
                            semester = input("Enter semester (e.g., 1st Semester): ")
                            acad_year = input("Enter academic year (e.g., 2024–2025): ")
                            views.view_unpaid_members(connect.cur, connect.conn, org_id, semester, acad_year)
                        
                        case '2':
                            semester = input("Enter semester (e.g., 1st Semester): ")
                            acad_year = input("Enter academic year (e.g., 2024–2025): ")
                            views.view_late_payments(connect.cur, connect.conn, semester, acad_year)
                        case '5':
                            break
                        
                        case _:
                            print("Invalid choice.")

            case '3':
                login.login()

            case _:
                print("Invalid choice.")
