import tkinter as tk
from tkinter import messagebox
from admin import connect

# Updated color scheme
MAROON_COLOR = "#800000"
WHITE = "#ffffff"
BORDER_WIDTH = 1

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def style_entry(entry):
    entry.config(bg=WHITE, fg=MAROON_COLOR, insertbackground=MAROON_COLOR, relief="solid", bd=BORDER_WIDTH)

def style_button(button):
    button.config(
        bg=WHITE, fg=MAROON_COLOR,
        activebackground="#f0f0f0", activeforeground=MAROON_COLOR,
        relief="solid", bd=BORDER_WIDTH, highlightthickness=0
    )

def style_label(label):
    label.config(bg=WHITE, fg=MAROON_COLOR)

def get_member(org_id, parent_window, callback):
    clear_frame(parent_window)
    parent_window.config(bg=WHITE)

    label = tk.Label(parent_window, text="Enter Member ID to edit:", font=("Helvetica", 12))
    style_label(label)
    label.pack(pady=10)
    mem_id_entry = tk.Entry(parent_window, font=("Helvetica", 11))
    style_entry(mem_id_entry)
    mem_id_entry.pack(pady=5)

    def submit():
        mem_id = mem_id_entry.get().strip()
        if not mem_id:
            messagebox.showerror("Error", "Member ID cannot be empty.")
            return
        connect.cur.execute("""
            SELECT * FROM organization_has_member ohm 
            JOIN member m ON ohm.mem_id = m.mem_id 
            WHERE ohm.mem_id = ? AND ohm.org_id = ?
        """, (mem_id, org_id))
        member = connect.cur.fetchone()
        if member:
            callback(member, mem_id)
        else:
            messagebox.showerror("Error", "No such member found under this organization.")

    submit_btn = tk.Button(parent_window, text="Submit", command=submit)
    style_button(submit_btn)
    submit_btn.pack(pady=10)

    back_btn = tk.Button(parent_window, text="Back", command=lambda: edit_member_menu(org_id, parent_window))
    style_button(back_btn)
    back_btn.pack(pady=5)

def get_fee(org_id, mem_id, parent_window, callback):
    clear_frame(parent_window)
    parent_window.config(bg=WHITE)

    label = tk.Label(parent_window, text="Enter Fee Reference Number to edit:", font=("Helvetica", 12))
    style_label(label)
    label.pack(pady=10)
    fee_ref_entry = tk.Entry(parent_window, font=("Helvetica", 11))
    style_entry(fee_ref_entry)
    fee_ref_entry.pack(pady=5)

    def submit_fee():
        fee_refnum = fee_ref_entry.get().strip()
        if not fee_refnum:
            messagebox.showerror("Error", "Fee Reference Number cannot be empty.")
            return
        connect.cur.execute("""
            SELECT * FROM member_pays_fee mpf JOIN fee f ON mpf.fee_refnum = f.fee_refnum
            WHERE mpf.mem_id = ? AND f.org_id = ? AND mpf.fee_refnum = ?
        """, (mem_id, org_id, fee_refnum))
        fee = connect.cur.fetchone()
        if fee:
            callback(fee, fee_refnum)
        else:
            messagebox.showerror("Error", "No fee found for this member under this organization.")

    submit_btn = tk.Button(parent_window, text="Submit", command=submit_fee)
    style_button(submit_btn)
    submit_btn.pack(pady=10)

    back_btn = tk.Button(parent_window, text="Back", command=lambda: edit_mem_fees(org_id, mem_id, parent_window))
    style_button(back_btn)
    back_btn.pack(pady=5)

