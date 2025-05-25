def menu():
    # Menu Loop
    while True:
        print('========== MENU ==========')
        print('[1] Log In')
        print('[2] Exit')
        print('==========================')
        choice = input('Choice: ')

        match choice:
            case '1':
                print('Logged In')
            case '2':
                print('Terminating program...')
                break
            case _:
                print('Invalid Choice')

# Main func
def main():
    menu()

# Run main
main()