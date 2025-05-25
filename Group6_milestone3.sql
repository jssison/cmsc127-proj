--creates table for organization entity including all its important attributes
CREATE TABLE organization(
	org_id INT AUTO_INCREMENT, --automatically increment integer digits based on the values encoded 
	org_name VARCHAR(50) NOT NULL, --NOT NULL syntax does not allow no value input for the said attributes
	org_username VARCHAR(50) NOT NULL,
	org_password VARCHAR(50) NOT NULL,
	CONSTRAINT organization_org_id_pk PRIMARY KEY (org_id), --sets organization_id as primary key
	CONSTRAINT organization_org_username_uk UNIQUE (org_username) --ensures that the username is unique and won't be duplicated 
);


--creates table for member entity including all its important attributes
CREATE TABLE member(
    mem_id INT AUTO_INCREMENT, --automatically increment integer digits based on the values encoded 
    mem_uname VARCHAR(50) NOT NULL, --NOT NULL syntax does not allow no value input for the said attributes
    mem_pword VARCHAR(50) NOT NULL,
    fname VARCHAR(50) NOT NULL,
    mname VARCHAR(50),
    lname VARCHAR(50) NOT NULL,
    degprog VARCHAR(50) NOT NULL,
    gender CHAR(1) NOT NULL,
    CONSTRAINT member_mem_id_pk PRIMARY KEY(mem_id), --sets mem_id as primary key of a member
    CONSTRAINT member_mem_uname_uk UNIQUE (mem_uname) --makes sure that the username is not yet existing or no duplication
);


--creates table for fee entity including all its important attributes
CREATE TABLE fee(
    fee_refnum INT(10),
    category VARCHAR(20) NOT NULL, --NOT NULL syntax does not allow no value input for the said attributes
    due_date DATE NOT NULL,
    amount INT NOT NULL,
    org_id INT(20) NOT NULL,
    CONSTRAINT fee_fee_refnum_pk PRIMARY KEY(fee_refnum), --sets fee_refnum as primary key of fee
    CONSTRAINT fee_org_id_fk FOREIGN KEY(org_id) REFERENCES organization(org_id) --references org_id to make sure proper alignment of fee with respective orgs
);


--table containing data of members that are part of the organizations
CREATE TABLE organization_has_member(
    org_id INT NOT NULL, --NOT NULL syntax does not allow no value input for the said attributes
    mem_id INT NOT NULL,
    academic_year VARCHAR(9) NOT NULL,
    committee VARCHAR(50) NOT NULL,
    semester VARCHAR(20) NOT NULL,
    org_role VARCHAR(50) NOT NULL,
    batch_year YEAR NOT NULL,
    batch_name VARCHAR(50) NOT NULL,
    mem_status VARCHAR(10) NOT NULL,
    CONSTRAINT organization_has_member_org_id_pk PRIMARY KEY (org_id, mem_id, academic_year, committee,
    semester, org_role, batch_year, mem_status), --combination of these attributes correctly specify the member of said org
    CONSTRAINT organization_has_member_org_id_fk FOREIGN KEY (org_id) REFERENCES organization(org_id), --references organization_id from entity organization
    CONSTRAINT organization_has_member_mem_id_fk FOREIGN KEY (mem_id) REFERENCES member(mem_id) --references mem_id from member to ensure that the said member is existing
);


--table containing the fees that the members have paid or yet to pay
CREATE TABLE member_pays_fee (
    mem_id INT NOT NULL, --NOT NULL syntax does not allow no value input for the said attributes
    fee_refnum INT NOT NULL,
    academic_year VARCHAR(9) NOT NULL,
    semester VARCHAR(20) NOT NULL,
    date_of_payment DATE,
    payment_status VARCHAR(20) NOT NULL,
	CONSTRAINT member_pays_fee_mem_id_pk PRIMARY KEY (mem_id, fee_refnum, academic_year, semester, date_of_payment, payment_status),
    CONSTRAINT member_pays_fee_mem_id_fk FOREIGN KEY (mem_id) REFERENCES member(mem_id), --references mem_id and fee_refnum for member and fee respectively to ensure proper alignment of the said fee to the member
    CONSTRAINT member_pays_fee_fee_refnum_fk FOREIGN KEY (fee_refnum) REFERENCES fee(fee_refnum)
);

