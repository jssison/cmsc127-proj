from admin import connect
import org_login
import member_login

org_id = None
mem_id = None

def login():
    print('\n========== LOG IN  AS ==========')
    print('[1] Organization')
    print('[2] Member')
    log_in_as = input('Choice: ')
    
    username = input('\nEnter Username: ')
    password = input('Password: ')

    match log_in_as:
        case '1':
            connect.cur.execute("SELECT * FROM organization WHERE org_username = ? AND org_password = ?", (username, password))
            authenticate1 = connect.cur.fetchone()
            if authenticate1:
                org_id = authenticate1[0]
                print("\nWelcome!")
                print("========== What do you want to do? ==========")
                print("[1] Add Members")
                print("[2] Remove Members")
                print("[3] View Members and Fees")
                answer = input("Enter choice: ")

                match answer:
                    #case '1':
                    #case '2':
                    case '3':
                        org_login.org_login(org_id)
                    case _:
                        'Invalid choice.'

            else:
                print('\nInvalid credentials')
        
        case '2':
            connect.cur.execute("SELECT * FROM member WHERE mem_uname = ? AND mem_pword = ?", (username, password))
            authenticate2 = connect.cur.fetchone()
            if authenticate2:
                mem_id = authenticate2[0]
                print(f"\nWelcome, {authenticate2[3]}!") 
                member_login.member_login(mem_id)

            else:
                print('\nInvalid credentials')

        case _:
            print('\nInvalid choice.')
