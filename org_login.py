from admin import connect
import login
from admin import views

#Printing of rows
def print_rows(rows):
    for row in rows:
        print(row)

#Format str to date
def format_date(date_str):
    connect.cur.execute("SELECT DATE_FORMAT(STR_TO_DATE(?, '%Y-%m-%d'), '%Y-%m-%d')", (date_str,))
    result = connect.cur.fetchone()
    if result:
        return result[0]
    return None

#Format str to include backticks
def format_str(s):
    return f"`{s.strip().replace('`', '')}`"

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
                    print('[4] List of Past and Present in Position')
                    print('[5] Percentage of active vs inactive members')
                    print('[6] Back to View Menu')
                    choice1 = input('Enter choice: ')

                    match choice1:
                        case '1':
                            rows = views.view_members_by(connect.cur, connect.conn, '`Role`', org_id)
                            #Print the results
                            print_rows(rows)

                        case '2':
                            acad_year = input("Enter academic year (e.g., 2024–2025): ")
                            connect.cur.execute("SELECT * FROM executive_committee_members")
                            rows = views.view_executive_members(connect.cur, connect.conn, org_id, acad_year)

                            print_rows(rows)

                        case '3':
                            given_date = input("Enter date (YYYY-MM-DD): ")
                            formatted_date = format_date(given_date)
                            if not formatted_date:
                                print("Invalid date format. Please use YYYY-MM-DD.")
                                continue
                            rows = views.view_alumni(connect.cur, connect.conn, org_id, formatted_date)
                            print_rows(rows)

                        case '4':
                            role = format_str(input("Enter role: "))
                            rows = views.view_role(connect.cur, connect.conn, role, org_id)

                            print_rows(rows)

                        case '5':
                            semester = input("Enter semester (e.g., 1st Semester): ")
                            acad_year = input("Enter academic year (e.g., 2024–2025): ")
                            rows = views.view_active_inactive(connect.cur, connect.conn, org_id, semester, acad_year)
                            
                            print_rows(rows)

                        case '6':
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
                            rows = views.view_unpaid_members(connect.cur, connect.conn, org_id, semester, acad_year)

                            print_rows(rows)

                        case '2':
                            semester = input("Enter semester (e.g., 1st Semester): ")
                            acad_year = input("Enter academic year (e.g., 2024–2025): ")
                            rows = views.view_late_payments(connect.cur, connect.conn, org_id, semester, acad_year)

                            print_rows(rows)
                        
                        case '3':
                            semester = input("Enter semester (e.g., 1st Semester): ")
                            rows = views.view_late_payments(connect.cur, connect.conn, org_id, semester, acad_year)
                            
                            print_rows(rows)
                        
                        case '4':
                            given_date = input("Enter date (YYYY-MM-DD): ")
                            formatted_date = format_date(given_date)
                            if not formatted_date:
                                print("Invalid date format. Please use YYYY-MM-DD.")
                                continue
                            rows = views.view_total_fees(connect.cur, connect.conn, org_id, formatted_date)

                            print_rows(rows)

                        case '5':
                            break
                        
                        case _:
                            print("Invalid choice.")

            case '3':
                return

            case _:
                print("Invalid choice.")