def edit_member_menu(org_id, parent_window):
    clear_frame(parent_window)
    parent_window.config(bg=WHITE)

    title = tk.Label(parent_window, text="EDIT MEMBER MENU", font=("Helvetica", 16, "bold"))
    style_label(title)
    title.pack(pady=20)

    buttons = [
        ("Edit Member Details", lambda: get_member(org_id, parent_window, lambda m, mid: edit_member_details(org_id, mid, parent_window))),
        ("Edit Organization Membership", lambda: get_member(org_id, parent_window, lambda m, mid: edit_org_membership(org_id, mid, parent_window))),
        ("Add Member Fees", lambda: add_mem_fees(org_id, parent_window)),
        ("Edit Member Fees", lambda: get_member(org_id, parent_window, lambda m, mid: edit_mem_fees(org_id, mid, parent_window))),
        ("Back to Dashboard", lambda: parent_window.event_generate("<<BackToDashboard>>"))
    ]

    for text, cmd in buttons[:-1]:
        btn = tk.Button(parent_window, text=text, width=25, command=cmd)
        style_button(btn)
        btn.pack(pady=5)

    last_btn = tk.Button(parent_window, text=buttons[-1][0], width=25, command=buttons[-1][1])
    style_button(last_btn)
    last_btn.pack(pady=20)

def edit_member_details(org_id, mem_id, parent_window):
    clear_frame(parent_window)
    parent_window.config(bg=WHITE)

    connect.cur.execute("SELECT * FROM member WHERE mem_id = ?", (mem_id,))
    member = connect.cur.fetchone()
    if not member:
        messagebox.showerror("Error", "Member not found.")
        edit_member_menu(org_id, parent_window)
        return

    fname = member[3]
    mname = member[4] or ''
    lname = member[5]
    uname = member[1]
    degprog = member[6]
    gender = member[7]

    title = tk.Label(parent_window, text=f"Editing Member ID {mem_id}", font=("Helvetica", 16, "bold"))
    style_label(title)
    title.pack(pady=10)

    labels_and_entries = [
        ("First Name:", fname),
        ("Middle Name (optional):", mname),
        ("Last Name:", lname),
        ("Username:", uname),
        ("Degree Program:", degprog),
        ("Gender (M/F):", gender)
    ]

    entries = []
    for text, val in labels_and_entries:
        lbl = tk.Label(parent_window, text=text)
        style_label(lbl)
        lbl.pack()
        ent = tk.Entry(parent_window)
        ent.insert(0, val)
        style_entry(ent)
        ent.pack()
        entries.append(ent)

    def save():
        new_fname = entries[0].get().strip()
        new_mname = entries[1].get().strip() or None
        new_lname = entries[2].get().strip()
        new_uname = entries[3].get().strip()
        new_degprog = entries[4].get().strip()
        new_gender = entries[5].get().strip().upper()

        if not new_fname or not new_lname or not new_uname or not new_degprog or new_gender not in ['M', 'F']:
            messagebox.showerror("Error", "Please fill all fields correctly.")
            return

        connect.cur.execute("""
            UPDATE member SET fname=?, mname=?, lname=?, mem_uname=?, degprog=?, gender=?
            WHERE mem_id=?
        """, (new_fname, new_mname, new_lname, new_uname, new_degprog, new_gender, mem_id))
        connect.conn.commit()
        messagebox.showinfo("Success", f"Member {mem_id} updated successfully.")
        edit_member_menu(org_id, parent_window)

    save_btn = tk.Button(parent_window, text="Save Changes", command=save)
    style_button(save_btn)
    save_btn.pack(pady=15)

    back_btn = tk.Button(parent_window, text="Back", command=lambda: edit_member_menu(org_id, parent_window))
    style_button(back_btn)
    back_btn.pack()

