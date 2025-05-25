import mariadb

def insert_to_org(cursor, connection):
    try:
        cursor.execute(
            """
            INSERT INTO organization VALUES
            (1111, 'Statistics Society', 'statsoc@gmail.com', 'statsOnTop'),
            (2222, 'Computer Science Society', 'cmscsoc@gmail.com', 'cmscsocdabest'),
            (3333, 'Chemistry Society', 'chemsoc@gmail.com', 'chemsocgogogo');
            """
        )
    except mariadb.Error as e:
        print(f'Error inserting into organization {e}')
    
    connection.commit()

def insert_to_mem(cursor, connection):
    try:
        cursor.execute(
            """
            INSERT INTO member VALUES
            (2022123, 'anademarces10@gmail.com', 'anamaganda', 'Ana', 'Z', 'Demarces', 'BSSTAT', 'F'),
            (2023234, 'gianraymundo2@gmail.com', 'gianpogi', 'Gian', NULL, 'Raymundo', 'BSCS', 'M'),
            (2021345, 'kimmyumali@gmail.com', 'kimmyruth', 'Kimmy', NULL, 'Umali', 'BSCHE', 'F'),
            (2024456, 'tinasacay@gmail.com', 'tina123', 'Tina', 'T', 'Sacay', 'BSSTAT', 'F'),
            (2022567, 'monmonilag@gmail.com', 'monmon', 'Monmon', 'Q', 'Ilag', 'BSCS', 'M'),
            (2020678, 'gelolaville@gmail.com', 'gelogs', 'Gelo', NULL, 'Laville', 'BSSTAT', 'M');
            """
        )
    except mariadb.Error as e:
        print(f'Error inserting into member {e}')

    connection.commit()

def insert_to_fee(cursor, connection):
    try:
        cursor.execute(
            """
            INSERT INTO fee VALUES
            (1001, 'Membership Fee', '2025-05-30', '150', 1111),
            (1002, 'Semestral Fee', '2025-06-10', '100', 1111),
            (1010, 'FRA Fee', '2025-05-15', '300', 1111),
            (1015, 'Membership Fee', '2025-05-30', '150', 2222),
            (1022, 'Event Fee', '2025-06-04', '200', 3333),
            (1050, 'Semestral Fee', '2025-06-01', '100', 2222),
            (1051, 'Semestral Fee', '2025-06-01', '150', 3333),
            (1052, 'Membership Fee', '2025-05-31', '150', 2222);
            """
        )
    except mariadb.Error as e:
        print(f'Error inserting into fee {e}')

    connection.commit()

def insert_to_orghasmem(cursor, connection):
    try:
        cursor.execute(
            """
            INSERT INTO organization_has_member VALUES
            (2222, 2023234, '2024-2025', 'Executive', '2nd Semester', 'President', '2023', 'Coders', 'Active'),
            (1111, 2022123, '2023-2024', 'Executive', '1st Semester', 'Treasurer', '2022', 'Arima', 'Inactive'),
            (1111, 2024456, '2024-2025', 'Socials', '1st Semester', 'Member', '2024', 'Percentile', 'Active'),
            (3333, 2021345, '2023-2024', 'Finance', '2nd Semester', 'Member', '2021', 'Molecule', 'Suspended'),
            (1111, 2020678, '2024-2025', 'Executive', '2nd Semester', 'Membership Head', '2020', 'Concordance', 'Alumni'),
            (2222, 2022567, '2023-2024', 'Membership', '2nd Semester', 'Member', '2022', 'C', 'Suspended');
            """
        )
    except mariadb.Error as e:
        print(f'Error inserting into org_has_mem {e}')

    connection.commit()

def insert_to_mempaysfee(cursor, connection):
    try:
        cursor.execute(
            """
            INSERT INTO member_pays_fee VALUES 
            (2023234, 1015, '2024-2025', '2nd Semester', '2025-04-30', 'Paid'),
            (2024456, 1002, '2024-2025', '1st Semester', '2024-11-23', 'Paid'),
            (2021345, 1022, '2024-2025', '2nd Semester', '2024-10-13', 'Paid');
            """
        )
    except mariadb.Error as e:
        print(f'Error inserting into mem_pays_fee {e}')

    connection.commit()