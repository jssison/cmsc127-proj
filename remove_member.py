import tkinter as tk
from tkinter import messagebox
from admin import connect

MAROON_COLOR = "#800000"
WHITE = "#ffffff"
BORDER_WIDTH = 2

def style_entry(entry):
    entry.config(bg=WHITE, fg=MAROON_COLOR, insertbackground=MAROON_COLOR, relief="solid", bd=BORDER_WIDTH)

def style_button(button):
    button.config(bg=WHITE, fg=MAROON_COLOR, activebackground="#f0f0f0", activeforeground=MAROON_COLOR,
                  relief="solid", bd=BORDER_WIDTH, highlightthickness=0)

def style_label(label):
    label.config(bg=WHITE, fg=MAROON_COLOR)

def remove_member(org_id, parent_window):
    def clear_frame():
        for widget in parent_window.winfo_children():
            widget.destroy()

    clear_frame()
    parent_window.config(bg=WHITE)

    title = tk.Label(parent_window, text="REMOVE A MEMBER", font=("Helvetica", 16, "bold"))
    style_label(title)
    title.pack(pady=10)

    label = tk.Label(parent_window, text="Enter Member ID to remove:", font=("Helvetica", 12))
    style_label(label)
    label.pack(pady=5)

    mem_id_entry = tk.Entry(parent_window, font=("Helvetica", 11))
    style_entry(mem_id_entry)
    mem_id_entry.pack(pady=5)

    def submit():
        mem_id = mem_id_entry.get().strip()
        if not mem_id:
            messagebox.showerror("Error", "Please enter a Member ID.")
            return

        connect.cur.execute("""
            SELECT * FROM organization_has_member
            WHERE mem_id = ? AND org_id = ?
        """, (mem_id, org_id))
        result = connect.cur.fetchone()

        if result:
            confirm = messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove member {mem_id}?")
            if confirm:
                # Delete from organization_has_member
                connect.cur.execute("""
                    DELETE FROM organization_has_member
                    WHERE mem_id = ? AND org_id = ?
                """, (mem_id, org_id))

                # Delete related fees
                connect.cur.execute("""
                    DELETE FROM member_pays_fee
                    WHERE mem_id = ? AND fee_refnum IN (
                        SELECT fee_refnum FROM fee WHERE org_id = ?
                    )
                """, (mem_id, org_id))

                # Delete from member table
                connect.cur.execute("""
                    DELETE FROM member
                    WHERE mem_id = ?
                """, (mem_id,))

                connect.conn.commit()
                messagebox.showinfo("Success", f"Member {mem_id} has been removed.")
                mem_id_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "No such member found in this organization.")

    submit_btn = tk.Button(parent_window, text="Remove Member", command=submit)
    style_button(submit_btn)
    submit_btn.pack(pady=10)

    back_btn = tk.Button(parent_window, text="Back", command=lambda: parent_window.event_generate("<<BackToDashboard>>"))
    style_button(back_btn)
    back_btn.pack(pady=5)
