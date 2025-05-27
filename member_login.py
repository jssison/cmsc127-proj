import tkinter as tk
from tkinter import ttk, messagebox
from admin import connect

def member_login_gui(mem_id, root_window=None):

    # Displays a GUI for the logged-in member, showing personal details and unpaid fees.

    # Parameters:
    # - mem_id: The ID of the member who logged in.
    # - root_window: The root Tkinter window to return to (if applicable).

    # Create a new Toplevel window for the member dashboard
    member_window = tk.Toplevel()
    member_window.title("Member Dashboard")
    member_window.geometry("700x600")
    member_window.configure(bg="#ffffff")

    # Font and color definitions
    header_font = ("Helvetica", 14, "bold")
    label_font = ("Helvetica", 11)
    maroon = "#800000"
    white = "#ffffff"

    # Dashboard header label
    tk.Label(member_window, text="Member Dashboard", font=header_font, fg=maroon, bg=white).pack(pady=10)

    # Style setup for Treeview with maroon theme
    style = ttk.Style()
    style.theme_use("default")

    style.configure("Maroon.Treeview",
                    background=maroon,
                    fieldbackground=maroon,
                    foreground=white,
                    font=label_font,
                    rowheight=25)
    style.configure("Maroon.Treeview.Heading",
                    background=maroon,
                    foreground=white,
                    font=(label_font[0], label_font[1], "bold"))

    style.map('Maroon.Treeview',
              background=[('selected', '#b03030')],
              foreground=[('selected', white)])

    # Query to fetch member and organization-related information
    connect.cur.execute("""
        SELECT 
            m.fname, m.mname, m.lname, m.degprog, m.gender,
            o.org_name,
            ohm.committee, ohm.semester, ohm.batch_name, ohm.mem_status, ohm.batch_year
        FROM member m
        JOIN organization_has_member ohm ON m.mem_id = ohm.mem_id
        JOIN organization o ON ohm.org_id = o.org_id
        WHERE m.mem_id = ?
    """, (mem_id,))
    rows = connect.cur.fetchall()

    if not rows:
        messagebox.showerror("Error", "No membership or organization data found.")
        return

    # Section title for member details
    tk.Label(member_window, text="Member Details", font=("Helvetica", 12, "bold"), bg=maroon, fg=white).pack(padx=20, pady=(10,0), fill='x')

    # Treeview setup to show member details
    columns = ("Field", "Value")
    tree_frame = tk.Frame(member_window, bg=white)
    tree_frame.pack(padx=20, pady=10, fill="x")

    tree = ttk.Treeview(tree_frame, columns=columns, show="", height=10, style="Maroon.Treeview")
    tree.pack(fill="x", expand=True)

    for col in columns:
        tree.column(col, anchor="w", width=300)

    # Parse and insert data into the treeview
    for row in rows:
        fname, mname, lname, degprog, gender, org_name, committee, semester, batch_name, mem_status, batch_year = row
        full_name = f"{fname} {mname + ' ' if mname else ''}{lname}"

        tree.insert("", "end", values=("Full Name", full_name))

        info = [
            ("Degree Program", degprog),
            ("Gender", gender),
            ("Organization", org_name),
            ("Committee", committee),
            ("Semester", semester),
            ("Batch Name", batch_name),
            ("Member Status", mem_status),
            ("Batch Year", batch_year)
        ]

        for field, value in info:
            tree.insert("", "end", values=(field, value))

    # Unpaid fees section with try-except to handle potential query failures
    try:
        # Create or update a view showing unpaid fees for this member
        connect.cur.execute(f"""
            CREATE OR REPLACE VIEW unpaid_member_fees AS
            SELECT fee.fee_refnum AS `Fee reference number`,
                   fee.category AS `Category`,
                   fee.due_date AS `Due date`,
                   fee.amount AS `Amount`,
                   org.org_name AS `Organization Name`,
                   mem_fee.academic_year AS `Academic Year`,
                   mem_fee.semester AS `Semester`,
                   mem_fee.payment_status AS `Payment Status`
            FROM member mem
            JOIN member_pays_fee mem_fee ON mem.mem_id = mem_fee.mem_id
            JOIN fee ON mem_fee.fee_refnum = fee.fee_refnum
            JOIN organization org ON fee.org_id = org.org_id
            WHERE mem.mem_id = '{mem_id}' AND mem_fee.payment_status = 'Not Paid';
        """)
        connect.conn.commit()

        # Fetch all unpaid fees from the view
        connect.cur.execute("SELECT * FROM unpaid_member_fees")
        unpaid_fees = connect.cur.fetchall()

        # Section title for unpaid fees
        tk.Label(member_window, text="\n📌 Unpaid Fees", font=header_font, fg=maroon, bg=white).pack(pady=10)

        if unpaid_fees:
            frame = tk.Frame(member_window, bg=white)
            frame.pack(padx=20, fill='both', expand=True)

            cols = ["Category", "Amount", "Due Date", "Org Name", "Academic Year", "Semester"]
            tree_fees = ttk.Treeview(frame, columns=cols, show="headings", height=6, style="Maroon.Treeview")
            
            for col in cols:
                tree_fees.heading(col, text=col)
                tree_fees.column(col, anchor="center")

            total_amt = 0
            for fee in unpaid_fees:
                ref, cat, due, amt, org, ay, sem, status = fee
                tree_fees.insert("", "end", values=(cat, f"₱{amt}", due, org, ay, sem))
                total_amt += amt

            tree_fees.pack(fill="both", expand=True)

            # Display total amount due
            tk.Label(member_window, text=f"\nTotal Unpaid Fees: ₱{total_amt}", font=label_font, fg=maroon, bg=white).pack(pady=10)
        else:
            tk.Label(member_window, text="Yehey! You have no unpaid fees!", font=label_font, fg=maroon, bg=white).pack(pady=10)

    except Exception as e:
        # Show error if query fails
        messagebox.showerror("Error", f"Error displaying unpaid fees:\n{e}")

    # Back button to close the member window and return to root (if applicable)
    def go_back():
        if root_window:
            root_window.deiconify()
        member_window.destroy()

    tk.Button(member_window, text="Back", command=go_back, bg=white, fg=maroon, font=label_font).pack(pady=15)
