import tkinter as tk
from tkinter import messagebox

from admin import connect
import org_login 
import member_login
import remove_member
import add_member
import edit_member

# Global variables to store currently logged-in organization and member IDs
org_id = None
mem_id = None

# --- Main Application Window Setup ---
root = tk.Tk()
root.title("Login Portal")
root.geometry("420x450")
root.configure(bg="#ffffff")

# --- Color and Font Configuration ---
MAROON = "#800000"
LIGHT_BG = "#f9f9f9"
BUTTON_BG = "#a94442"
BUTTON_FG = "white"
FONT_TITLE = ("Helvetica", 18, "bold")
FONT_LABEL = ("Helvetica", 12)
FONT_ENTRY = ("Helvetica", 11)
FONT_BUTTON = ("Helvetica", 11, "bold")

def clear_screen():
   
    #Clears all widgets from the main window.
    #Used when switching between screens (login, dashboard, etc.).

    for widget in root.winfo_children():
        widget.pack_forget()

def show_org_dashboard(org_id_param):
    
    #Displays the dashboard for the logged-in organization user.

    #Parameters:
    #- org_id_param: The ID of the logged-in organization.
    
    global org_id
    org_id = org_id_param

    clear_screen()
    root.deiconify()

    # Dashboard Title
    tk.Label(root, text="Organization Dashboard", font=FONT_TITLE, bg="#ffffff", fg=MAROON).pack(pady=(20, 10))

    def handle_choice(choice):
        
        #Handles button choices for dashboard actions.

        #Parameters:
        #- choice: Integer representing action selected.
        #   1 = Add Member
        #   2 = Remove Member
        #   3 = Edit Member
        #   4 = View Members & Fees
        
        if choice == 1:
            root.withdraw()
            add_member.add_member_gui(org_id, parent_window=root)
        elif choice == 2:
            remove_member.remove_member(org_id, parent_window=root)
            root.bind("<<BackToDashboard>>", lambda e: show_org_dashboard(org_id))
        elif choice == 3:
            edit_member.edit_member_menu(org_id, parent_window=root)
            root.bind("<<BackToDashboard>>", lambda e: show_org_dashboard(org_id))
        elif choice == 4:
            root.withdraw()
            org_login.main(root, org_id)
        else:
            messagebox.showerror("Error", "Invalid option")

    # Dashboard Buttons
    tk.Button(root, text="Add Members", font=FONT_BUTTON, bg=BUTTON_BG, fg=MAROON,
              command=lambda: handle_choice(1)).pack(pady=5)
    tk.Button(root, text="Remove Members", font=FONT_BUTTON, bg=BUTTON_BG, fg=MAROON,
              command=lambda: handle_choice(2)).pack(pady=5)
    tk.Button(root, text="Edit Members", font=FONT_BUTTON, bg=BUTTON_BG, fg=MAROON,
              command=lambda: handle_choice(3)).pack(pady=5)
    tk.Button(root, text="View Members & Fees", font=FONT_BUTTON, bg=BUTTON_BG, fg=MAROON,
              command=lambda: handle_choice(4)).pack(pady=5)
    tk.Button(root, text="Logout", font=FONT_BUTTON, bg="#cccccc", fg=MAROON,
              command=main_menu).pack(pady=20)

def login_attempt():
    
    #Displays the login screen and handles authentication for both organizations and members.
    
    clear_screen()

    tk.Label(root, text="Login", font=FONT_TITLE, bg="#ffffff", fg=MAROON).pack(pady=(30, 10))

    # Username Field
    tk.Label(root, text="Username:", font=FONT_LABEL, bg="#ffffff", fg=MAROON).pack()
    username_entry = tk.Entry(root, font=FONT_ENTRY, bg=LIGHT_BG, fg=MAROON)
    username_entry.pack(pady=5)

    # Password Field
    tk.Label(root, text="Password:", font=FONT_LABEL, bg="#ffffff", fg=MAROON).pack()
    password_entry = tk.Entry(root, show="*", font=FONT_ENTRY, bg=LIGHT_BG, fg=MAROON)
    password_entry.pack(pady=5)

    def authenticate():
        
        #Authenticates the user based on username and password input.
        #Redirects to either organization dashboard or member GUI.
        
        username = username_entry.get()
        password = password_entry.get()

        # Try organization credentials
        connect.cur.execute("SELECT * FROM organization WHERE org_username = ? AND org_password = ?",
                            (username, password))
        org_authenticate = connect.cur.fetchone()
        if org_authenticate:
            global org_id
            org_id = org_authenticate[0]
            messagebox.showinfo("Login Successful", "Welcome to your Organization's Account!")
            show_org_dashboard(org_id)
            return

        # Try member credentials
        connect.cur.execute("SELECT * FROM member WHERE mem_uname = ? AND mem_pword = ?",
                            (username, password))
        mem_authenticate = connect.cur.fetchone()
        if mem_authenticate:
            global mem_id
            mem_id = mem_authenticate[0]
            messagebox.showinfo("Login Successful", f"Welcome, {mem_authenticate[3]}!")
            root.withdraw()
            member_login.member_login_gui(mem_id, root)
            return

        # Invalid credentials
        messagebox.showerror("Login Failed", "Invalid credentials. Please try again.")

    # Login and Back Buttons
    tk.Button(root, text="Login", font=FONT_BUTTON, bg=BUTTON_BG, fg=MAROON,
              command=authenticate).pack(pady=10)
    tk.Button(root, text="Back", font=FONT_BUTTON, bg="#cccccc", fg=MAROON,
              command=main_menu).pack(pady=5)

def main_menu():
    
    #Displays the main menu of the portal with options to Login or Exit.
    
    clear_screen()
    root.deiconify()

    tk.Label(root, text="Login to Portal", font=FONT_TITLE, bg="#ffffff", fg=MAROON).pack(pady=(40, 20))
    tk.Button(root, text="Login", font=FONT_BUTTON, bg=BUTTON_BG, fg=MAROON,
              command=login_attempt).pack(pady=10)
    tk.Button(root, text="Exit", font=FONT_BUTTON, bg="#999999", fg=MAROON,
              command=root.quit).pack(pady=10)

# --- Start Application ---
main_menu()
root.mainloop()
