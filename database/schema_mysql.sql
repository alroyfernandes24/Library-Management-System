-- ==============================================================
-- DATABASE SCHEMA: MySQL (For MySQL Workbench / phpMyAdmin / XAMPP)
-- Project: Library Management System (DBMS Mini Project)
-- ==============================================================

DROP DATABASE IF EXISTS library_db;
CREATE DATABASE library_db;
USE library_db;

-- --------------------------------------------------------------
-- 1. Table: categories
-- --------------------------------------------------------------
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
) ENGINE=InnoDB;

-- --------------------------------------------------------------
-- 2. Table: authors
-- --------------------------------------------------------------
CREATE TABLE authors (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    author_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    biography TEXT
) ENGINE=InnoDB;

-- --------------------------------------------------------------
-- 3. Table: books
-- --------------------------------------------------------------
CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    isbn VARCHAR(20) NOT NULL UNIQUE,
    title VARCHAR(200) NOT NULL,
    category_id INT,
    publication_year INT,
    total_copies INT NOT NULL DEFAULT 1,
    available_copies INT NOT NULL DEFAULT 1,
    CONSTRAINT chk_total_copies CHECK (total_copies >= 0),
    CONSTRAINT chk_avail_copies CHECK (available_copies >= 0 AND available_copies <= total_copies),
    CONSTRAINT fk_books_category FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- --------------------------------------------------------------
-- 4. Table: book_authors (Many-to-Many Junction Table)
-- --------------------------------------------------------------
CREATE TABLE book_authors (
    book_id INT NOT NULL,
    author_id INT NOT NULL,
    PRIMARY KEY (book_id, author_id),
    CONSTRAINT fk_ba_book FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    CONSTRAINT fk_ba_author FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- --------------------------------------------------------------
-- 5. Table: members
-- --------------------------------------------------------------
CREATE TABLE members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15),
    membership_date DATE NOT NULL,
    membership_type ENUM('Student', 'Faculty', 'General') DEFAULT 'Student',
    status ENUM('Active', 'Suspended', 'Expired') DEFAULT 'Active',
    max_books_allowed INT DEFAULT 3,
    CONSTRAINT chk_max_books CHECK (max_books_allowed > 0)
) ENGINE=InnoDB;

-- --------------------------------------------------------------
-- 6. Table: borrow_transactions
-- --------------------------------------------------------------
CREATE TABLE borrow_transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE DEFAULT NULL,
    status ENUM('Issued', 'Returned', 'Overdue') DEFAULT 'Issued',
    CONSTRAINT fk_bt_book FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    CONSTRAINT fk_bt_member FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- --------------------------------------------------------------
