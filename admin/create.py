import mariadb

# creating the entity organization with the following attributes and constraints
def create_org(cursor, connection):
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS organization(
            org_id INT AUTO_INCREMENT,  
            org_name VARCHAR(50) NOT NULL, 
            org_username VARCHAR(50) NOT NULL,
            org_password VARCHAR(50) NOT NULL,
            CONSTRAINT organization_org_id_pk PRIMARY KEY (org_id), 
            CONSTRAINT organization_org_username_uk UNIQUE (org_username) 
        );
        """
        )
    except mariadb.Error as e:
        print(f'Error creating organization table {e}')

    connection.commit()

# creating the entity member with the following attributes and constraints
def create_mem(cursor, connection):
    try:
        cursor.execute( """
        CREATE TABLE IF NOT EXISTS member(
            mem_id INT AUTO_INCREMENT, 
            mem_uname VARCHAR(50) NOT NULL,
            mem_pword VARCHAR(50) NOT NULL,
            fname VARCHAR(50) NOT NULL,
            mname VARCHAR(50),
            lname VARCHAR(50) NOT NULL,
            degprog VARCHAR(50) NOT NULL,
            gender CHAR(1) NOT NULL,
            CONSTRAINT member_mem_id_pk PRIMARY KEY(mem_id), 
            CONSTRAINT member_mem_uname_uk UNIQUE (mem_uname) 
        );
        """
        )
    except mariadb.Error as e:
        print(f'Error creating member table {e}')

    connection.commit()

# creating the entity fee with the following attributes and constraints
def create_fee(cursor, connection):
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS fee(
            fee_refnum INT AUTO_INCREMENT,
            category VARCHAR(20) NOT NULL, 
            due_date DATE NOT NULL,
            amount INT NOT NULL,
            org_id INT(20) NOT NULL,
            CONSTRAINT fee_fee_refnum_pk PRIMARY KEY(fee_refnum), 
            CONSTRAINT fee_org_id_fk FOREIGN KEY(org_id) REFERENCES organization(org_id) 
        );
        """
        )
    except mariadb.Error as e:
        print(f'Error creating fee table {e}')

    connection.commit()

# creating the organization_has_member with the following relationship attributes and constraints
def create_orghasmem(cursor, connection):
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS organization_has_member(
            org_id INT NOT NULL, 
            mem_id INT NOT NULL,
            academic_year VARCHAR(9) NOT NULL,
            committee VARCHAR(50) NOT NULL,
            semester VARCHAR(20) NOT NULL,
            org_role VARCHAR(50) NOT NULL,
            batch_year YEAR NOT NULL,
            batch_name VARCHAR(50) NOT NULL,
            mem_status VARCHAR(10) NOT NULL,
            CONSTRAINT organization_has_member_org_id_pk PRIMARY KEY (org_id, mem_id, academic_year, committee,
            semester, org_role, batch_year, mem_status), 
            CONSTRAINT organization_has_member_org_id_fk FOREIGN KEY (org_id) REFERENCES organization(org_id), 
            CONSTRAINT organization_has_member_mem_id_fk FOREIGN KEY (mem_id) REFERENCES member(mem_id) 
        );
        """
        )
    except mariadb.Error as e:
        print(f'Error creating org_has_mem table {e}')

    connection.commit()

# creating the organization_has_member with the following relationship attributes and constraints
def create_mempaysfee(cursor, connection):
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS member_pays_fee (
            mem_id INT NOT NULL, 
            fee_refnum INT NOT NULL,
            academic_year VARCHAR(9) NOT NULL,
            semester VARCHAR(20) NOT NULL,
            date_of_payment DATE,
            payment_status VARCHAR(20) NOT NULL,
            CONSTRAINT member_pays_fee_mem_id_pk PRIMARY KEY (mem_id, fee_refnum, academic_year, semester, date_of_payment, payment_status),
            CONSTRAINT member_pays_fee_mem_id_fk FOREIGN KEY (mem_id) REFERENCES member(mem_id), 
            CONSTRAINT member_pays_fee_fee_refnum_fk FOREIGN KEY (fee_refnum) REFERENCES fee(fee_refnum)
        );
        """
        )
    except mariadb.Error as e:
        print(f'Error creating mem_pays_fee table {e}')

    connection.commit()
