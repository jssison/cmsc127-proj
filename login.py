from admin import connect
import org_login

org_id = None
mem_id = None

def login():
    while True:
        print('\n========== LOG IN  AS ==========')
        print('[1] Organization')
        print('[2] Member')
        print('[3] Exit')
        print('==================================')
        log_in_as = input('Choice: ')
        
        if log_in_as not in ['1', '2', '3']:
            print('\nInvalid choice. Please try again.')
            continue
        elif log_in_as == '1' or log_in_as == '2':
            username = input('Username: ')
            password = input('Password: ')

        match log_in_as:
            case '1':
                connect.cur.execute("SELECT * FROM organization WHERE org_username = ? AND org_password = ?", (username, password))
                authenticate1 = connect.cur.fetchone()
                if authenticate1:
                    org_id = authenticate1[0]
                    print("\nWelcome!")
                    org_login.org_login(org_id)
                else:
                    print('\nInvalid credentials')
            
            case '2':
                connect.cur.execute("SELECT * FROM member WHERE mem_uname = ? AND mem_pword = ?", (username, password))
                authenticate2 = connect.cur.fetchone()
                if authenticate2:
                    print("\nWelcome!")
                    break
                else:
                    print('\nInvalid credentials')
            
            case '3':
                print('\nExiting...')
                break

            case _:
                print('\nInvalid choice.')
