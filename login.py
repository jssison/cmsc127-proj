import tkinter as tk
from tkinter import messagebox

from admin import connect
import org_login  # Assuming this contains the org main menu Toplevel
import member_login
import remove_member
import add_member
import edit_member

org_id = None
mem_id = None

# Window setup
root = tk.Tk()
root.title("Login Portal")
root.geometry("420x450")
root.configure(bg="#ffffff")

# --- Colors & Fonts ---
MAROON = "#800000"
LIGHT_BG = "#f9f9f9"
BUTTON_BG = "#a94442"
BUTTON_FG = "white"
FONT_TITLE = ("Helvetica", 18, "bold")
FONT_LABEL = ("Helvetica", 12)
FONT_ENTRY = ("Helvetica", 11)
FONT_BUTTON = ("Helvetica", 11, "bold")


def clear_screen():
    for widget in root.winfo_children():
        widget.pack_forget()


def show_org_dashboard(org_id_param):
    global org_id
    org_id = org_id_param  # store globally for access elsewhere

    clear_screen()
    root.deiconify()  # Make sure root is visible when showing dashboard

    tk.Label(root, text="Organization Dashboard", font=FONT_TITLE, bg="#ffffff", fg=MAROON).pack(pady=(20, 10))

    def handle_choice(choice):
        if choice == 1:
            root.withdraw()
            add_member.add_member_gui(org_id, parent_window=root)
        elif choice == 2:
            root.withdraw()
            remove_member.remove_member(org_id, parent_window=root)
        elif choice == 3:
            root.withdraw()
            edit_member.edit_member_menu(org_id, parent_window=root)
        elif choice == 4:
            root.withdraw()
            # Open org main menu as Toplevel and pass root so it can deiconify root on close
            org_login.main(root, org_id)
        else:
            messagebox.showerror("Error", "Invalid option")

    tk.Button(root, text="Add Members", font=FONT_BUTTON, bg=BUTTON_BG, fg=MAROON, command=lambda: handle_choice(1)).pack(pady=5)
    tk.Button(root, text="Remove Members", font=FONT_BUTTON, bg=BUTTON_BG, fg=MAROON, command=lambda: handle_choice(2)).pack(pady=5)
    tk.Button(root, text="Edit Members", font=FONT_BUTTON, bg=BUTTON_BG, fg=MAROON, command=lambda: handle_choice(3)).pack(pady=5)
    tk.Button(root, text="View Members & Fees", font=FONT_BUTTON, bg=BUTTON_BG, fg=MAROON, command=lambda: handle_choice(4)).pack(pady=5)
    tk.Button(root, text="Logout", font=FONT_BUTTON, bg="#cccccc", fg=MAROON, command=main_menu).pack(pady=20)


def show_login_fields(role):
    clear_screen()

    tk.Label(root, text=f"{role} Login", font=FONT_TITLE, bg="#ffffff", fg=MAROON).pack(pady=(30, 10))

    # Username
    tk.Label(root, text="Username:", font=FONT_LABEL, bg="#ffffff", fg=MAROON).pack()
    username_entry = tk.Entry(root, font=FONT_ENTRY, bg=LIGHT_BG, fg=MAROON)
    username_entry.pack(pady=5)

    # Password
    tk.Label(root, text="Password:", font=FONT_LABEL, bg="#ffffff", fg=MAROON).pack()
    password_entry = tk.Entry(root, show="*", font=FONT_ENTRY, bg=LIGHT_BG, fg=MAROON)
    password_entry.pack(pady=5)

    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()

        if role == "Organization":
            connect.cur.execute("SELECT * FROM organization WHERE org_username = ? AND org_password = ?", (username, password))
            auth = connect.cur.fetchone()
            if auth:
                global org_id
                org_id = auth[0]
                messagebox.showinfo("Success", "Welcome Organization!")
                show_org_dashboard(org_id)
            else:
                messagebox.showerror("Login Failed", "Invalid credentials.")
        elif role == "Member":
            connect.cur.execute("SELECT * FROM member WHERE mem_uname = ? AND mem_pword = ?", (username, password))
            auth = connect.cur.fetchone()
            if auth:
                global mem_id
                mem_id = auth[0]
                messagebox.showinfo("Success", f"Welcome, {auth[3]}!")
                root.withdraw()  # hides the login window
                member_login.member_login_gui(mem_id, root)
            else:
                messagebox.showerror("Login Failed", "Invalid credentials.")

    tk.Button(root, text="Login", font=FONT_BUTTON, bg=BUTTON_BG, fg=MAROON, command=attempt_login).pack(pady=10)
    tk.Button(root, text="Back", font=FONT_BUTTON, bg="#cccccc", fg=MAROON, command=main_menu).pack(pady=5)


def main_menu():
    clear_screen()
    root.deiconify()  # Ensure root is visible when showing main menu

    tk.Label(root, text="Login as:", font=FONT_TITLE, bg="#ffffff", fg=MAROON).pack(pady=(40, 20))

    tk.Button(root, text="Organization", font=FONT_BUTTON, bg=BUTTON_BG, fg=MAROON,
              command=lambda: show_login_fields("Organization")).pack(pady=10)
    tk.Button(root, text="Member", font=FONT_BUTTON, bg=BUTTON_BG, fg=MAROON,
              command=lambda: show_login_fields("Member")).pack(pady=10)
    tk.Button(root, text="Exit", font=FONT_BUTTON, bg="#999999", fg=MAROON, command=root.quit).pack(pady=10)


# --- Start the app ---
main_menu()
root.mainloop()