--Dummy Data Insertions

--sample data for different organization with its respective attributes
INSERT INTO organization VALUES
    (1111, 'Statistics Society', 'statsoc@gmail.com', 'statsOnTop'),
    (2222, 'Computer Science Society', 'cmscsoc@gmail.com', 'cmscsocdabest'),
    (3333, 'Chemistry Society', 'chemsoc@gmail.com', 'chemsocgogogo');


--sample data for different members of an org with their respective attributes that correctly classify them
INSERT INTO member VALUES
    (2022123, 'anademarces10@gmail.com', 'anamaganda', 'Ana', 'Z', 'Demarces', 'BSSTAT', 'F'),
    (2023234, 'gianraymundo2@gmail.com', 'gianpogi', 'Gian', NULL, 'Raymundo', 'BSCS', 'M'),
    (2021345, 'kimmyumali@gmail.com', 'kimmyruth', 'Kimmy', NULL, 'Umali', 'BSCHE', 'F'),
    (2024456, 'tinasacay@gmail.com', 'tina123', 'Tina', 'T', 'Sacay', 'BSSTAT', 'F'),
    (2022567, 'monmonilag@gmail.com', 'monmon', 'Monmon', 'Q', 'Ilag', 'BSCS', 'M'),
    (2020678, 'gelolaville@gmail.com', 'gelogs', 'Gelo', NULL, 'Laville', 'BSSTAT', 'M');

--sample data of fees that the members will paid or have paid with respective attributes
INSERT INTO fee VALUES
    (1001, 'Membership Fee', '2025-05-30', '150', 1111),
    (1002, 'Semestral Fee', '2025-06-10', '100', 1111),
    (1010, 'FRA Fee', '2025-05-15', '300', 1111),
    (1015, 'Membership Fee', '2025-05-30', '150', 2222),
    (1022, 'Event Fee', '2025-06-04', '200', 3333),
    (1050, 'Semestral Fee', '2025-06-01', '100', 2222),
    (1051, 'Semestral Fee', '2025-06-01', '150', 3333),
    (1052, 'Membership Fee', '2025-05-31', '150', 2222);

--sample data that correctly references an existing member to an existing organization
INSERT INTO organization_has_member VALUES
    (2222, 2023234, '2024-2025', 'Executive', '2nd Semester', 'President', '2023', 'Coders', 'Active'),
    (1111, 2022123, '2023-2024', 'Executive', '1st Semester', 'Treasurer', '2022', 'Arima', 'Inactive'),
    (1111, 2024456, '2024-2025', 'Socials', '1st Semester', 'Member', '2024', 'Percentile', 'Active'),
    (3333, 2021345, '2023-2024', 'Finance', '2nd Semester', 'Member', '2021', 'Molecule', 'Suspended'),
    (1111, 2020678, '2024-2025', 'Executive', '2nd Semester', 'Membership Head', '2020', 'Concordance', 'Alumni'),
    (2222, 2022567, '2023-2024', 'Membership', '2nd Semester', 'Member', '2022', 'C', 'Suspended');

--sample data that correctly classifies the fee in an organization that a member has paid/not paid
INSERT INTO member_pays_fee VALUES 
    (2023234, 1015, '2024-2025', '2nd Semester', '2025-04-30', 'Paid'),
    (2024456, 1002, '2024-2025', '1st Semester', '204-11-23', 'Paid'),
    (2021345, 1022, '2024-2025', '2nd Semester', NULL, 'Not Paid');

-- Reports

