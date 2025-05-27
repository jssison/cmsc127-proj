import tkinter as tk
from tkinter import messagebox
import re

from admin import connect

def add_member_gui(org_id, parent_window=None):
    add_win = tk.Toplevel()
    add_win.title("Add New Member")
    add_win.geometry("450x650")
    add_win.configure(bg="#ffffff")

    MAROON = "#800000"
    FONT_LABEL = ("Helvetica", 11)
    FONT_ENTRY = ("Helvetica", 11)

    def on_close():
        if parent_window:
            parent_window.deiconify()
        add_win.destroy()

    add_win.protocol("WM_DELETE_WINDOW", on_close)

    # Create canvas + scrollbar for scrolling form
    canvas = tk.Canvas(add_win, bg="#ffffff", highlightthickness=0)
    scrollbar = tk.Scrollbar(add_win, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#ffffff")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tk.Label(scrollable_frame, text="Add a New Member", font=("Helvetica", 16, "bold"), fg=MAROON, bg="#ffffff").pack(pady=10)

    entries = {}

    # --- Validators ---
    def validate_alnum(P):
        return P.isalnum() or P == ""

    def validate_numeric(P):
        return P.isdigit() or P == ""

    def validate_alpha_space_dash(P):
        # Letters, spaces, or hyphen allowed
        return all(c.isalpha() or c.isspace() or c == '-' for c in P) or P == ""

    def validate_gender(P):
        return P.upper() in ("M", "F", "")  # Allow empty for editing

    def validate_year_format(P):
        # Matches "" or digits or digits-digits (e.g. 2024-2025)
        return re.fullmatch(r"(\d{0,4}(-\d{0,4})?)?", P) is not None

    def validate_numeric(P):
        return P.isdigit() or P == ""

    # Helper to add label+entry with optional validation
    def add_label_entry(text, required=True, validate_func=None):
        tk.Label(scrollable_frame, text=text, font=FONT_LABEL, fg=MAROON, bg="#ffffff", anchor="w").pack(fill='x', pady=(10, 0), padx=10)
        if validate_func:
            vcmd = add_win.register(validate_func)
            ent = tk.Entry(scrollable_frame, font=FONT_ENTRY, bg="#f9f9f9", fg=MAROON,
                           validate="key", validatecommand=(vcmd, '%P'))
        else:
            ent = tk.Entry(scrollable_frame, font=FONT_ENTRY, bg="#f9f9f9", fg=MAROON)
        ent.pack(fill='x', pady=(0, 5), padx=10)
        entries[text] = (ent, required)

    # Add fields with validation where appropriate
    add_label_entry("Member ID:", validate_func=validate_numeric)
    add_label_entry("Username:")
    add_label_entry("Password:")  # No validation, free text
    add_label_entry("First Name:", validate_func=validate_alpha_space_dash)
    add_label_entry("Middle Name (optional):", required=False, validate_func=validate_alpha_space_dash)
    add_label_entry("Last Name:", validate_func=validate_alpha_space_dash)
    add_label_entry("Degree Program (e.g BSSTAT):", validate_func=lambda P: all(c.isalnum() or c.isspace() for c in P) or P == "")
    add_label_entry("Gender (M/F):", validate_func=validate_gender)
    add_label_entry("Academic Year (e.g., 2024-2025):", validate_func=validate_year_format)
    add_label_entry("Semester (e.g 1st Semester):")  # free text
    add_label_entry("Committee:")  # free text
    add_label_entry("Role:")  # free text
    add_label_entry("Batch Year:", validate_func=validate_numeric)
    add_label_entry("Batch Name:")  # free text
    add_label_entry("Status (Active/Inactive/Alumni/Suspended):")  # free text, ideally dropdown

    # Buttons frame inside scrollable frame
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

        # Extra validation on gender for safety
        if data["Gender (M/F):"].upper() not in ('M', 'F'):
            messagebox.showerror("Input Error", "Gender must be M or F.")
            return

        try:
            connect.cur.execute("""
                INSERT INTO member (mem_id, mem_uname, mem_pword, fname, mname, lname, degprog, gender)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data["Member ID:"],
                data["Username:"],
                data["Password:"],
                data["First Name:"],
                data["Middle Name (optional):"] if data["Middle Name (optional):"] else None,
                data["Last Name:"],
                data["Degree Program (e.g BSSTAT):"],
                data["Gender (M/F):"].upper()
            ))

            connect.cur.execute("""
                INSERT INTO organization_has_member (
                    org_id, mem_id, academic_year, committee,
                    semester, org_role, batch_year, batch_name, mem_status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                org_id,
                data["Member ID:"],
                data["Academic Year (e.g., 2024-2025):"],
                data["Committee:"],
                data["Semester (e.g 1st Semester):"],
                data["Role:"],
                data["Batch Year:"],
                data["Batch Name:"],
                data["Status (Active/Inactive/Alumni/Suspended):"]
            ))

            connect.conn.commit()
            messagebox.showinfo("Success", f"Member {data['First Name:']} {data['Last Name:']} has been added successfully.")
            on_close()

        except Exception as e:
            messagebox.showerror("Database Error", f"Error adding member:\n{e}")

    submit_btn = tk.Button(btn_frame, text="Add Member", bg=MAROON, fg="white", font=("Helvetica", 12, "bold"), command=submit)
    submit_btn.pack(side="left", expand=True, fill='x', padx=(0, 5), ipady=5)

    back_btn = tk.Button(btn_frame, text="Back", bg="#999999", fg="white", font=("Helvetica", 12, "bold"), command=on_close)
    back_btn.pack(side="right", expand=True, fill='x', padx=(5, 0), ipady=5)

    if parent_window:
        parent_window.withdraw()

