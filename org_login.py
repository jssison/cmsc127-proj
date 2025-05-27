import tkinter as tk
from tkinter import ttk, messagebox
from admin import connect, views

def format_date(date_str):
    connect.cur.execute("SELECT DATE_FORMAT(STR_TO_DATE(?, '%Y-%m-%d'), '%Y-%m-%d')", (date_str,))
    result = connect.cur.fetchone()
    if result:
        return result[0]
    return None

def format_str(s):
    return f"`{s.strip().replace('`', '')}`"

def print_rows_treeview(tree, rows):
    for i in tree.get_children():
        tree.delete(i)
    for idx, row in enumerate(rows):
        # Add tag for row styling (alternate colors or just maroon bg)
        tree.insert("", "end", values=row, tags=('maroon_row',))

def set_tree_columns(tree, cols):
    tree.delete(*tree.get_children())
    tree["columns"] = cols
    tree["show"] = "headings"
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

def open_members_menu(main_menu_win, org_id):
    main_menu_win.withdraw()  # Hide the organization main menu
    
    win = tk.Toplevel(main_menu_win)
    win.title("Organization Members")
    win.geometry("850x600")
    win.configure(bg="white")

    lbl = tk.Label(win, text="Organization Members", font=("Helvetica", 14, "bold"), fg="#800000", bg="white")
    lbl.pack(pady=10)

    frame_opts = tk.Frame(win, bg="white")
    frame_opts.pack(pady=5)

    options = [
        ("Members of the Organization", "members"),
        ("Executive Members", "executive"),
        ("Alumni Members", "alumni"),
        ("List of Past and Present in Position", "role"),
        ("Percentage of active vs inactive members", "percentage"),
    ]

    selected_option = tk.StringVar(value=options[0][1])
    for text, val in options:
        rb = tk.Radiobutton(frame_opts, text=text, variable=selected_option, value=val, bg="white", fg="#800000", anchor="w")
        rb.pack(fill='x', padx=20)

    frame_inputs = tk.Frame(win, bg="white")
    frame_inputs.pack(pady=10)
    input_vars = {}

    def clear_inputs():
        for widget in frame_inputs.winfo_children():
            widget.destroy()
        input_vars.clear()

    def create_input(label_text, var_name):
        lbl = tk.Label(frame_inputs, text=label_text, bg="white", fg="#800000")
        lbl.pack(anchor="w", padx=10)
        ent = tk.Entry(frame_inputs)
        ent.pack(fill='x', padx=10, pady=2)
        input_vars[var_name] = ent

    def update_inputs(*args):
        clear_inputs()
        opt = selected_option.get()
        if opt == "members":
            create_input("Order by (e.g., Role, Gender, Status, Degree Program, Batch year, Committee):", "order_by")
        elif opt == "executive":
            create_input("Academic year (e.g., 2024–2025):", "acad_year")
        elif opt == "alumni":
            create_input("Date (YYYY-MM-DD):", "date")
        elif opt == "role":
            create_input("Role:", "role")
        elif opt == "percentage":
            create_input("Number of semesters:", "num_semesters")

    selected_option.trace_add("write", update_inputs)
    update_inputs()

    tree_frame = tk.Frame(win)
    tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
    tree = ttk.Treeview(tree_frame)
    tree.pack(fill='both', expand=True)

    # Apply maroon background color to rows via tag configuration
    style = ttk.Style()
    style.configure("Treeview", background="white", foreground="black", fieldbackground="white")
    style.map("Treeview", background=[('selected', '#800000')], foreground=[('selected', 'white')])
    tree.tag_configure('maroon_row', background='#800000', foreground='white')

    def run_query():
        opt = selected_option.get()
        try:
            if opt == "members":
                order_by = input_vars["order_by"].get()
                if not order_by:
                    messagebox.showerror("Input Error", "Order by is required.")
                    return
                formatted_order_by = format_str(order_by)
                rows = views.view_members_by(connect.cur, connect.conn, formatted_order_by, org_id)
                headers = ["Membership ID", "Full Name", "Role", "Status", "Gender", "Degree Program", "Batch year", "Committee"]
                set_tree_columns(tree, headers)
                print_rows_treeview(tree, rows)

            elif opt == "executive":
                acad_year = input_vars["acad_year"].get()
                if not acad_year:
                    messagebox.showerror("Input Error", "Academic year is required.")
                    return
                rows = views.view_executive_members(connect.cur, connect.conn, org_id, acad_year)
                if rows:
                    headers = ["Membership ID", "Full Name", "Organization", "Academic Year"]
                    set_tree_columns(tree, headers)
                print_rows_treeview(tree, rows)

            elif opt == "alumni":
                date_str = input_vars["date"].get()
                formatted_date = format_date(date_str)
                if not formatted_date:
                    messagebox.showerror("Input Error", "Invalid date format. Use YYYY-MM-DD.")
                    return
                rows = views.view_alumni(connect.cur, connect.conn, org_id, formatted_date)
                if rows:
                    headers = ["Membership ID", "Full Name", "Organization"]
                    set_tree_columns(tree, headers)
                print_rows_treeview(tree, rows)

            elif opt == "role":
                role = input_vars["role"].get()
                if not role:
                    messagebox.showerror("Input Error", "Role is required.")
                    return
                rows = views.view_role(connect.cur, connect.conn, role, org_id)
                if rows:
                    headers = ["Membership ID", "Full Name", "Role", "Organization", "Academic Year"]
                    set_tree_columns(tree, headers)
                print_rows_treeview(tree, rows)

            elif opt == "percentage":
                try:
                    num_semesters = int(input_vars["num_semesters"].get())
                except:
                    messagebox.showerror("Input Error", "Number of semesters must be an integer.")
                    return
                rows = views.view_percentage(connect.cur, connect.conn, org_id, num_semesters)
                if rows:
                    headers = ["Total Members", "Active Count", "Inactive Count", "Active Percentage", "Inactive Percentage"]
                    set_tree_columns(tree, headers)
                print_rows_treeview(tree, rows)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

    tk.Button(win, text="View", bg="#800000", fg="white", command=run_query).pack(pady=5)

    def on_close():
        main_menu_win.deiconify()  # Show the organization main menu again
        win.destroy()

    tk.Button(win, text="Close", bg="#cccccc", fg="#800000", command=on_close).pack(pady=5)
    win.protocol("WM_DELETE_WINDOW", on_close)