-- 7. Table: fines
-- --------------------------------------------------------------
CREATE TABLE fines (
    fine_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT NOT NULL UNIQUE,
    member_id INT NOT NULL,
    fine_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    paid_status ENUM('Unpaid', 'Paid') DEFAULT 'Unpaid',
    paid_date DATE DEFAULT NULL,
    CONSTRAINT fk_fine_trans FOREIGN KEY (transaction_id) REFERENCES borrow_transactions(transaction_id) ON DELETE CASCADE,
    CONSTRAINT fk_fine_member FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- --------------------------------------------------------------
-- 8. Table: audit_logs (Audit Trail for DBMS)
-- --------------------------------------------------------------
CREATE TABLE audit_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    action_type VARCHAR(20) NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ==============================================================
-- TRIGGERS (Automated Business Logic)
-- ==============================================================

DELIMITER //

CREATE TRIGGER trg_after_issue_book
AFTER INSERT ON borrow_transactions
FOR EACH ROW
BEGIN
    IF NEW.status = 'Issued' THEN
        UPDATE books 
        SET available_copies = available_copies - 1
        WHERE book_id = NEW.book_id;

        INSERT INTO audit_logs (table_name, action_type, description)
        VALUES ('borrow_transactions', 'ISSUE', CONCAT('Book ID ', NEW.book_id, ' issued to Member ID ', NEW.member_id));
    END IF;
END//

CREATE TRIGGER trg_after_return_book
AFTER UPDATE ON borrow_transactions
FOR EACH ROW
BEGIN
    DECLARE overdue_days INT;
    DECLARE calculated_fine DECIMAL(10,2);

    IF OLD.return_date IS NULL AND NEW.return_date IS NOT NULL THEN
        UPDATE books 
        SET available_copies = available_copies + 1
        WHERE book_id = NEW.book_id;

        INSERT INTO audit_logs (table_name, action_type, description)
        VALUES ('borrow_transactions', 'RETURN', CONCAT('Book ID ', NEW.book_id, ' returned by Member ID ', NEW.member_id));

        IF NEW.return_date > NEW.due_date THEN
            SET overdue_days = DATEDIFF(NEW.return_date, NEW.due_date);
            SET calculated_fine = overdue_days * 5.00;

            INSERT INTO fines (transaction_id, member_id, fine_amount, paid_status)
            VALUES (NEW.transaction_id, NEW.member_id, calculated_fine, 'Unpaid');
        END IF;
    END IF;
END//

CREATE TRIGGER trg_before_issue_check
BEFORE INSERT ON borrow_transactions
FOR EACH ROW
BEGIN
    DECLARE v_available INT;
    DECLARE v_status VARCHAR(20);
    DECLARE v_current_issued INT;
    DECLARE v_max_allowed INT;

    SELECT available_copies INTO v_available FROM books WHERE book_id = NEW.book_id;
    IF v_available <= 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error: Cannot issue book. No copies currently available!';
    END IF;

    SELECT status, max_books_allowed INTO v_status, v_max_allowed FROM members WHERE member_id = NEW.member_id;
    IF v_status != 'Active' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error: Member is not Active. Cannot issue book!';
    END IF;

    SELECT COUNT(*) INTO v_current_issued 
    FROM borrow_transactions 
    WHERE member_id = NEW.member_id AND return_date IS NULL;

    IF v_current_issued >= v_max_allowed THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error: Member has already reached maximum allowed borrow limit!';
    END IF;
END//

-- ==============================================================
-- STORED PROCEDURES
-- ==============================================================

CREATE PROCEDURE sp_IssueBook(
    IN p_member_id INT,
    IN p_book_id INT,
    IN p_loan_days INT,
    OUT p_message VARCHAR(150)
)
BEGIN
    DECLARE v_avail INT;
    DECLARE v_status VARCHAR(20);
    DECLARE v_issued_count INT;
    DECLARE v_max_allowed INT;
    DECLARE v_due_date DATE;

    SELECT available_copies INTO v_avail FROM books WHERE book_id = p_book_id;
    SELECT status, max_books_allowed INTO v_status, v_max_allowed FROM members WHERE member_id = p_member_id;

    IF v_avail <= 0 THEN
        SET p_message = 'Failed: Book is currently out of stock!';
    ELSEIF v_status != 'Active' THEN
        SET p_message = 'Failed: Member account is not active!';
    ELSE
        SELECT COUNT(*) INTO v_issued_count FROM borrow_transactions WHERE member_id = p_member_id AND return_date IS NULL;
        IF v_issued_count >= v_max_allowed THEN
            SET p_message = 'Failed: Member maximum borrowing quota reached!';
        ELSE
            SET v_due_date = DATE_ADD(CURDATE(), INTERVAL p_loan_days DAY);
            INSERT INTO borrow_transactions (book_id, member_id, issue_date, due_date, status)
            VALUES (p_book_id, p_member_id, CURDATE(), v_due_date, 'Issued');
            SET p_message = 'Success: Book issued successfully!';
        END IF;
    END IF;
END//

CREATE PROCEDURE sp_ReturnBook(
    IN p_transaction_id INT,
    OUT p_message VARCHAR(150),
    OUT p_fine DECIMAL(10,2)
)
BEGIN
    DECLARE v_due_date DATE;
    DECLARE v_already_returned DATE;
    DECLARE v_days_overdue INT;

    SELECT return_date, due_date INTO v_already_returned, v_due_date 
    FROM borrow_transactions 
    WHERE transaction_id = p_transaction_id;

    IF v_already_returned IS NOT NULL THEN
        SET p_message = 'Notice: Book has already been returned!';
        SET p_fine = 0.00;
    ELSE
        UPDATE borrow_transactions 
        SET return_date = CURDATE(), status = 'Returned'
        WHERE transaction_id = p_transaction_id;

        IF CURDATE() > v_due_date THEN
            SET v_days_overdue = DATEDIFF(CURDATE(), v_due_date);
            SET p_fine = v_days_overdue * 5.00;
            SET p_message = CONCAT('Book returned late by ', v_days_overdue, ' days. Fine imposed: Rs. ', p_fine);
        ELSE
            SET p_fine = 0.00;
            SET p_message = 'Book returned on time. No fine imposed!';
        END IF;
    END IF;
END//

CREATE PROCEDURE sp_PayFine(
    IN p_fine_id INT,
    OUT p_message VARCHAR(100)
)
BEGIN
    DECLARE v_status VARCHAR(10);
    SELECT paid_status INTO v_status FROM fines WHERE fine_id = p_fine_id;

    IF v_status = 'Paid' THEN
        SET p_message = 'Fine has already been settled!';
    ELSE
        UPDATE fines 
        SET paid_status = 'Paid', paid_date = CURDATE() 
        WHERE fine_id = p_fine_id;
        SET p_message = 'Fine paid successfully!';
    END IF;
END//

DELIMITER ;

-- ==============================================================
-- VIEWS
-- ==============================================================

CREATE OR REPLACE VIEW vw_book_catalog AS
SELECT 
    b.book_id,
    b.isbn,
    b.title,
    c.category_name,
    IFNULL(GROUP_CONCAT(a.author_name SEPARATOR ', '), 'Unknown') AS authors,
    b.publication_year,
    b.total_copies,
    b.available_copies,
    CASE 
        WHEN b.available_copies > 0 THEN 'Available'
        ELSE 'Out of Stock'
    END AS status
FROM books b
LEFT JOIN categories c ON b.category_id = c.category_id
LEFT JOIN book_authors ba ON b.book_id = ba.book_id
LEFT JOIN authors a ON ba.author_id = a.author_id
GROUP BY b.book_id, b.isbn, b.title, c.category_name, b.publication_year, b.total_copies, b.available_copies;

CREATE OR REPLACE VIEW vw_active_loans AS
SELECT 
    t.transaction_id,
    t.book_id,
    b.title AS book_title,
    t.member_id,
    CONCAT(m.first_name, ' ', m.last_name) AS member_name,
    m.email AS member_email,
    m.phone AS member_phone,
    t.issue_date,
    t.due_date,
    GREATEST(0, DATEDIFF(CURDATE(), t.due_date)) AS overdue_days,
    CASE 
        WHEN CURDATE() > t.due_date THEN 'Overdue'
        ELSE 'Active'
    END AS loan_status
FROM borrow_transactions t
JOIN books b ON t.book_id = b.book_id
JOIN members m ON t.member_id = m.member_id
WHERE t.return_date IS NULL;

CREATE OR REPLACE VIEW vw_outstanding_fines AS
SELECT 
    f.fine_id,
    f.transaction_id,
    m.member_id,
    CONCAT(m.first_name, ' ', m.last_name) AS member_name,
    m.email,
    m.phone,
    b.title AS book_title,
    f.fine_amount,
    f.paid_status
FROM fines f
JOIN members m ON f.member_id = m.member_id
JOIN borrow_transactions t ON f.transaction_id = t.transaction_id
JOIN books b ON t.book_id = b.book_id
WHERE f.paid_status = 'Unpaid';

CREATE OR REPLACE VIEW vw_library_summary AS
SELECT 
    (SELECT COUNT(*) FROM books) AS total_titles,
    (SELECT SUM(total_copies) FROM books) AS total_volumes,
    (SELECT SUM(available_copies) FROM books) AS available_volumes,
    (SELECT COUNT(*) FROM members WHERE status = 'Active') AS active_members,
    (SELECT COUNT(*) FROM borrow_transactions WHERE return_date IS NULL) AS currently_borrowed,
    (SELECT IFNULL(SUM(fine_amount), 0) FROM fines WHERE paid_status = 'Unpaid') AS pending_fines_amount;

-- ==============================================================
-- DUMMY / SAMPLE DATA (50 Books, 30 Authors, 10 Categories, 30 Members)
-- ==============================================================

-- Categories
INSERT INTO categories (category_id, category_name, description) VALUES
(1, 'Computer Science & Software Eng.', 'Data structures, algorithms, databases, operating systems, and architectures'),
(2, 'Mathematics & Statistics', 'Discrete mathematics, calculus, linear algebra, and probability theory'),
(3, 'Literature & World Classics', 'Dystopian fiction, classical English literature, poetry, and drama'),
(4, 'Electronics & IoT', 'Digital electronics, microprocessors, signal processing, and embedded systems'),
(5, 'Management & Entrepreneurship', 'Business strategy, startups, finance, organizational leadership'),
(6, 'Artificial Intelligence & Data Science', 'Deep learning, neural networks, machine learning, NLP, and computer vision'),
(7, 'Physics & Mechanical Engineering', 'Quantum mechanics, thermodynamics, fluid dynamics, and astrophysics'),
(8, 'Psychology, Soft Skills & Productivity', 'Behavioral psychology, habit formation, communication, and cognitive science'),
(9, 'Civil & Structural Engineering', 'Strength of materials, fluid mechanics, structural design, and surveying'),
(10, 'Cyber Security & Cloud Infrastructure', 'Cryptography, network defense, distributed systems, cloud computing, and DevOps');

-- Authors
INSERT INTO authors (author_id, author_name, email, biography) VALUES
(1, 'Abraham Silberschatz', 'silberschatz@db-book.com', 'Professor of CS, Yale University. Renowned author of Database and OS books.'),
(2, 'Henry F. Korth', 'korth@db-book.com', 'Professor of CS, Lehigh University. Co-author of Database System Concepts.'),
(3, 'Robert C. Martin', 'unclebob@cleancoder.com', 'Known as "Uncle Bob", author of Clean Code and agile software advocate.'),
(4, 'Thomas H. Cormen', 'thc@clrs-book.com', 'Emeritus Professor at Dartmouth College, lead author of CLRS Algorithms.'),
(5, 'George Orwell', 'george@classicauthors.org', 'English novelist and essayist, author of 1984 and Animal Farm.'),
(6, 'Donald Knuth', 'knuth@cs.stanford.edu', 'Turing Award recipient, author of The Art of Computer Programming.'),
(7, 'Stuart Russell', 'russell@cs.berkeley.edu', 'Professor of Computer Science at UC Berkeley, author of AI: A Modern Approach.'),
(8, 'Peter Norvig', 'norvig@norvig.com', 'Distinguished Education Fellow at Stanford, former Director of Research at Google.'),
(9, 'Ian Goodfellow', 'ian@deeplearningbook.org', 'Creator of Generative Adversarial Networks (GANs), lead author of Deep Learning.'),
(10, 'Yoshua Bengio', 'yoshua@mila.quebec', 'Turing Award laureate, pioneer in deep learning and recurrent networks.'),
(11, 'Martin Fowler', 'fowler@thoughtworks.com', 'Chief Scientist at ThoughtWorks, author of Refactoring and Patterns of EAA.'),
(12, 'Bjarne Stroustrup', 'bjarne@stroustrup.com', 'Inventor and designer of C++, professor of Computer Science at Columbia.'),
(13, 'Richard P. Feynman', 'feynman@caltech.edu', 'Nobel laureate in Physics, creator of Feynman diagrams and quantum physics lectures.'),
(14, 'James Clear', 'james@jamesclear.com', 'Speaker and bestselling author of Atomic Habits.'),
(15, 'Peter Thiel', 'thiel@foundersfund.com', 'Venture capitalist, co-founder of PayPal and Palantir, author of Zero to One.'),
(16, 'Andrew S. Tanenbaum', 'ast@cs.vu.nl', 'Author of Modern Operating Systems and Computer Networks, creator of MINIX.'),
(17, 'Brian W. Kernighan', 'bwk@cs.princeton.edu', 'Pioneer at Bell Labs, co-author of The C Programming Language (K&R).'),
(18, 'Dennis Ritchie', 'dmr@bell-labs.com', 'Turing Award laureate, creator of the C programming language and co-creator of Unix.'),
(19, 'Linus Torvalds', 'torvalds@kernel.org', 'Creator and principal developer of the Linux kernel and Git version control.'),
(20, 'Guido van Rossum', 'guido@python.org', 'Creator and Benevolent Dictator for Life (BDFL) of Python programming language.'),
(21, 'Yann LeCun', 'yann@meta.com', 'Turing Award laureate, Chief AI Scientist at Meta, pioneer of Convolutional Networks.'),
(22, 'Geoffrey Hinton', 'hinton@cs.toronto.edu', 'Nobel and Turing laureate, godfather of modern deep learning and backpropagation.'),
(23, 'Stephen Hawking', 'hawking@cam.ac.uk', 'Theoretical physicist, cosmologist, author of A Brief History of Time.'),
(24, 'Yuval Noah Harari', 'harari@huji.ac.il', 'Historian and philosopher, author of international bestseller Sapiens.'),
(25, 'Daniel Kahneman', 'kahneman@princeton.edu', 'Nobel laureate in Economic Sciences, author of Thinking, Fast and Slow.'),
(26, 'Dale Carnegie', 'carnegie@associates.org', 'Author of How to Win Friends and Influence People, leadership trainer.'),
(27, 'Walter Isaacson', 'isaacson@aspeninstitute.org', 'Biographer of Steve Jobs, Albert Einstein, Benjamin Franklin, and Leonardo da Vinci.'),
(28, 'Sun Tzu', 'suntzu@ancientstrategy.org', 'Ancient Chinese military general, strategist, and philosopher.'),
(29, 'Carl Sagan', 'sagan@cornell.edu', 'Astronomer, planetary scientist, and science communicator, author of Cosmos.'),
(30, 'Michael Sipser', 'sipser@math.mit.edu', 'Professor of Applied Mathematics at MIT, author of Theory of Computation.');

-- Books
INSERT INTO books (book_id, isbn, title, category_id, publication_year, total_copies, available_copies) VALUES
(1, '978-0078022159', 'Database System Concepts (6th Edition)', 1, 2011, 8, 7),
(2, '978-0132350884', 'Clean Code: A Handbook of Agile Software Craftsmanship', 1, 2008, 6, 5),
(3, '978-0262033848', 'Introduction to Algorithms (CLRS 3rd Ed)', 1, 2009, 7, 6),
(4, '978-0451524935', '1984', 3, 1949, 10, 10),
(5, '978-0201896831', 'The Art of Computer Programming, Vol 1', 1, 1997, 5, 5),
(6, '978-0131103627', 'The C Programming Language (ANSI C)', 1, 1988, 7, 7),
(7, '978-0134444321', 'Discrete Mathematics and Its Applications', 2, 2018, 6, 6),
(8, '978-0073380377', 'Digital Design: Principles and Practices', 4, 2017, 5, 5),
(9, '978-0134610993', 'Artificial Intelligence: A Modern Approach (4th Ed)', 6, 2020, 8, 7),
(10, '978-0262035613', 'Deep Learning (Adaptive Computation & ML)', 6, 2016, 7, 6),
(11, '978-0134757599', 'Refactoring: Improving the Design of Existing Code', 1, 2018, 5, 5),
(12, '978-0321563842', 'The C++ Programming Language (4th Edition)', 1, 2013, 6, 5),
(13, '978-0465024933', 'The Feynman Lectures on Physics, Vol 1', 7, 1963, 6, 6),
(14, '978-0735211292', 'Atomic Habits: An Easy & Proven Way to Build Good Habits', 8, 2018, 10, 9),
(15, '978-0804139298', 'Zero to One: Notes on Startups, or How to Build the Future', 5, 2014, 6, 5),
(16, '978-1119320913', 'Operating System Concepts (10th Edition)', 1, 2018, 8, 7),
(17, '978-0134494166', 'Clean Architecture: A Craftsman''s Guide to Software Structure', 1, 2017, 6, 6),
(18, '978-0321982384', 'Linear Algebra and Its Applications (5th Ed)', 2, 2015, 6, 6),
(19, '978-0201633610', 'Design Patterns: Elements of Reusable Object-Oriented Software', 1, 1994, 6, 6),
(20, '978-0060850524', 'Brave New World', 3, 1932, 7, 7),
(21, '978-0133591620', 'Modern Operating Systems (4th Edition)', 1, 2014, 6, 5),
(22, '978-0132126953', 'Computer Networks (5th Edition)', 1, 2010, 7, 6),
(23, '978-1133187790', 'Introduction to the Theory of Computation (3rd Ed)', 1, 2012, 5, 5),
(24, '978-0262510875', 'Structure and Interpretation of Computer Programs (SICP)', 1, 1996, 4, 4),
(25, '978-0553380163', 'A Brief History of Time', 7, 1988, 8, 7),
(26, '978-0062316097', 'Sapiens: A Brief History of Humankind', 8, 2015, 9, 8),
(27, '978-0374533557', 'Thinking, Fast and Slow', 8, 2011, 7, 7),
(28, '978-0671027032', 'How to Win Friends and Influence People', 8, 1936, 8, 8),
(29, '978-1451648539', 'Steve Jobs: The Exclusive Biography', 5, 2011, 6, 6),
(30, '978-1599869773', 'The Art of War', 5, 2007, 7, 7),
(31, '978-0345539434', 'Cosmos: A Personal Voyage', 7, 1980, 6, 6),
(32, '978-1617294433', 'Deep Learning with Python (2nd Edition)', 6, 2021, 6, 5),
(33, '978-0135957059', 'The Pragmatic Programmer (20th Anniversary Edition)', 1, 2019, 7, 6),
(34, '978-0134092669', 'Computer Systems: A Programmer''s Perspective (3rd Ed)', 1, 2015, 6, 6),
(35, '978-1593279288', 'Python Crash Course: A Hands-On, Project-Based Introduction', 1, 2019, 8, 7),
(36, '978-0066620732', 'Just for Fun: The Story of an Accidental Revolutionary', 1, 2001, 5, 5),
(37, '978-0321486813', 'Compilers: Principles, Techniques, and Tools (Dragon Book)', 1, 2006, 6, 6),
(38, '978-0134444284', 'Cryptography and Network Security: Principles and Practice', 10, 2016, 6, 5),
(39, '978-1617294273', 'Cloud Native Patterns: Designing M-Scale Services', 10, 2019, 5, 5),
(40, '978-1593272906', 'Practical Malware Analysis: The Hands-On Guide', 10, 2012, 5, 5),
(41, '978-1491929124', 'Site Reliability Engineering: How Google Runs Production', 10, 2016, 6, 5),
(42, '978-0132847377', 'Data Structures and Algorithm Analysis in C++', 1, 2013, 6, 6),
(43, '978-0071390118', 'Principles of Neural Science (6th Edition)', 6, 2021, 4, 4),
(44, '978-0201558029', 'Concrete Mathematics: A Foundation for Computer Science', 2, 1994, 5, 5),
(45, '978-0521876544', 'Probability and Computing: Randomization in Algorithms', 2, 2017, 5, 5),
(46, '978-8121901628', 'Fluid Mechanics and Hydraulic Machines', 9, 2019, 6, 6),
(47, '978-8121901765', 'Strength of Materials and Structural Mechanics', 9, 2020, 6, 6),
(48, '978-0123821881', 'Embedded Systems: Architecture, Programming and Design', 4, 2018, 5, 5),
(49, '978-3030239220', 'Quantum Computing: An Applied Approach', 7, 2021, 5, 5),
(50, '978-1476708690', 'The Innovators: How a Group of Hackers, Geniuses Created Digital Revolution', 5, 2014, 6, 6);

-- Book Authors Mapping
INSERT INTO book_authors (book_id, author_id) VALUES
(1, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 17), (6, 18), (7, 4), (8, 7),
(9, 7), (9, 8), (10, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14),
(15, 15), (16, 1), (16, 2), (17, 3), (18, 4), (19, 11), (20, 5), (21, 16),
(22, 16), (23, 30), (24, 8), (25, 23), (26, 24), (27, 25), (28, 26), (29, 27),
(30, 28), (31, 29), (32, 21), (32, 10), (33, 11), (33, 3), (34, 17), (35, 20),
(36, 19), (37, 6), (38, 16), (39, 11), (40, 19), (41, 8), (42, 12), (43, 22),
(44, 6), (45, 4), (46, 16), (47, 16), (48, 12), (49, 13), (50, 27);

-- Members
INSERT INTO members (member_id, first_name, last_name, email, phone, membership_date, membership_type, status, max_books_allowed) VALUES
(1, 'Atharva', 'Sharma', 'atharva.sharma@college.edu', '9876543210', '2026-01-10', 'Student', 'Active', 4),
(2, 'Priya', 'Patel', 'priya.patel@college.edu', '9876543211', '2026-01-15', 'Student', 'Active', 3),
(3, 'Dr. Rajesh', 'Verma', 'rajesh.verma@college.edu', '9876543212', '2025-08-01', 'Faculty', 'Active', 8),
(4, 'Sneha', 'Kulkarni', 'sneha.k@college.edu', '9876543213', '2026-02-01', 'Student', 'Active', 3),
(5, 'Rohan', 'Mehta', 'rohan.m@college.edu', '9876543214', '2025-11-20', 'Student', 'Suspended', 2),
(6, 'Aman', 'Gupta', 'aman.gupta@college.edu', '9876543215', '2026-01-20', 'Student', 'Active', 4),
(7, 'Ananya', 'Deshmukh', 'ananya.d@college.edu', '9876543216', '2026-02-10', 'Student', 'Active', 3),
(8, 'Prof. Vikram', 'Sarabhai', 'vikram.s@college.edu', '9876543217', '2025-07-15', 'Faculty', 'Active', 8),
(9, 'Tanvi', 'Joshi', 'tanvi.j@college.edu', '9876543218', '2026-01-18', 'Student', 'Active', 3),
(10, 'Rahul', 'Nair', 'rahul.n@college.edu', '9876543219', '2025-10-05', 'Student', 'Active', 3),
(11, 'Divya', 'Iyer', 'divya.i@college.edu', '9876543220', '2026-02-14', 'Student', 'Active', 4),
(12, 'Dr. Meera', 'Sengupta', 'meera.s@college.edu', '9876543221', '2025-06-01', 'Faculty', 'Active', 8),
(13, 'Karthik', 'Reddy', 'karthik.r@college.edu', '9876543222', '2026-01-05', 'General', 'Active', 2),
(14, 'Siddharth', 'Bansal', 'siddharth.b@college.edu', '9876543223', '2025-12-11', 'Student', 'Suspended', 2),
(15, 'Pooja', 'Hegde', 'pooja.h@college.edu', '9876543224', '2026-02-20', 'Student', 'Active', 3),
(16, 'Aditya', 'Chopra', 'aditya.c@college.edu', '9876543225', '2026-01-08', 'Student', 'Active', 4),
(17, 'Neha', 'Singhal', 'neha.s@college.edu', '9876543226', '2026-01-22', 'Student', 'Active', 3),
(18, 'Prof. Anand', 'Kumar', 'anand.k@college.edu', '9876543227', '2025-05-12', 'Faculty', 'Active', 8),
(19, 'Varun', 'Dhawan', 'varun.d@college.edu', '9876543228', '2026-02-03', 'Student', 'Active', 3),
(20, 'Kavita', 'Rao', 'kavita.r@college.edu', '9876543229', '2025-11-14', 'Student', 'Active', 4),
(21, 'Dr. S. K.', 'Bhattacharya', 'sk.bhatta@college.edu', '9876543230', '2025-04-10', 'Faculty', 'Active', 8),
(22, 'Gaurav', 'Kapoor', 'gaurav.k@college.edu', '9876543231', '2026-01-12', 'Student', 'Active', 3),
(23, 'Bhavna', 'Menon', 'bhavna.m@college.edu', '9876543232', '2026-02-18', 'Student', 'Active', 3),
(24, 'Rakesh', 'Jhunjhunwala', 'rakesh.j@college.edu', '9876543233', '2025-09-09', 'General', 'Active', 2),
(25, 'Ishaan', 'Awasthi', 'ishaan.a@college.edu', '9876543234', '2026-01-30', 'Student', 'Active', 3),
(26, 'Simran', 'Kaur', 'simran.k@college.edu', '9876543235', '2026-02-05', 'Student', 'Active', 4),
(27, 'Prof. C. N. R.', 'Rao', 'cnr.rao@college.edu', '9876543236', '2025-03-01', 'Faculty', 'Active', 8),
(28, 'Nikhil', 'Kamath', 'nikhil.k@college.edu', '9876543237', '2026-01-14', 'Student', 'Active', 3),
(29, 'Shruti', 'Haasan', 'shruti.h@college.edu', '9876543238', '2025-10-25', 'Student', 'Active', 3),
(30, 'Arjun', 'Rampal', 'arjun.r@college.edu', '9876543239', '2025-12-05', 'Student', 'Suspended', 2);

-- Borrow Transactions
INSERT INTO borrow_transactions (transaction_id, book_id, member_id, issue_date, due_date, return_date, status) VALUES
(1, 1, 1, DATE_SUB(CURDATE(), INTERVAL 5 DAY), DATE_ADD(CURDATE(), INTERVAL 9 DAY), NULL, 'Issued'),
(2, 9, 6, DATE_SUB(CURDATE(), INTERVAL 3 DAY), DATE_ADD(CURDATE(), INTERVAL 11 DAY), NULL, 'Issued'),
(3, 10, 3, DATE_SUB(CURDATE(), INTERVAL 7 DAY), DATE_ADD(CURDATE(), INTERVAL 21 DAY), NULL, 'Issued'),
(4, 14, 7, DATE_SUB(CURDATE(), INTERVAL 2 DAY), DATE_ADD(CURDATE(), INTERVAL 12 DAY), NULL, 'Issued'),
(5, 16, 11, DATE_SUB(CURDATE(), INTERVAL 4 DAY), DATE_ADD(CURDATE(), INTERVAL 10 DAY), NULL, 'Issued'),
(6, 21, 16, DATE_SUB(CURDATE(), INTERVAL 6 DAY), DATE_ADD(CURDATE(), INTERVAL 8 DAY), NULL, 'Issued'),
(7, 22, 17, DATE_SUB(CURDATE(), INTERVAL 1 DAY), DATE_ADD(CURDATE(), INTERVAL 13 DAY), NULL, 'Issued'),
(8, 25, 18, DATE_SUB(CURDATE(), INTERVAL 8 DAY), DATE_ADD(CURDATE(), INTERVAL 20 DAY), NULL, 'Issued'),
(9, 32, 20, DATE_SUB(CURDATE(), INTERVAL 3 DAY), DATE_ADD(CURDATE(), INTERVAL 11 DAY), NULL, 'Issued'),
(10, 33, 22, DATE_SUB(CURDATE(), INTERVAL 5 DAY), DATE_ADD(CURDATE(), INTERVAL 9 DAY), NULL, 'Issued'),
(11, 35, 23, DATE_SUB(CURDATE(), INTERVAL 2 DAY), DATE_ADD(CURDATE(), INTERVAL 12 DAY), NULL, 'Issued'),
(12, 41, 26, DATE_SUB(CURDATE(), INTERVAL 4 DAY), DATE_ADD(CURDATE(), INTERVAL 10 DAY), NULL, 'Issued'),
(13, 2, 2, DATE_SUB(CURDATE(), INTERVAL 18 DAY), DATE_SUB(CURDATE(), INTERVAL 4 DAY), NULL, 'Overdue'),
(14, 3, 9, DATE_SUB(CURDATE(), INTERVAL 22 DAY), DATE_SUB(CURDATE(), INTERVAL 8 DAY), NULL, 'Overdue'),
(15, 12, 10, DATE_SUB(CURDATE(), INTERVAL 20 DAY), DATE_SUB(CURDATE(), INTERVAL 6 DAY), NULL, 'Overdue'),
(16, 15, 13, DATE_SUB(CURDATE(), INTERVAL 16 DAY), DATE_SUB(CURDATE(), INTERVAL 2 DAY), NULL, 'Overdue'),
(17, 26, 19, DATE_SUB(CURDATE(), INTERVAL 25 DAY), DATE_SUB(CURDATE(), INTERVAL 11 DAY), NULL, 'Overdue'),
(18, 38, 28, DATE_SUB(CURDATE(), INTERVAL 19 DAY), DATE_SUB(CURDATE(), INTERVAL 5 DAY), NULL, 'Overdue'),
(19, 4, 3, DATE_SUB(CURDATE(), INTERVAL 40 DAY), DATE_SUB(CURDATE(), INTERVAL 26 DAY), DATE_SUB(CURDATE(), INTERVAL 28 DAY), 'Returned'),
(20, 5, 8, DATE_SUB(CURDATE(), INTERVAL 45 DAY), DATE_SUB(CURDATE(), INTERVAL 15 DAY), DATE_SUB(CURDATE(), INTERVAL 18 DAY), 'Returned'),
(21, 6, 1, DATE_SUB(CURDATE(), INTERVAL 30 DAY), DATE_SUB(CURDATE(), INTERVAL 16 DAY), DATE_SUB(CURDATE(), INTERVAL 17 DAY), 'Returned'),
(22, 7, 4, DATE_SUB(CURDATE(), INTERVAL 35 DAY), DATE_SUB(CURDATE(), INTERVAL 21 DAY), DATE_SUB(CURDATE(), INTERVAL 22 DAY), 'Returned'),
(23, 18, 12, DATE_SUB(CURDATE(), INTERVAL 50 DAY), DATE_SUB(CURDATE(), INTERVAL 20 DAY), DATE_SUB(CURDATE(), INTERVAL 25 DAY), 'Returned'),
(24, 23, 16, DATE_SUB(CURDATE(), INTERVAL 32 DAY), DATE_SUB(CURDATE(), INTERVAL 18 DAY), DATE_SUB(CURDATE(), INTERVAL 20 DAY), 'Returned'),
(25, 27, 21, DATE_SUB(CURDATE(), INTERVAL 42 DAY), DATE_SUB(CURDATE(), INTERVAL 12 DAY), DATE_SUB(CURDATE(), INTERVAL 15 DAY), 'Returned'),
(26, 29, 24, DATE_SUB(CURDATE(), INTERVAL 38 DAY), DATE_SUB(CURDATE(), INTERVAL 24 DAY), DATE_SUB(CURDATE(), INTERVAL 25 DAY), 'Returned'),
(27, 34, 25, DATE_SUB(CURDATE(), INTERVAL 29 DAY), DATE_SUB(CURDATE(), INTERVAL 15 DAY), DATE_SUB(CURDATE(), INTERVAL 17 DAY), 'Returned'),
(28, 44, 27, DATE_SUB(CURDATE(), INTERVAL 60 DAY), DATE_SUB(CURDATE(), INTERVAL 30 DAY), DATE_SUB(CURDATE(), INTERVAL 35 DAY), 'Returned'),
(29, 8, 4, DATE_SUB(CURDATE(), INTERVAL 35 DAY), DATE_SUB(CURDATE(), INTERVAL 21 DAY), DATE_SUB(CURDATE(), INTERVAL 16 DAY), 'Returned'),
(30, 11, 6, DATE_SUB(CURDATE(), INTERVAL 40 DAY), DATE_SUB(CURDATE(), INTERVAL 26 DAY), DATE_SUB(CURDATE(), INTERVAL 20 DAY), 'Returned'),
(31, 19, 8, DATE_SUB(CURDATE(), INTERVAL 55 DAY), DATE_SUB(CURDATE(), INTERVAL 25 DAY), DATE_SUB(CURDATE(), INTERVAL 17 DAY), 'Returned'),
(32, 28, 18, DATE_SUB(CURDATE(), INTERVAL 48 DAY), DATE_SUB(CURDATE(), INTERVAL 18 DAY), DATE_SUB(CURDATE(), INTERVAL 14 DAY), 'Returned'),
(33, 13, 11, DATE_SUB(CURDATE(), INTERVAL 32 DAY), DATE_SUB(CURDATE(), INTERVAL 18 DAY), DATE_SUB(CURDATE(), INTERVAL 12 DAY), 'Returned'),
(34, 17, 15, DATE_SUB(CURDATE(), INTERVAL 30 DAY), DATE_SUB(CURDATE(), INTERVAL 16 DAY), DATE_SUB(CURDATE(), INTERVAL 8 DAY), 'Returned'),
(35, 24, 22, DATE_SUB(CURDATE(), INTERVAL 28 DAY), DATE_SUB(CURDATE(), INTERVAL 14 DAY), DATE_SUB(CURDATE(), INTERVAL 4 DAY), 'Returned'),
(36, 39, 29, DATE_SUB(CURDATE(), INTERVAL 26 DAY), DATE_SUB(CURDATE(), INTERVAL 12 DAY), DATE_SUB(CURDATE(), INTERVAL 7 DAY), 'Returned');

-- Fines
INSERT INTO fines (fine_id, transaction_id, member_id, fine_amount, paid_status, paid_date) VALUES
(1, 29, 4, 25.00, 'Paid', DATE_SUB(CURDATE(), INTERVAL 15 DAY)),
(2, 30, 6, 30.00, 'Paid', DATE_SUB(CURDATE(), INTERVAL 19 DAY)),
(3, 31, 8, 40.00, 'Paid', DATE_SUB(CURDATE(), INTERVAL 16 DAY)),
(4, 32, 18, 20.00, 'Paid', DATE_SUB(CURDATE(), INTERVAL 13 DAY)),
(5, 33, 11, 30.00, 'Unpaid', NULL),
(6, 34, 15, 40.00, 'Unpaid', NULL),
(7, 35, 22, 50.00, 'Unpaid', NULL),
(8, 36, 29, 25.00, 'Unpaid', NULL),
(9, 21, 1, 15.00, 'Paid', DATE_SUB(CURDATE(), INTERVAL 16 DAY)),
(10, 27, 25, 35.00, 'Unpaid', NULL);

-- Audit Logs
INSERT INTO audit_logs (table_name, action_type, description) VALUES
('system', 'INITIALIZE', 'Initial library database setup and schema creation completed.'),
('categories', 'INSERT', 'Created 10 academic and engineering categories.'),
('authors', 'INSERT', 'Populated catalog with 30 recognized academic and technical authors.'),
('books', 'INSERT', 'Batch catalog import: 50 reference and course books added.'),
('members', 'INSERT', 'Registered initial batch of 30 students, research scholars, and faculty.'),
('borrow_transactions', 'ISSUE', 'Book ID 1 (Database System Concepts) issued to Member ID 1 (Atharva Sharma).'),
('borrow_transactions', 'ISSUE', 'Book ID 9 (Artificial Intelligence: A Modern Approach) issued to Member ID 6 (Aman Gupta).'),
('borrow_transactions', 'ISSUE', 'Book ID 10 (Deep Learning) issued to Dr. Rajesh Verma (Faculty).'),
('borrow_transactions', 'ISSUE', 'Book ID 14 (Atomic Habits) issued to Ananya Deshmukh.'),
('borrow_transactions', 'ISSUE', 'Book ID 21 (Modern Operating Systems) issued to Aditya Chopra.'),
('borrow_transactions', 'ISSUE', 'Book ID 22 (Computer Networks) issued to Neha Singhal.'),
('borrow_transactions', 'RETURN', 'Book ID 4 returned on time by Dr. Rajesh Verma.'),
('borrow_transactions', 'RETURN', 'Book ID 5 returned on time by Prof. Vikram Sarabhai.'),
('borrow_transactions', 'RETURN', 'Book ID 8 returned late by 5 days by Sneha Kulkarni. Imposed fine: Rs. 25.00.'),
('fines', 'PAYMENT', 'Fine ID 1 of Rs. 25.00 paid and cleared by Sneha Kulkarni.'),
('borrow_transactions', 'RETURN', 'Book ID 11 returned late by 6 days by Aman Gupta. Imposed fine: Rs. 30.00.'),
('fines', 'PAYMENT', 'Fine ID 2 of Rs. 30.00 paid and cleared by Aman Gupta.'),
('borrow_transactions', 'RETURN', 'Book ID 13 returned late by 6 days by Divya Iyer. Fine generated: Rs. 30.00.'),
('borrow_transactions', 'RETURN', 'Book ID 17 returned late by 8 days by Pooja Hegde. Fine generated: Rs. 40.00.'),
('borrow_transactions', 'RETURN', 'Book ID 24 returned late by 10 days by Gaurav Kapoor. Fine generated: Rs. 50.00.');