-- #1
--Member details per member of an org
CREATE VIEW members_by_details AS
	SELECT mem.mem_id AS `Membership ID`, 
	CASE
        WHEN mem.mname IS NOT NULL AND mem.mname != ''
            THEN CONCAT(mem.fname, ' ', mem.mname, ' ', mem.lname)
        ELSE CONCAT(mem.fname, ' ', mem.lname)
    END AS `Full Name`, 
	orgmem.org_role AS `Role`,
	orgmem.mem_status AS `Status`, 
	mem.gender AS `Gender`, 
	mem.degprog AS `Degree Program`, 
	orgmem.batch_year AS `Batch year`, 
	orgmem.committee AS `Committee`
	FROM member AS mem JOIN organization_has_member AS orgmem ON 
	mem.mem_id = orgmem.mem_id;

-- #2
--Display members with unpaid fees based on payment status
CREATE VIEW member_with_unpaid_membership_fees AS
	SELECT 
		m.mem_id AS `Membership ID`,
		CONCAT(m.fname, ' ', IFNULL(m.mname, ''), IF(m.mname IS NOT NULL, ' ', ''), m.lname) AS `Full Name`,
		m.degprog AS `Degree Program`,
		m.gender AS `Gender`,
		ohm.org_id AS `Organization`,
		mpf.academic_year AS `Academic Year`,
		mpf.semester AS `Semester`
	FROM member m
	JOIN organization_has_member ohm
		ON m.mem_id = ohm.mem_id
	JOIN member_pays_fee mpf
		ON m.mem_id = mpf.mem_id
	WHERE mpf.payment_status = 'Not Paid';


-- #3
--Check payment status of each payment made by members 
--if it is unpaid, include them on the view
CREATE VIEW unpaid_member_fees AS	
	SELECT fee.fee_refnum AS `Fee reference number`, 
	fee.category AS `Category`, 
	fee.due_date AS `Due date`, 
	fee.amount AS `Amount`, 
	org.org_name AS `Organization Name`, 
	mem_fee.academic_year AS `Academic Year`, 
	mem_fee.semester AS `Semester`, 
	mem_fee.payment_status AS `Payment Status` 
	FROM  member AS mem JOIN member_pays_fee AS mem_fee 
	ON mem.mem_id = mem_fee.mem_id
	JOIN fee ON mem_fee.fee_refnum = fee.fee_refnum
	JOIN organization AS org
	ON fee.org_id = org.org_id
	WHERE mem_fee.payment_status = 'Not Paid';

-- #4
--Check member's committee if they are in the executive committee
CREATE VIEW executive_committee_members AS
	SELECT mem.mem_id AS `Membership ID`,
	CASE
        WHEN mem.mname IS NOT NULL AND mem.mname != ''
            THEN CONCAT(mem.fname, ' ', mem.mname, ' ', mem.lname)
        ELSE CONCAT(mem.fname, ' ', mem.lname)
    END AS `Full Name`, 
	org.org_name AS `Organization name`, 
	orgmem.academic_year AS `Academic year`
	FROM member AS mem JOIN organization_has_member AS orgmem
	ON mem.mem_id = orgmem.mem_id 
	JOIN organization AS org 
	ON orgmem.org_id = org.org_id
	WHERE orgmem.committee = 'Executive';

-- #5
--Display presidents/specified role of a given org per academic year 
CREATE VIEW presidents AS
	SELECT mem.mem_id AS `Membership ID`,
	CASE
        WHEN mem.mname IS NOT NULL AND mem.mname != ''
            THEN CONCAT(mem.fname, ' ', mem.mname, ' ', mem.lname)
        ELSE CONCAT(mem.fname, ' ', mem.lname)
    END AS `Full Name`,  
	orgmem.org_role AS `Role`,
	org.org_name AS `Organization name`,
	orgmem.academic_year AS `Academic year`
	FROM member AS mem JOIN organization_has_member AS orgmem
	ON mem.mem_id = orgmem.mem_id
	JOIN organization AS org
	ON orgmem.org_id = org.org_id
	WHERE orgmem.org_role = 'President'
	ORDER BY orgmem.academic_year DESC;

