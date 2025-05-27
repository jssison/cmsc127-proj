import tkinter as tk
from tkinter import messagebox
from admin import connect

# Color scheme constants for UI styling
MAROON_COLOR = "#800000"
WHITE = "#ffffff"
BORDER_WIDTH = 1

# Utility to clear all widgets in a frame
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# Styles Entry widget with custom colors
def style_entry(entry):
    entry.config(bg=WHITE, fg=MAROON_COLOR, insertbackground=MAROON_COLOR, relief="solid", bd=BORDER_WIDTH)

# Styles Button widget with custom colors
def style_button(button):
    button.config(
        bg=WHITE, fg=MAROON_COLOR,
        activebackground="#f0f0f0", activeforeground=MAROON_COLOR,
        relief="solid", bd=BORDER_WIDTH, highlightthickness=0
    )

# Styles Label widget with custom colors
def style_label(label):
    label.config(bg=WHITE, fg=MAROON_COLOR)

# Prompts the user to input a Member ID and passes selected member to callback
def get_member(org_id, parent_window, callback):
    clear_frame(parent_window)
    parent_window.config(bg=WHITE)

    # Input field for member ID
    label = tk.Label(parent_window, text="Enter Member ID to edit:", font=("Helvetica", 12))
    style_label(label)
    label.pack(pady=10)
    mem_id_entry = tk.Entry(parent_window, font=("Helvetica", 11))
    style_entry(mem_id_entry)
    mem_id_entry.pack(pady=5)

    # On submit, validate and fetch member data
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

    # Back to edit menu
    back_btn = tk.Button(parent_window, text="Back", command=lambda: edit_member_menu(org_id, parent_window))
    style_button(back_btn)
    back_btn.pack(pady=5)

# Prompts for Fee Ref Number, fetches fee data, and calls callback
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
            SELECT * FROM member_pays_fee mpf 
            JOIN fee f ON mpf.fee_refnum = f.fee_refnum
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

# Main menu for editing member data
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

# Allows editing personal details of a member
def edit_member_details(org_id, mem_id, parent_window):
    clear_frame(parent_window)
    parent_window.config(bg=WHITE)

    connect.cur.execute("SELECT * FROM member WHERE mem_id = ?", (mem_id,))
    member = connect.cur.fetchone()
    if not member:
        messagebox.showerror("Error", "Member not found.")
        edit_member_menu(org_id, parent_window)
        return

    fname, mname, lname, uname, degprog, gender = member[3], member[4] or '', member[5], member[1], member[6], member[7]

    title = tk.Label(parent_window, text=f"Editing Member ID {mem_id}", font=("Helvetica", 16, "bold"))
    style_label(title)
    title.pack(pady=10)

    # Create input fields
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
        new_fname, new_mname, new_lname = entries[0].get().strip(), entries[1].get().strip() or None, entries[2].get().strip()
        new_uname, new_degprog, new_gender = entries[3].get().strip(), entries[4].get().strip(), entries[5].get().strip().upper()

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

# Edits membership-specific information (role, committee, etc.)
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

    # Extract fields
    committee, org_role, mem_status = org_mem[3], org_mem[5], org_mem[8]
    academic_year, semester, batch_year, batch_name = org_mem[2], org_mem[4], org_mem[6], org_mem[7]

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
        new_committee, new_role, new_status = entries[0].get().strip(), entries[1].get().strip(), entries[2].get().strip()
        new_acadyear, new_semester = entries[3].get().strip(), entries[4].get().strip()
        new_batchyear, new_batchname = entries[5].get().strip(), entries[6].get().strip()

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

# CONTINUED BELOW ⬇️ (Due to character limit)
