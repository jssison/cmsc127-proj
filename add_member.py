import tkinter as tk
from tkinter import messagebox
import re

from admin import connect  # your DB connection and cursor

def edit_member_gui(member_id, parent_window=None):
    edit_win = tk.Toplevel()
    edit_win.title("Edit Member")
    edit_win.geometry("450x650")
    edit_win.configure(bg="#ffffff")

    MAROON = "#800000"
    FONT_LABEL = ("Helvetica", 11)
    FONT_ENTRY = ("Helvetica", 11)

    def on_close():
        if parent_window:
            parent_window.deiconify()
        edit_win.destroy()

    edit_win.protocol("WM_DELETE_WINDOW", on_close)

    # Canvas + scrollbar for scrollable form
    canvas = tk.Canvas(edit_win, bg="#ffffff", highlightthickness=0)
    scrollbar = tk.Scrollbar(edit_win, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#ffffff")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tk.Label(scrollable_frame, text="Edit Member", font=("Helvetica", 16, "bold"), fg=MAROON, bg="#ffffff").pack(pady=10)

    entries = {}

    # --- Validators ---
    def validate_alnum(P):
        return P.isalnum() or P == ""

    def validate_numeric(P):
        return P.isdigit() or P == ""

    def validate_alpha_space_dash(P):
        return all(c.isalpha() or c.isspace() or c == '-' for c in P) or P == ""

    def validate_gender(P):
        return P.upper() in ("M", "F", "")

    def validate_year_format(P):
        return re.fullmatch(r"(\d{0,4}(-\d{0,4})?)?", P) is not None

    # Helper to add label+entry with optional validation
    def add_label_entry(text, required=True, validate_func=None):
        tk.Label(scrollable_frame, text=text, font=FONT_LABEL, fg=MAROON, bg="#ffffff", anchor="w").pack(fill='x', pady=(10, 0), padx=10)
        if validate_func:
            vcmd = edit_win.register(validate_func)
            ent = tk.Entry(scrollable_frame, font=FONT_ENTRY, bg="#f9f9f9", fg=MAROON,
                           validate="key", validatecommand=(vcmd, '%P'))
        else:
            ent = tk.Entry(scrollable_frame, font=FONT_ENTRY, bg="#f9f9f9", fg=MAROON)
        ent.pack(fill='x', pady=(0, 5), padx=10)
        entries[text] = (ent, required)

    # Add fields with validation where appropriate
    add_label_entry("Member ID:", validate_func=validate_numeric)
    add_label_entry("Username:")
    add_label_entry("Password:")
    add_label_entry("First Name:", validate_func=validate_alpha_space_dash)
    add_label_entry("Middle Name (optional):", required=False, validate_func=validate_alpha_space_dash)
    add_label_entry("Last Name:", validate_func=validate_alpha_space_dash)
    add_label_entry("Degree Program (e.g BSSTAT):", validate_func=lambda P: all(c.isalnum() or c.isspace() for c in P) or P == "")
    add_label_entry("Gender (M/F):", validate_func=validate_gender)
    add_label_entry("Academic Year (e.g., 2024-2025):", validate_func=validate_year_format)
    add_label_entry("Semester (e.g 1st Semester):")
    add_label_entry("Committee:")
    add_label_entry("Role:")
    add_label_entry("Batch Year:", validate_func=validate_numeric)
    add_label_entry("Batch Name:")
    add_label_entry("Status (Active/Inactive/Alumni/Suspended):")

    # Fetch current data from DB and populate entries
    try:
        connect.cur.execute("""
            SELECT mem_id, mem_uname, mem_pword, fname, mname, lname, degprog, gender
            FROM member
            WHERE mem_id = ?
        """, (member_id,))
        member = connect.cur.fetchone()
        if not member:
            messagebox.showerror("Error", f"No member found with ID {member_id}")
            on_close()
            return

        connect.cur.execute("""
            SELECT academic_year, committee, semester, org_role, batch_year, batch_name, mem_status
            FROM organization_has_member
            WHERE mem_id = ?
        """, (member_id,))
        org_member = connect.cur.fetchone()

        # Map DB fields to entries
        data_map = {
            "Member ID:": member[0],
            "Username:": member[1],
            "Password:": member[2],
            "First Name:": member[3],
            "Middle Name (optional):": member[4] or "",
            "Last Name:": member[5],
            "Degree Program (e.g BSSTAT):": member[6],
            "Gender (M/F):": member[7],
            "Academic Year (e.g., 2024-2025):": org_member[0] if org_member else "",
            "Committee:": org_member[1] if org_member else "",
            "Semester (e.g 1st Semester):": org_member[2] if org_member else "",
            "Role:": org_member[3] if org_member else "",
            "Batch Year:": org_member[4] if org_member else "",
            "Batch Name:": org_member[5] if org_member else "",
            "Status (Active/Inactive/Alumni/Suspended):": org_member[6] if org_member else "",
        }

        for label, (entry, _) in entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, str(data_map.get(label, "")))

    except Exception as e:
        messagebox.showerror("Database Error", f"Error fetching member data:\n{e}")
        on_close()
        return

    # Buttons frame
    btn_frame = tk.Frame(scrollable_frame, bg="#ffffff")
    btn_frame.pack(pady=20, fill='x', padx=10)

    def submit():
        data = {}
        for label, (entry, required) in entries.items():
            val = entry.get().strip()
            if required and not val:
                messagebox.showerror("Input Error", f"{label} is required.")
                return
            data[label] = val

        if data["Gender (M/F):"].upper() not in ('M', 'F'):
            messagebox.showerror("Input Error", "Gender must be M or F.")
            return

        try:
            # Update member table
            connect.cur.execute("""
                UPDATE member SET
                    mem_uname = ?, mem_pword = ?, fname = ?, mname = ?, lname = ?, degprog = ?, gender = ?
                WHERE mem_id = ?
            """, (
                data["Username:"],
                data["Password:"],
                data["First Name:"],
                data["Middle Name (optional):"] if data["Middle Name (optional):"] else None,
                data["Last Name:"],
                data["Degree Program (e.g BSSTAT):"],
                data["Gender (M/F):"].upper(),
                data["Member ID:"]
            ))

            # Update organization_has_member table
            connect.cur.execute("""
                UPDATE organization_has_member SET
                    academic_year = ?, committee = ?, semester = ?, org_role = ?, batch_year = ?, batch_name = ?, mem_status = ?
                WHERE mem_id = ? AND org_id = (
                    SELECT org_id FROM organization_has_member WHERE mem_id = ?
                )
            """, (
                data["Academic Year (e.g., 2024-2025):"],
                data["Committee:"],
                data["Semester (e.g 1st Semester):"],
                data["Role:"],
                data["Batch Year:"],
                data["Batch Name:"],
                data["Status (Active/Inactive/Alumni/Suspended):"],
                data["Member ID:"],
                data["Member ID:"]
            ))

            connect.conn.commit()
            messagebox.showinfo("Success", f"Member {data['First Name:']} {data['Last Name:']} updated successfully.")
            on_close()

        except Exception as e:
            messagebox.showerror("Database Error", f"Error updating member:\n{e}")

    submit_btn = tk.Button(btn_frame, text="Save Changes", bg=MAROON, fg="white", font=("Helvetica", 12, "bold"), command=submit)
    submit_btn.pack(side="left", expand=True, fill='x', padx=(0, 5), ipady=5)

    back_btn = tk.Button(btn_frame, text="Back", bg="#999999", fg="white", font=("Helvetica", 12, "bold"), command=on_close)
    back_btn.pack(side="right", expand=True, fill='x', padx=(5, 0), ipady=5)

    if parent_window:
        parent_window.withdraw()
