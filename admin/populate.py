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
            (2020678, 'gelolaville@gmail.com', 'gelogs', 'Gelo', NULL, 'Laville', 'BSSTAT', 'M'),
            (2022538, 'ginamath@gmail.com', 'ginamath', 'Gina', NULL, 'Math', 'BSSTAT', 'F'),
            (2023474, 'tyesoquin@gmail.com', 'tyesoq', 'Tyeso', 'R', 'Quin', 'BSSTAT', 'M'),
            (2021111, 'makiyum@gmail.com', 'makiy', 'Maki', 'F', 'Yum', 'BSSTAT', 'F'),
            (2021221, 'kayego@gmail.com', 'kayetrix', 'Kaye', 'T', 'Go', 'BSSTAT', 'F'),
            (2021234, 'algaeninz@gmail.com', 'algie', 'Algae', 'T', 'Ninz', 'BSCS', 'M'),
            (2020452, 'iskapreneur@gmail.com', 'iska', 'Iska', NULL, 'Preneur', 'BSCS', 'F'),
            (2022777, 'flovalo@gmail.com', 'flor', 'Flo', NULL, 'Valo', 'BSCS', 'M'),
            (2022779, 'angeleys@gmail.com', 'angeline', 'Angel', NULL, 'Eys', 'BSCS', 'F'),
            (2024345, 'christineyu@gmail.com', 'christy', 'Christine', NULL, 'Yu', 'BSCHE', 'F'),
            (2024987, 'asheleysab@gmail.com', 'ashsab', 'Asheley', NULL, 'Sab', 'BSCHE', 'F'),
            (2023387, 'jeemsaura@gmail.com', 'jeemar', 'Jeemar', NULL, 'Aura', 'BSCHE', 'M'),
            (2022187, 'willgo@gmail.com', 'will', 'Will', NULL, 'Go', 'BSCHE', 'M'),
            (2021087, 'blythebatumbs@gmail.com', 'blythe', 'Blythe', 'O', 'Batumbs', 'BSCHE', 'F');
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
            (1011, 'Membership Fee', '2024-05-15', '300', 1111),
            (1012, 'FRA Fee', '2025-05-15', '300', 1111),
            (1013, 'FRA Fee', '2024-01-10', '300', 1111),
            (1014, 'Membership Fee', '2024-05-15', '300', 1111),
            (1019, 'Membership Fee', '2025-06-30', '300', 1111),
            (1015, 'Membership Fee', '2025-06-10', '150', 2222),
            (1022, 'Event Fee', '2025-06-04', '200', 3333),
            (1050, 'Semestral Fee', '2025-01-10', '100', 2222),
            (1051, 'Semestral Fee', '2024-06-01', '150', 3333),
            (1052, 'Membership Fee', '2024-04-15', '150', 2222);
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
            (2222, 2023234, '2024-2025', 'Membership', '2nd Semester', 'Member', '2023', 'Coders', 'Active'),
            (1111, 2022123, '2023-2024', 'Executive', '1st Semester', 'Treasurer', '2022', 'Arima', 'Active'),
            (1111, 2024456, '2024-2025', 'Socials', '1st Semester', 'Member', '2024', 'Percentile', 'Active'),
            (3333, 2021345, '2023-2024', 'Finance', '2nd Semester', 'Member', '2021', 'Molecule', 'Suspended'),
            (1111, 2020678, '2023-2024', 'Executive', '2nd Semester', 'President', '2020', 'Concordance', 'Alumni'),
            (2222, 2022567, '2023-2024', 'Membership', '2nd Semester', 'Member', '2022', 'C', 'Suspended'),
            (1111, 2022538, '2024-2025', 'Scholastic', '1st Semester', 'Member', '2023', 'Range', 'Inactive'),
            (1111, 2023474, '2024-2025', 'Executive', '1st Semester', 'Treasurer', '2023', 'Range', 'Active'),
            (1111, 2021111, '2023-2024', 'Executive', '2nd Semester', 'President', '2023', 'Z', 'Alumni'),
            (1111, 2021221, '2024-2025', 'Membership', '2nd Semester', 'Member', '2022', 'Bivariate', 'Alumni'),
            (2222, 2021234, '2023-2024', 'Membership', '2nd Semester', 'Member', '2022', 'C', 'Inactive'),
            (2222, 2022777, '2024-2025', 'Finance', '1st Semester', 'Member', '2022', 'Python', 'Expelled'),
            (2222, 2020452, '2024-2025', 'Socials', '1st Semester', 'Member', '2021', 'Python', 'Alumni'),
            (2222, 2022779, '2023-2024', 'Membership', '2nd Semester', 'Member', '2023', 'Coders', 'Active'),
            (3333, 2024345, '2024-2025', 'Publicity', '1st Semester', 'Member', '2024', 'Chem', 'Active'),
            (3333, 2024987, '2024-2025', 'Scholastic', '1st Semester', 'Member', '2024', 'Chem', 'Active'),
            (3333, 2023387, '2023-2024', 'Scholastic', '2nd Semester', 'Member', '2023', 'Proton', 'Inactive'),
            (3333, 2022187, '2024-2025', 'Executive', '1st Semester', 'President', '2022', 'Ion', 'Active'),
            (3333, 2021087, '2023-2024', 'Executive', '2nd Semester', 'President', '2021', 'Electron', 'Alumni');
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
            (2024456, 1002, '2024-2025', '2nd Semester', '2025-01-23', 'Paid'),
            (2023474, 1001, '2024-2025', '2nd Semester', '0000-00-00', 'Not paid'),
            (2022123, 1011, '2023-2024', '2nd Semester', '2024-05-30', 'Paid'),
            (2024456, 1012, '2024-2025', '2nd Semester', '0000-00-00', 'Not paid'),
            (2022123, 1013, '2023-2024', '1st Semester', '0000-00-00', 'Not paid'),
            (2022123, 1014, '2023-2024', '2nd Semester', '2024-05-10', 'Paid'),
            (2022538, 1019, '2024-2025', '2nd Semester', '2025-02-09', 'Paid'),
            (2024987, 1022, '2024-2025', '2nd Semester', '0000-00-00', 'Not paid'),
            (2023387, 1051, '2023-2024', '2nd Semester', '2024-06-06', 'Not paid'),
            (2023234, 1050, '2024-2025', '1st Semester', '0000-00-00', 'Not paid'),
            (2023234, 1052, '2023-2024', '2nd Semester', '2024-03-10', 'Paid');
            """
        )
    except mariadb.Error as e:
        print(f'Error inserting into mem_pays_fee {e}')

    connection.commit()