def edit_org_membership(org_id, mem_id, parent_window):
    clear_frame(parent_window)
    parent_window.config(bg=WHITE)

    connect.cur.execute("""
        SELECT * FROM organization_has_member WHERE mem_id = ? AND org_id = ?
    """, (mem_id, org_id))
    org_mem = connect.cur.fetchone()
    if not org_mem:
        messagebox.showerror("Error", "Membership details not found.")
        edit_member_menu(org_id, parent_window)
        return

    committee = org_mem[3]
    org_role = org_mem[5]
    mem_status = org_mem[8]
    academic_year = org_mem[2]
    semester = org_mem[4]
    batch_year = org_mem[6]
    batch_name = org_mem[7]

    title = tk.Label(parent_window, text=f"Edit Membership for Member {mem_id}", font=("Helvetica", 16, "bold"))
    style_label(title)
    title.pack(pady=10)

    labels_and_values = [
        ("Committee:", committee),
        ("Role:", org_role),
        ("Status (Active/Inactive/Alumni/Suspended):", mem_status),
        ("Academic Year (e.g., 2024-2025):", academic_year),
        ("Semester (1st Semester/2nd Semester):", semester),
        ("Batch Year:", batch_year),
        ("Batch Name:", batch_name)
    ]

    entries = []
    for label_text, val in labels_and_values:
        lbl = tk.Label(parent_window, text=label_text)
        style_label(lbl)
        lbl.pack()
        ent = tk.Entry(parent_window)
        ent.insert(0, val)
        style_entry(ent)
        ent.pack()
        entries.append(ent)

    def save_membership():
        new_committee = entries[0].get().strip()
        new_role = entries[1].get().strip()
        new_status = entries[2].get().strip()
        new_acadyear = entries[3].get().strip()
        new_semester = entries[4].get().strip()
        new_batchyear = entries[5].get().strip()
        new_batchname = entries[6].get().strip()

        if not all([new_committee, new_role, new_status, new_acadyear, new_semester, new_batchyear, new_batchname]):
            messagebox.showerror("Error", "Please fill all fields.")
            return

        connect.cur.execute("""
            UPDATE organization_has_member 
            SET committee=?, org_role=?, mem_status=?, academic_year=?, semester=?, batch_year=?, batch_name=?
            WHERE mem_id=? AND org_id=?
        """, (new_committee, new_role, new_status, new_acadyear, new_semester, new_batchyear, new_batchname, mem_id, org_id))
        connect.conn.commit()
        messagebox.showinfo("Success", f"Membership details for member {mem_id} updated.")
        edit_member_menu(org_id, parent_window)

    save_btn = tk.Button(parent_window, text="Save Changes", command=save_membership)
    style_button(save_btn)
    save_btn.pack(pady=15)

    back_btn = tk.Button(parent_window, text="Back", command=lambda: edit_member_menu(org_id, parent_window))
    style_button(back_btn)
    back_btn.pack()

def add_mem_fees(org_id, parent_window):
    clear_frame(parent_window)
    parent_window.config(bg=WHITE)

    title = tk.Label(parent_window, text="Add Member Fees", font=("Helvetica", 16, "bold"))
    style_label(title)
    title.pack(pady=10)

    labels = ["Member ID:", "Fee Reference Number:", "Payment Date (YYYY-MM-DD):"]
    entries = []
    for text in labels:
        lbl = tk.Label(parent_window, text=text)
        style_label(lbl)
        lbl.pack()
        ent = tk.Entry(parent_window)
        style_entry(ent)
        ent.pack()
        entries.append(ent)

    def save_fee():
        mem_id = entries[0].get().strip()
        fee_refnum = entries[1].get().strip()
        payment_date = entries[2].get().strip()

        if not mem_id or not fee_refnum or not payment_date:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        connect.cur.execute("SELECT * FROM organization_has_member WHERE mem_id=? AND org_id=?", (mem_id, org_id))
        if not connect.cur.fetchone():
            messagebox.showerror("Error", "Member does not belong to this organization.")
            return

        try:
            connect.cur.execute("""
                INSERT INTO member_pays_fee (mem_id, fee_refnum, date_of_payment) VALUES (?, ?, ?)
            """, (mem_id, fee_refnum, payment_date))
            connect.conn.commit()
            messagebox.showinfo("Success", "Fee added successfully.")
            edit_member_menu(org_id, parent_window)
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")

    add_fee_btn = tk.Button(parent_window, text="Add Fee", command=save_fee)
    style_button(add_fee_btn)
    add_fee_btn.pack(pady=15)

    back_btn = tk.Button(parent_window, text="Back", command=lambda: edit_member_menu(org_id, parent_window))
    style_button(back_btn)
    back_btn.pack()

