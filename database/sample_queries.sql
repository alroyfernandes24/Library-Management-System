-- ==============================================================
-- ADVANCED SQL QUERIES FOR DBMS MINI PROJECT (LAB & VIVA PRACTICE)
-- Project: Library Management System
-- ==============================================================

-- --------------------------------------------------------------
-- 1. BASIC RETRIEVAL & FILTERING
-- --------------------------------------------------------------

-- Query 1.1: List all books published after the year 2000 ordered by year descending
SELECT book_id, title, publication_year, available_copies
FROM books
WHERE publication_year > 2000
ORDER BY publication_year DESC;

-- Query 1.2: Find all active members who are students
SELECT member_id, first_name, last_name, email, membership_type
FROM members
WHERE status = 'Active' AND membership_type = 'Student';


-- --------------------------------------------------------------
-- 2. JOINS (INNER, LEFT, MULTI-TABLE JOINS)
-- --------------------------------------------------------------

-- Query 2.1: Retrieve book titles along with their category name and author(s)
-- (Demonstrates 3-way JOIN across M:N relationship)
SELECT 
    b.title AS Book_Title,
    c.category_name AS Category,
    a.author_name AS Author
FROM books b
JOIN categories c ON b.category_id = c.category_id
JOIN book_authors ba ON b.book_id = ba.book_id
JOIN authors a ON ba.author_id = a.author_id
ORDER BY b.title;

-- Query 2.2: Find all books that have NEVER been borrowed
-- (Demonstrates LEFT JOIN with NULL check)
SELECT 
    b.book_id,
    b.title,
    b.isbn
FROM books b
LEFT JOIN borrow_transactions t ON b.book_id = t.book_id
WHERE t.transaction_id IS NULL;

-- Query 2.3: List currently issued books with borrower names and contact info
SELECT 
    t.transaction_id,
    b.title,
    CONCAT(m.first_name, ' ', m.last_name) AS borrower_name,
    m.phone,
    t.issue_date,
    t.due_date
FROM borrow_transactions t
JOIN books b ON t.book_id = b.book_id
JOIN members m ON t.member_id = m.member_id
WHERE t.return_date IS NULL;


-- --------------------------------------------------------------
-- 3. AGGREGATE FUNCTIONS & GROUP BY / HAVING
-- --------------------------------------------------------------

-- Query 3.1: Count total number of books and average publication year per category
SELECT 
    c.category_name,
    COUNT(b.book_id) AS total_books_count,
    SUM(b.total_copies) AS total_copies,
    ROUND(AVG(b.publication_year), 0) AS avg_publication_year
FROM categories c
LEFT JOIN books b ON c.category_id = b.category_id
GROUP BY c.category_id, c.category_name
ORDER BY total_copies DESC;

-- Query 3.2: Find authors who have written more than 1 book in the catalog
-- (Demonstrates GROUP BY with HAVING clause)
SELECT 
    a.author_id,
    a.author_name,
    COUNT(ba.book_id) AS books_authored
FROM authors a
JOIN book_authors ba ON a.author_id = ba.author_id
GROUP BY a.author_id, a.author_name
HAVING COUNT(ba.book_id) > 1;

-- Query 3.3: Calculate total revenue collected from paid fines and total pending fines
SELECT 
    paid_status,
    COUNT(*) AS count_of_fines,
    SUM(fine_amount) AS total_amount
FROM fines
GROUP BY paid_status;


-- --------------------------------------------------------------
-- 4. NESTED SUBQUERIES & CORRELATED SUBQUERIES
-- --------------------------------------------------------------

-- Query 4.1: Find the member(s) who have borrowed the highest number of books
-- (Subquery with MAX)
SELECT 
    m.member_id,
    m.first_name,
    m.last_name,
    COUNT(t.transaction_id) AS total_borrows
FROM members m
JOIN borrow_transactions t ON m.member_id = t.member_id
GROUP BY m.member_id, m.first_name, m.last_name
HAVING total_borrows = (
    SELECT MAX(borrow_count)
    FROM (
        SELECT COUNT(transaction_id) AS borrow_count
        FROM borrow_transactions
        GROUP BY member_id
    ) AS temp_counts
);

-- Query 4.2: Find members who currently have overdue books using EXISTS
SELECT 
    m.member_id,
    m.first_name,
    m.last_name,
    m.email
FROM members m
WHERE EXISTS (
    SELECT 1 
    FROM borrow_transactions t 
    WHERE t.member_id = m.member_id 
      AND t.return_date IS NULL 
      AND CURRENT_DATE > t.due_date
);

-- Query 4.3: Find books whose total copies are strictly greater than the average total copies across all books
SELECT 
    book_id,
    title,
    total_copies
FROM books
WHERE total_copies > (SELECT AVG(total_copies) FROM books);


-- --------------------------------------------------------------
-- 5. SET OPERATIONS (UNION, INTERSECT, EXCEPT / MINUS)
-- --------------------------------------------------------------

-- Query 5.1: Combine names of authors and members who have contact emails ending with specific domain
SELECT author_name AS full_name, email, 'Author' AS role FROM authors WHERE email IS NOT NULL
UNION
SELECT CONCAT(first_name, ' ', last_name) AS full_name, email, 'Member' AS role FROM members;


-- --------------------------------------------------------------
-- 6. ANALYTICAL & WINDOW FUNCTIONS (For modern DBMS / MySQL 8.0+)
-- --------------------------------------------------------------

-- Query 6.1: Rank books within each category according to total copies available
SELECT 
    b.title,
    c.category_name,
    b.total_copies,
    DENSE_RANK() OVER (PARTITION BY b.category_id ORDER BY b.total_copies DESC) AS rank_in_category
FROM books b
JOIN categories c ON b.category_id = c.category_id;

-- Query 6.2: Running total of fines issued over time
SELECT 
    fine_id,
    member_id,
    fine_amount,
    SUM(fine_amount) OVER (ORDER BY fine_id) AS running_total_fines
FROM fines;
