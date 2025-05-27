from admin import connect
import login
from admin import views
from tabulate import tabulate

#Printing of rows
#
#    for row in rows:
#       print(row)

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

def print_rows(rows):
    if not rows:
        print("No data found.")
        return
    
    headers = [desc[0] for desc in connect.cur.description]  #getting the column names from the views
    print(tabulate(rows, headers=headers, tablefmt="heavy_grid")) #Reference: https://pypi.org/project/tabulate/

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
                    print('\n========== VIEW MEMBERS ==========')
                    print('[1] Members of the Organization')
                    print('[2] Executive Members')
                    print('[3] Alumni Members')
                    print('[4] List of Past and Present in Position')
                    print('[5] Percentage of active vs inactive members')
                    print('[6] Back to View Menu')
                    choice1 = input('Enter choice: ')

                    match choice1:
                        case '1':
                            order_by = input("Enter order by (e.g., Role, Gender, Status, Degree Program, Batch year, Committee): ")
                            formatted_order_by = format_str(order_by)
                            rows = views.view_members_by(connect.cur, connect.conn, formatted_order_by, org_id)
                            #Print the results
                            print_rows(rows)

                        case '2':
                            acad_year = input("Enter academic year (e.g., 2024–2025): ")
                            rows = views.view_executive_members(connect.cur, connect.conn, org_id, acad_year)

                            print_rows(rows)

                        case '3':
                            given_date = input("Enter date (YYYY-MM-DD): ")
                            formatted_date = format_date(given_date)
                            if not formatted_date:
                                print("Invalid date format. Please use YYYY-MM-DD.")
                                continue
                            rows = views.view_alumni(connect.cur, connect.conn, org_id, formatted_date)
                            
                            if not rows:
                                    print(f"\nNo alumni as of {given_date}.")
                            else:
                                    print_rows(rows)

                        case '4':
                            role = input("Enter role: ")
                            rows = views.view_role(connect.cur, connect.conn, role, org_id)

                            print_rows(rows)

                        case '5':
                            num_of_sems = int(input("Enter number of semesters: "))
                            rows = views.view_percentage(connect.cur, connect.conn, org_id, num_of_sems)
                            
                            print_rows(rows)

                        case '6':
                            break
                        
                        case _:
                            print("Invalid choice.")
            
            case '2':
                while True:
                    print('\n========== VIEW FEES ==========')
                    print('[1] List of Unpaid Members')
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

                            if not rows:
                                    print(f"\nNo unpaid members for {semester}, {acad_year}.")
                            else:
                                    print_rows(rows)

                        case '2':
                            semester = input("Enter semester (e.g., 1st Semester): ")
                            acad_year = input("Enter academic year (e.g., 2024–2025): ")
                            rows = views.view_late_payments(connect.cur, connect.conn, org_id, semester, acad_year)

                            if not rows:
                                    print(f"\nNo late payments made by members for {semester}, {acad_year}.")
                            else:
                                    print_rows(rows)
                        
                        case '3':
                            semester = input("Enter semester (e.g., 1st Semester): ")
                            acad_year = input("Enter academic year (e.g., 2024–2025): ")
                            rows = views.view_unpaid(connect.cur, connect.conn, org_id, semester, acad_year)
                            
                            if not rows:
                                    print(f"\nNo members have debt for {semester}, {acad_year}.")
                            else:
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