def edit_mem_fees(org_id, mem_id, parent_window):
    clear_frame(parent_window)
    parent_window.config(bg=WHITE)

    connect.cur.execute("""
        SELECT mpf.fee_refnum, mpf.date_of_payment, f.fee_name 
        FROM member_pays_fee mpf JOIN fee f ON mpf.fee_refnum = f.fee_refnum
        WHERE mpf.mem_id = ? AND f.org_id = ?
    """, (mem_id, org_id))
    fees = connect.cur.fetchall()
    if not fees:
        messagebox.showinfo("Info", "No fees found for this member.")
        edit_member_menu(org_id, parent_window)
        return

    title = tk.Label(parent_window, text=f"Fees for Member {mem_id}", font=("Helvetica", 16, "bold"))
    style_label(title)
    title.pack(pady=10)

    for fee_refnum, payment_date, fee_name in fees:
        fee_str = f"Ref#: {fee_refnum} | {fee_name} | Paid on: {payment_date}"
        frame = tk.Frame(parent_window, bg=WHITE)
        frame.pack(fill="x", pady=2, padx=5)

        lbl = tk.Label(frame, text=fee_str, bg=WHITE, fg=MAROON_COLOR)
        lbl.pack(side="left")

        edit_btn = tk.Button(frame, text="Edit", command=lambda ref=fee_refnum: edit_fee_detail(org_id, mem_id, ref, parent_window))
        style_button(edit_btn)
        edit_btn.pack(side="right")

    back_btn = tk.Button(parent_window, text="Back", command=lambda: edit_member_menu(org_id, parent_window))
    style_button(back_btn)
    back_btn.pack(pady=15)

def edit_fee_detail(org_id, mem_id, fee_refnum, parent_window):
    clear_frame(parent_window)
    parent_window.config(bg=WHITE)

    connect.cur.execute("""
        SELECT * FROM member_pays_fee WHERE mem_id = ? AND fee_refnum = ?
    """, (mem_id, fee_refnum))
    fee = connect.cur.fetchone()
    if not fee:
        messagebox.showerror("Error", "Fee record not found.")
        edit_mem_fees(org_id, mem_id, parent_window)
        return

    title = tk.Label(parent_window, text=f"Edit Fee {fee_refnum} for Member {mem_id}", font=("Helvetica", 16, "bold"))
    style_label(title)
    title.pack(pady=10)

    lbl = tk.Label(parent_window, text="Payment Date (YYYY-MM-DD):")
    style_label(lbl)
    lbl.pack()
    payment_date_entry = tk.Entry(parent_window)
    payment_date_entry.insert(0, fee[2])
    style_entry(payment_date_entry)
    payment_date_entry.pack()

    def save_fee_changes():
        new_date = payment_date_entry.get().strip()
        if not new_date:
            messagebox.showerror("Error", "Payment date cannot be empty.")
            return
        connect.cur.execute("""
            UPDATE member_pays_fee SET date_of_payment=? WHERE mem_id=? AND fee_refnum=?
        """, (new_date, mem_id, fee_refnum))
        connect.conn.commit()
        messagebox.showinfo("Success", "Fee updated successfully.")
        edit_mem_fees(org_id, mem_id, parent_window)

    save_btn = tk.Button(parent_window, text="Save Changes", command=save_fee_changes)
    style_button(save_btn)
    save_btn.pack(pady=15)

    back_btn = tk.Button(parent_window, text="Back", command=lambda: edit_mem_fees(org_id, mem_id, parent_window))
    style_button(back_btn)
    back_btn.pack()