-- #6
--Display late payments based on payment date and due date
CREATE VIEW late_payments_view AS
	SELECT 
		m.mem_id AS `Membership ID`,
		CONCAT(m.fname, ' ', IFNULL(m.mname, ''), IF(m.mname IS NOT NULL, ' ', ''), m.lname) AS `Full Name`,
		m.degprog AS `Degree Program`,
		m.gender AS `Gender`,
		ohm.org_id AS `Organization ID`,
		mpf.academic_year AS `Academic Year`,
		mpf.semester AS `Semester`,
		f.fee_refnum AS `Fee Reference`,
		f.due_date AS `Due Date`,
		mpf.date_of_payment AS `Date of Payment`,
		mpf.payment_status AS `Payment Status`
	FROM member m
	JOIN organization_has_member ohm
		ON m.mem_id = ohm.mem_id
	JOIN member_pays_fee mpf
		ON m.mem_id = mpf.mem_id
	JOIN fee f
		ON mpf.fee_refnum = f.fee_refnum
	WHERE mpf.date_of_payment > f.due_date;

-- #7
--Display active vs inactive member percantage based on member status
CREATE VIEW active_vs_inactive_percentage AS 
	SELECT 
		academic_year,
		semester,
		COUNT(*) AS total_members,
		SUM(mem_status = 'Active') AS active_count,
		SUM(mem_status = 'Inactive') AS inactive_count,
		ROUND((SUM(mem_status = 'Active') / COUNT(*)) * 100, 2) AS active_percentage,
		ROUND((SUM(mem_status = 'Inactive') / COUNT(*)) * 100, 2) AS inactive_percentage
	FROM 
		organization_has_member
	WHERE 
		organization_id = organization_id
	GROUP BY 
		academic_year, semester
	ORDER BY 
		academic_year DESC, semester DESC;

-- #8
--Display alumni members of a given org
CREATE VIEW alumni_members AS
SELECT mem.mem_id AS `Membership ID`,
    CASE
        WHEN mem.mname IS NOT NULL AND mem.mname != ''
            THEN CONCAT(mem.fname, ' ', mem.mname, ' ', mem.lname)
        ELSE CONCAT(mem.fname, ' ', mem.lname)
    END AS `Full Name`,
    org.org_name AS `Organization Name`
FROM member AS mem JOIN organization_has_member AS orgmem 
ON mem.mem_id = orgmem.mem_id 
JOIN organization AS org 
ON orgmem.org_id = org.org_id 
WHERE orgmem.mem_status = 'Alumni';


-- #9
--Display total amount of paid and unpaid fees
CREATE VIEW total_unpaid AS
SELECT o.org_name,
    -- Total Paid Amount (before or on today)
    COALESCE(SUM(
        CASE
            WHEN mpf.payment_status = 'Paid' AND mpf.date_of_payment <= CURRENT_DATE THEN f.amount
            ELSE 0 END), 0) AS total_paid_amount,    COALESCE(SUM(
        CASE 
            WHEN f.due_date <= CURRENT_DATE AND 
                 (mpf.payment_status = 'Not Paid' OR mpf.date_of_payment > CURRENT_DATE)
            THEN f.amount
            ELSE 0 END), 0) AS total_unpaid_amount

FROM organization o
JOIN fee f ON o.org_id = f.org_id
JOIN member_pays_fee mpf ON f.fee_refnum = mpf.fee_refnum
GROUP BY o.org_name;


-- #10
-- Display member details with the highest debt of a given org for a given sem
CREATE VIEW highest_debt 
	SELECT m.mem_id,
	m.fname,
	m.lname,
	SUM(CASE
	WHEN mpf.payment_status != 'Paid' THEN f.amount ELSE 0 END) AS unpaid_amount
	FROM member m
	JOIN member_pays_fee mpf ON m.mem_id = mpf.mem_id
	JOIN fee f ON mpf.fee_refnum = f.fee_refnum
	WHERE f.org_id = given_organization_id
	And mpf.semester = given_semester
	GROUP BY m.mem_id, m.fname,m.lname
	ORDER BY unpaid_amount DESC	;	

-- Delete data
DELETE FROM organization_has_member;
DELETE FROM member_pays_fee;
DELETE FROM fee;
DELETE FROM member;
DELETE FROM organization;