def open_fees_menu(main_menu_win, org_id):
    main_menu_win.withdraw()  # Hide the organization main menu
    
    win = tk.Toplevel(main_menu_win)
    win.title("Organization Fees")
    win.geometry("850x600")
    win.configure(bg="white")

    lbl = tk.Label(win, text="Organization Fees", font=("Helvetica", 14, "bold"), fg="#800000", bg="white")
    lbl.pack(pady=10)

    frame_opts = tk.Frame(win, bg="white")
    frame_opts.pack(pady=5)

    options = [
        ("List of Unpaid Members", "unpaid"),
        ("Late Payments by all Members", "late"),
        ("Member/s with Highest Unpaid Fees", "highest"),
        ("Total Unpaid and Paid Fees", "total"),
    ]

    selected_option = tk.StringVar(value=options[0][1])
    for text, val in options:
        rb = tk.Radiobutton(frame_opts, text=text, variable=selected_option, value=val, bg="white", fg="#800000", anchor="w")
        rb.pack(fill='x', padx=20)

    frame_inputs = tk.Frame(win, bg="white")
    frame_inputs.pack(pady=10)
    input_vars = {}

    def clear_inputs():
        for widget in frame_inputs.winfo_children():
            widget.destroy()
        input_vars.clear()

    def create_input(label_text, var_name):
        lbl = tk.Label(frame_inputs, text=label_text, bg="white", fg="#800000")
        lbl.pack(anchor="w", padx=10)
        ent = tk.Entry(frame_inputs)
        ent.pack(fill='x', padx=10, pady=2)
        input_vars[var_name] = ent

    def update_inputs(*args):
        clear_inputs()
        opt = selected_option.get()
        if opt in ("unpaid", "late", "highest"):
            create_input("Semester (e.g., 1st Semester):", "semester")
            if opt != "highest":
                create_input("Academic year (e.g., 2024–2025):", "acad_year")
        elif opt == "total":
            create_input("Date (YYYY-MM-DD):", "date")

    selected_option.trace_add("write", update_inputs)
    update_inputs()

    tree_frame = tk.Frame(win)
    tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
    tree = ttk.Treeview(tree_frame)
    tree.pack(fill='both', expand=True)

    # Apply maroon background color to rows via tag configuration
    style = ttk.Style()
    style.configure("Treeview", background="white", foreground="black", fieldbackground="white")
    style.map("Treeview", background=[('selected', '#800000')], foreground=[('selected', 'white')])
    tree.tag_configure('maroon_row', background='#800000', foreground='white')

    def run_query():
        opt = selected_option.get()
        try:
            if opt == "unpaid":
                semester = input_vars["semester"].get()
                acad_year = input_vars["acad_year"].get()
                if not semester or not acad_year:
                    messagebox.showerror("Input Error", "Semester and academic year are required.")
                    return
                rows = views.view_unpaid_members(connect.cur, connect.conn, org_id, semester, acad_year)
                if rows:
                    headers = ["Membership ID", "Full Name", "Degree Program", "Gender", "Organization ID", "Academic Year", "Semester"]
                    set_tree_columns(tree, headers)
                    print_rows_treeview(tree, rows)
                else:
                    set_tree_columns(tree, [])
                    messagebox.showinfo("No Data", "No unpaid members found.")

            elif opt == "late":
                semester = input_vars["semester"].get()
                acad_year = input_vars["acad_year"].get()
                if not semester or not acad_year:
                    messagebox.showerror("Input Error", "Semester and academic year are required.")
                    return
                rows = views.view_late_payments(connect.cur, connect.conn, org_id, semester, acad_year)
                if rows:
                    headers = ["Membership ID", "Full Name", "Degree Program", "Gender", "Organization ID", "Academic Year", "Semester", "Fee Reference Number", "Due Date", "Date of Payment", "Status"]
                    set_tree_columns(tree, headers)
                    print_rows_treeview(tree, rows)
                else:
                    set_tree_columns(tree, [])
                    messagebox.showinfo("No Data", "No late payments found.")

            elif opt == "highest":
                semester = input_vars["semester"].get()
                if not semester:
                    messagebox.showerror("Input Error", "Semester is required.")
                    return
                rows = views.view_unpaid(connect.cur, connect.conn, org_id, semester)
                if rows:
                    headers = ["Membership ID", "Full Name", "Unpaid Amount"]
                    set_tree_columns(tree, headers)
                    print_rows_treeview(tree, rows)
                else:
                    set_tree_columns(tree, [])
                    messagebox.showinfo("No Data", "No highest unpaid fees found.")

            elif opt == "total":
                date_str = input_vars["date"].get()
                formatted_date = format_date(date_str)
                if not formatted_date:
                    messagebox.showerror("Input Error", "Invalid date format. Use YYYY-MM-DD.")
                    return
                rows = views.view_total_fees(connect.cur, connect.conn, org_id, formatted_date)
                if rows:
                    headers = ["Total Unpaid", "Total Paid"]
                    set_tree_columns(tree, headers)
                    print_rows_treeview(tree, rows)
                else:
                    set_tree_columns(tree, [])
                    messagebox.showinfo("No Data", "No fee records found.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

    tk.Button(win, text="View", bg="#800000", fg="white", command=run_query).pack(pady=5)

    def on_close():
        main_menu_win.deiconify()  # Show the organization main menu again
        win.destroy()

    tk.Button(win, text="Close", bg="#cccccc", fg="#800000", command=on_close).pack(pady=5)
    win.protocol("WM_DELETE_WINDOW", on_close)

def main(parent, org_id):
    # parent: is root (dashboard window)
    parent.withdraw()  # Hide dashboard while org main menu is open

    win = tk.Toplevel(parent)
    win.title("Organization Main Menu")
    win.geometry("400x300")
    win.configure(bg="white")

    tk.Label(win, text="Organization Menu", font=("Helvetica", 16, "bold"), fg="#800000", bg="white").pack(pady=30)

    # Buttons for different org menu actions
    tk.Button(win, text="Organization Members", width=25, fg="#800000",
              command=lambda: open_members_menu(win, org_id)).pack(pady=10)
    tk.Button(win, text="Organization Fees", width=25, fg="#800000",
              command=lambda: open_fees_menu(win, org_id)).pack(pady=10)

    def back_to_dashboard():
        win.destroy()
        parent.deiconify()  # Show dashboard again

    tk.Button(win, text="Back to Dashboard", width=25, fg="#800000", command=back_to_dashboard).pack(pady=10)

    def on_close():
        back_to_dashboard()

    win.protocol("WM_DELETE_WINDOW", on_close)
