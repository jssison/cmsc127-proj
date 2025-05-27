from admin import connect


def remove_member(org_id):
    print("\n========== Remove a Member ==========")
    mem_id = input("Enter the Member ID to remove from this organization: ")

    # First check if the member is part of the org
    connect.cur.execute("""
        SELECT * FROM organization_has_member
        WHERE mem_id = ? AND org_id = ?
    """, (mem_id, org_id))
    result = connect.cur.fetchone()

    if result:
        confirm = input(f"Are you sure you want to remove member {mem_id}? (y/n): ")
        if confirm.lower() == 'y':
            # Remove from organization_has_member
            connect.cur.execute("""
                DELETE FROM organization_has_member
                WHERE mem_id = ? AND org_id = ?
            """, (mem_id, org_id))

            #remove their fee payment records too
            connect.cur.execute("""
                DELETE FROM member_pays_fee
                WHERE mem_id = ? AND fee_refnum IN (
                    SELECT fee_refnum FROM fee WHERE org_id = ?
                )
            """, (mem_id, org_id))

            # Remove from member table
            connect.cur.execute("""
                DELETE FROM member
                WHERE mem_id = ?
            """, (mem_id,))

            connect.conn.commit()
            print(f"Member with {mem_id} has been removed from organization.")
        else:
            print("Cancelled.")
    else:
        print("No such member found under this organization.")
