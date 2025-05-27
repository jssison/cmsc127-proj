import tkinter as tk
from tkinter import messagebox
from admin import connect

# Constants for consistent styling
MAROON_COLOR = "#800000"
WHITE = "#ffffff"
BORDER_WIDTH = 2

# Applies consistent styling to Entry widgets
def style_entry(entry):
    entry.config(bg=WHITE, fg=MAROON_COLOR, insertbackground=MAROON_COLOR, relief="solid", bd=BORDER_WIDTH)

# Applies consistent styling to Button widgets
def style_button(button):
    button.config(bg=WHITE, fg=MAROON_COLOR, activebackground="#f0f0f0", activeforeground=MAROON_COLOR,
                  relief="solid", bd=BORDER_WIDTH, highlightthickness=0)

# Applies consistent styling to Label widgets
def style_label(label):
    label.config(bg=WHITE, fg=MAROON_COLOR)

# Main function to handle member removal UI and logic
def remove_member(org_id, parent_window):
    """Displays the UI and logic to remove a member from the organization."""
    
    # Clear any existing widgets in the parent window
    def clear_frame():
        for widget in parent_window.winfo_children():
            widget.destroy()

    clear_frame()

    # Configure parent window styling
    parent_window.deiconify()
    parent_window.config(bg=WHITE)
    parent_window.update()  # Ensure updates are applied

    # Title label
    title = tk.Label(parent_window, text="REMOVE A MEMBER", font=("Helvetica", 16, "bold"))
    style_label(title)
    title.pack(pady=10)

    # Instruction label
    label = tk.Label(parent_window, text="Enter Member ID to remove:", font=("Helvetica", 12))
    style_label(label)
    label.pack(pady=5)

    # Entry widget to input member ID
    mem_id_entry = tk.Entry(parent_window, font=("Helvetica", 11))
    style_entry(mem_id_entry)
    mem_id_entry.pack(pady=5)

    # Logic for member removal when 'Remove Member' is clicked
    def submit():
        mem_id = mem_id_entry.get().strip()
        if not mem_id:
            messagebox.showerror("Error", "Please enter a Member ID.")
            return

        # Check if member exists in the organization
        connect.cur.execute("""
            SELECT * FROM organization_has_member
            WHERE mem_id = ? AND org_id = ?
        """, (mem_id, org_id))
        result = connect.cur.fetchone()

        if result:
            confirm = messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove member {mem_id}?")
            if confirm:
                # Delete from organization_has_member table
                connect.cur.execute("""
                    DELETE FROM organization_has_member
                    WHERE mem_id = ? AND org_id = ?
                """, (mem_id, org_id))

                # Delete related fee payments by the member for this org
                connect.cur.execute("""
                    DELETE FROM member_pays_fee
                    WHERE mem_id = ? AND fee_refnum IN (
                        SELECT fee_refnum FROM fee WHERE org_id = ?
                    )
                """, (mem_id, org_id))

                # Delete from the member table entirely
                connect.cur.execute("""
                    DELETE FROM member
                    WHERE mem_id = ?
                """, (mem_id,))

                # Save all changes
                connect.conn.commit()
                messagebox.showinfo("Success", f"Member {mem_id} has been removed.")
                mem_id_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "No such member found in this organization.")

    # Submit button
    submit_btn = tk.Button(parent_window, text="Remove Member", command=submit)
    style_button(submit_btn)
    submit_btn.pack(pady=10)

    # Navigation back to dashboard or previous menu
    def go_back():
        # Trigger a custom event that other windows can bind to (useful for modular navigation)
        parent_window.event_generate("<<BackToDashboard>>")

    # Back button
    back_btn = tk.Button(parent_window, text="Back", command=go_back)
    style_button(back_btn)
    back_btn.pack(pady=5)
