# MICRO PROJECT SYNOPSIS
## ON
# AUTOMATED LIBRARY MANAGEMENT SYSTEM
### Submitted for the Subject
### DATABASE MANAGEMENT SYSTEMS (DBMS)

**Submitted By:**
1. Aditya Chitimilla – 11385
2. Atharva Doke – 11388
3. Alroy Fernandes – 11393

**Class:** S.E. CSE - C  
**Academic Year:** 2026–27  

**Under the Guidance of:**  
Prof. Afreen Sayed  

**Society of St. Francis Xavier, Pilar’s**  
**Fr. Conceicao Rodrigues College of Engineering**  
Fr. Agnel Ashram, Bandstand, Bandra (W), Mumbai – 400 050  
*(Autonomous College affiliated to University of Mumbai)*  
Department of Computer Science & Engineering  

---

## Formatting Specifications (Reference Only)
| Specification | Requirement |
| :--- | :--- |
| Paper Size | A4 |
| Font Family | Times New Roman |
| Body Text | 12 pt, Regular |
| Main Headings | 14 pt, Bold |
| Subheadings | 12 pt, Bold |
| Project Title | 16 pt, Bold, Center aligned |
| Cover Page Main Heading | 18 pt, Bold, Center aligned |
| Line Spacing | 1.5 |
| Paragraph Alignment | Justified |
| Margins | Top: 0.75", Bottom: 0.75", Left: 1", Right: 1" |
| Page Number | Bottom-center |
| Heading Numbering | 1, 2, 3…; subheadings 7.1, 7.2… |
| Tables | Times New Roman, 11–12 pt; captions above tables |
| Figures/Diagrams | Centered; caption below figure |
| Printing | A4, single-sided print |

---

## Table of Contents
1. Project Title
2. Introduction
3. Problem Statement
4. Objectives
5. Scope of the Project
6. Proposed System
7. Database Design
   - 7.1 Entities and Attributes
   - 7.2 ER/EER Diagram
   - 7.3 Relational Schema
   - 7.4 Primary Keys and Foreign Keys
8. SQL Implementation
9. Sample SQL Queries
10. Expected Outcome
11. Conclusion
12. References

---

## 1. Project Title
**Automated Library Management System with Relational Integrity and Trigger-Based Fine Calculation**

---

## 2. Introduction
A modern educational or institutional library manages thousands of book volumes, diversified academic classifications, multiple contributing authors, and hundreds of registered students and faculty members. Traditional manual registers and flat spreadsheet-based methods fail to guarantee relational consistency, struggle with concurrent borrow requests, suffer from redundant records, and lack automated mechanisms to calculate overdue return fines.

The Automated Library Management System is a database-centric desktop and web application engineered on relational database principles (3NF normalization, ACID transaction management, foreign key integrity, automated triggers, and aggregate analytics). The database architecture connects inventory management, multi-author book attribution, member borrowing quotas, real-time stock decrementation, and automated monetary penalty computation into a unified, secure database platform.

---

## 3. Problem Statement
Conventional paper ledgers and unstructured digital spreadsheets suffer from several database management challenges:
1. **Redundancy and Update Anomalies:** Book and author details are duplicated across transactions. Modifying an author's name or a category description across multiple rows leads to data inconsistency.
2. **Deletion Anomalies:** Deleting a member's loan history often leads to accidental deletion of the member's profile or book catalog record if relational separation is absent.
3. **Inventory Drift and Race Conditions:** Lack of database constraints allows physical book copies to be loaned beyond actual shelf count, resulting in negative available stock.
4. **Manual and Inaccurate Fine Imposition:** Determining overdue durations and computing fines (e.g., ₹5.00 per delayed day) manually is error-prone, labor-intensive, and causes institutional revenue loss.
5. **Absence of Audit Trail:** No historical record exists of who added books, registered new authors, issued volumes, or cleared penalties.

---

## 4. Objectives
The core objectives of the proposed database system include:
1. **Develop a 3NF Normalized Relational Database:** Eliminate update, insertion, and deletion anomalies across 8 distinct relational tables (`categories`, `authors`, `books`, `book_authors`, `members`, `borrow_transactions`, `fines`, `audit_logs`).
2. **Enforce Referential Integrity and Domain Constraints:** Implement Primary Keys, Foreign Keys with cascading actions, `CHECK` constraints on copy counts and fine amounts, and `UNIQUE` constraints on ISBNs and member emails.
3. **Automate Inventory and Overdue Penalty Rules via Triggers:** Deploy active database triggers that automatically decrement available book stock upon issuance, increment copies upon return, and compute overdue fines at ₹5/day upon return.
4. **Support Multi-Author Attribution:** Resolve the Many-to-Many ($M:N$) relationship between books and authors via a composite-key junction table (`book_authors`) and provide dynamic author creation in the user interface.
5. **Build User-Friendly Management Interfaces:** Deliver dual accessible interfaces (Python Tkinter Desktop GUI and HTML5/Bootstrap 5 Web REST Client) for catalog browsing, member quota tracking, and instant SQL query execution.

---

## 5. Scope of the Project
The functional scope covers the end-to-end operational lifecycle of an institutional library:
- **Catalog & Inventory Management:** Full CRUD operations for books, genre categories, and author profiles; dynamic on-the-fly author creation during book entry; ISBN uniqueness verification; and stock tracking.
- **Membership Management:** Member registration across three tiers (Student with 3 books limit, Faculty with 8 books limit, and General with 3 books limit), email uniqueness, and real-time active loan counters.
- **Circulation & Transactions:** Safe issuance with pre-condition checks (member status, quota limit, shelf availability) and return logging with automated trigger-driven stock restoration.
- **Fines & Revenue Tracking:** Automatic penalty generation for overdue returns, fine status tracking (`Unpaid` vs `Paid`), and receipt clearance.
- **Audit Logging & Analytics:** Automatic timestamped audit logging for every catalog insert, deletion, author creation, loan issue, return, and payment.

**Boundaries / Outside Current Scope:**
- Real-time RFID hardware scanner integration.
- External payment gateway processing (fines are recorded and marked paid by the library administrator).
- Inter-library courier logistics.

---

## 6. Proposed System
The proposed system employs a **3-Tier Architecture**:
1. **Presentation Layer:**
   - A lightweight Desktop GUI developed using Python Tkinter, offering high-speed tabbed navigation across Dashboard, Book Catalog, Member Directory, Issue/Return Desk, Fines Tracker, and Audit Logs.
   - A modern Web Application using HTML5, Bootstrap 5, and JavaScript fetching data asynchronously via RESTful endpoints. It includes a dynamic "Add New Book" modal with an embedded "➕ Add New Author" sub-routine.
2. **Application & Controller Layer:**
   - A Python-powered application controller (`db_manager.py` & `app_web.py`) providing parameter validation, business logic enforcement (checking member quotas and book availability before issuing), and transactional wrappers.
3. **Relational Database Management System (DBMS):**
   - SQLite 3 (with foreign key enforcement enabled via `PRAGMA foreign_keys = ON`) and compatible with enterprise MySQL 8.0+.
   - Database-level automation featuring active event triggers (`trg_after_issue_book`, `trg_after_return_book`, `trg_calculate_fine_on_return`) and pre-compiled analytical views (`vw_book_catalog`, `vw_active_loans`, `vw_library_summary`).

---

## 7. Database Design

### 7.1 Entities and Attributes
The system models eight essential database entities:
1. **CATEGORIES:** Classifies books by discipline.
   - `category_id` (INT, PK, Auto-increment)
   - `category_name` (VARCHAR(50), NOT NULL, UNIQUE)
   - `description` (TEXT)
2. **AUTHORS:** Stores writer profiles.
   - `author_id` (INT, PK, Auto-increment)
   - `author_name` (VARCHAR(100), NOT NULL)
   - `email` (VARCHAR(100))
   - `biography` (TEXT)
3. **BOOKS:** Represents physical book titles in the library collection.
   - `book_id` (INT, PK, Auto-increment)
   - `isbn` (VARCHAR(20), NOT NULL, UNIQUE)
   - `title` (VARCHAR(200), NOT NULL)
   - `category_id` (INT, FK referencing `categories`)
   - `publication_year` (INT)
   - `total_copies` (INT, NOT NULL, CHECK $\ge 0$)
   - `available_copies` (INT, NOT NULL, CHECK $\ge 0$ and $\le$ `total_copies`)
4. **BOOK_AUTHORS:** Junction entity resolving the $M:N$ relationship between Books and Authors.
   - `book_id` (INT, PK, FK referencing `books`, ON DELETE CASCADE)
   - `author_id` (INT, PK, FK referencing `authors`, ON DELETE CASCADE)
5. **MEMBERS:** Maintains registered patrons and their borrowing privileges.
   - `member_id` (INT, PK, Auto-increment)
   - `first_name` (VARCHAR(50), NOT NULL)
   - `last_name` (VARCHAR(50), NOT NULL)
   - `email` (VARCHAR(100), NOT NULL, UNIQUE)
   - `phone` (VARCHAR(15))
   - `membership_date` (DATE, DEFAULT CURRENT_DATE)
   - `membership_type` (VARCHAR(20), CHECK IN ('Student', 'Faculty', 'General'))
   - `status` (VARCHAR(20), CHECK IN ('Active', 'Suspended', 'Expired'))
   - `max_books_allowed` (INT, CHECK $> 0$)
6. **BORROW_TRANSACTIONS:** Tracks book loan lifecycles.
   - `transaction_id` (INT, PK, Auto-increment)
   - `book_id` (INT, FK referencing `books`, ON DELETE CASCADE)
   - `member_id` (INT, FK referencing `members`, ON DELETE CASCADE)
   - `issue_date` (DATE, NOT NULL, DEFAULT CURRENT_DATE)
   - `due_date` (DATE, NOT NULL)
   - `return_date` (DATE, NULLABLE until returned)
   - `status` (VARCHAR(20), DEFAULT 'Issued')
7. **FINES:** Stores monetary penalties assessed on overdue loans.
   - `fine_id` (INT, PK, Auto-increment)
   - `transaction_id` (INT, NOT NULL, UNIQUE, FK referencing `borrow_transactions`, ON DELETE CASCADE)
   - `member_id` (INT, NOT NULL, FK referencing `members`, ON DELETE CASCADE)
   - `fine_amount` (DECIMAL(10,2), NOT NULL, CHECK $\ge 0$)
   - `paid_status` (VARCHAR(20), DEFAULT 'Unpaid', CHECK IN ('Unpaid', 'Paid'))
   - `paid_date` (DATE, NULLABLE)
8. **AUDIT_LOGS:** Provides tamper-evident system audit logging.
   - `log_id` (INT, PK, Auto-increment)
   - `table_name` (VARCHAR(50), NOT NULL)
   - `action_type` (VARCHAR(20), NOT NULL)
   - `description` (TEXT, NOT NULL)
   - `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

### 7.2 ER/EER Diagram
The Entity-Relationship diagram depicts all entities, primary/foreign keys, and cardinalities:
- `CATEGORIES` 1 ——— N `BOOKS` (One category classifies many books)
- `AUTHORS` 1 ——— N `BOOK_AUTHORS` N ——— 1 `BOOKS` (Many authors write many books)
- `MEMBERS` 1 ——— N `BORROW_TRANSACTIONS` (One member borrows multiple books)
- `BOOKS` 1 ——— N `BORROW_TRANSACTIONS` (One book title is loaned across multiple transactions)
- `BORROW_TRANSACTIONS` 1 ——— 0..1 `FINES` (An overdue transaction incurs at most one fine record)

*(See Figure 1 in Section 10 for the generated high-resolution diagram).*

### 7.3 Relational Schema
The database satisfies Third Normal Form (3NF) requirements:
- $\text{categories}(\underline{\text{category\_id}}, \text{category\_name}, \text{description})$
- $\text{authors}(\underline{\text{author\_id}}, \text{author\_name}, \text{email}, \text{biography})$
- $\text{books}(\underline{\text{book\_id}}, \text{isbn}, \text{title}, \text{category\_id}^*, \text{publication\_year}, \text{total\_copies}, \text{available\_copies})$
- $\text{book\_authors}(\underline{\text{book\_id}}^*, \underline{\text{author\_id}}^*)$
- $\text{members}(\underline{\text{member\_id}}, \text{first\_name}, \text{last\_name}, \text{email}, \text{phone}, \text{membership\_date}, \text{membership\_type}, \text{status}, \text{max\_books\_allowed})$
- $\text{borrow\_transactions}(\underline{\text{transaction\_id}}, \text{book\_id}^*, \text{member\_id}^*, \text{issue\_date}, \text{due\_date}, \text{return\_date}, \text{status})$
- $\text{fines}(\underline{\text{fine\_id}}, \text{transaction\_id}^*, \text{member\_id}^*, \text{fine_amount}, \text{paid\_status}, \text{paid\_date})$
- $\text{audit\_logs}(\underline{\text{log\_id}}, \text{table\_name}, \text{action\_type}, \text{description}, \text{created\_at})$

*(Underlined attributes denote Primary Keys; asterisks denote Foreign Keys).*

### 7.4 Primary Keys and Foreign Keys
| Table Name | Primary Key | Foreign Key(s) | Referential Action / Constraints |
| :--- | :--- | :--- | :--- |
| `categories` | `category_id` | None | `category_name UNIQUE` |
| `authors` | `author_id` | None | `author_name NOT NULL` |
| `books` | `book_id` | `category_id` $\rightarrow$ `categories` | `isbn UNIQUE`, `available_copies <= total_copies` |
| `book_authors` | `(book_id, author_id)` | `book_id` $\rightarrow$ `books`, `author_id` $\rightarrow$ `authors` | `ON DELETE CASCADE` |
| `members` | `member_id` | None | `email UNIQUE`, `CHECK(max_books_allowed > 0)` |
| `borrow_transactions` | `transaction_id` | `book_id` $\rightarrow$ `books`, `member_id` $\rightarrow$ `members` | `ON DELETE CASCADE` |
| `fines` | `fine_id` | `transaction_id` $\rightarrow$ `borrow_transactions`, `member_id` $\rightarrow$ `members` | `transaction_id UNIQUE`, `fine_amount >= 0` |
| `audit_logs` | `log_id` | None | System timestamp tracking |

---

## 8. SQL Implementation
The system demonstrates complete mastery over standard and advanced SQL paradigms:
1. **Data Definition Language (DDL):** `CREATE TABLE`, `DROP TABLE`, `ALTER TABLE`, and domain integrity constraints (`PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `NOT NULL`, `CHECK`, `DEFAULT`).
2. **Data Manipulation Language (DML):** `INSERT INTO`, `UPDATE`, `DELETE`, and parameter-safe prepared statements.
3. **Data Query Language (DQL):** Multi-table joins (`INNER JOIN`, `LEFT JOIN`), filtering (`WHERE`, `LIKE`, `IN`, `BETWEEN`), ordering (`ORDER BY`), and string aggregations (`GROUP_CONCAT` / `GROUP BY`).
4. **Aggregate Functions & Analytics:** `COUNT(*)`, `SUM()`, `AVG()`, `MAX()`, `MIN()`, grouped by category or patron tier, accompanied by `HAVING` filters.
5. **Database Triggers:**
   - `trg_after_issue_book`: Automatically decrements `available_copies` on `books` when a row is inserted into `borrow_transactions`.
   - `trg_after_return_book`: Restores `available_copies` when `return_date` is stamped.
   - `trg_calculate_fine_on_return`: Computes date difference ($\text{return\_date} - \text{due\_date}$) and creates an automatic row in `fines` at ₹5.00/day if overdue.
6. **Pre-Compiled Database Views:**
   - `vw_book_catalog`: Joins books, categories, and author names.
   - `vw_active_loans`: Joins active borrow records with patron contact and overdue calculations.
   - `vw_library_summary`: Single-row statistical dashboard aggregator.

---

## 9. Sample SQL Queries

### Query 1: Comprehensive Book Catalog with Multi-Author String Aggregation
```sql
SELECT 
    b.book_id,
    b.isbn,
    b.title,
    c.category_name,
    IFNULL(GROUP_CONCAT(a.author_name, ', '), 'Unknown') AS authors,
    b.publication_year,
    b.total_copies,
    b.available_copies
FROM books b
LEFT JOIN categories c ON b.category_id = c.category_id
LEFT JOIN book_authors ba ON b.book_id = ba.book_id
LEFT JOIN authors a ON ba.author_id = a.author_id
GROUP BY b.book_id
ORDER BY b.book_id ASC
LIMIT 5;
```
**Output:**
| book_id | isbn | title | category_name | authors | publication_year | total_copies | available_copies |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 978-0131103627 | The C Programming Language | Computer Science | Brian W. Kernighan, Dennis M. Ritchie | 1988 | 5 | 5 |
| 2 | 978-0262033848 | Introduction to Algorithms | Computer Science | Thomas H. Cormen, Charles E. Leiserson | 2009 | 4 | 3 |
| 3 | 978-0073523323 | Database System Concepts | Computer Science | Abraham Silberschatz, Henry F. Korth | 2019 | 6 | 6 |
| 4 | 978-0132350884 | Clean Code: Agile Software | Software Engineering | Robert C. Martin | 2008 | 5 | 4 |
| 5 | 978-0134685991 | Effective Java (3rd Edition) | Programming Languages | Joshua Bloch | 2018 | 4 | 4 |

---

### Query 2: Active Borrow Transactions with Real-Time Overdue Calculation
```sql
SELECT 
    t.transaction_id,
    b.title AS book_title,
    (m.first_name || ' ' || m.last_name) AS member_name,
    m.email,
    t.issue_date,
    t.due_date,
    CASE 
        WHEN DATE('now') > t.due_date THEN (JULIANDAY(DATE('now')) - JULIANDAY(t.due_date))
        ELSE 0 
    END AS days_overdue
FROM borrow_transactions t
JOIN books b ON t.book_id = b.book_id
JOIN members m ON t.member_id = m.member_id
WHERE t.return_date IS NULL
ORDER BY days_overdue DESC;
```
**Output:**
| transaction_id | book_title | member_name | email | issue_date | due_date | days_overdue |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 3 | Artificial Intelligence: A Modern Approach | Daniel Craig | daniel.c@univ.edu | 2026-09-10 | 2026-09-24 | 33 |
| 1 | Introduction to Algorithms | Aarav Sharma | aarav.sharma@college.edu | 2026-10-15 | 2026-10-29 | 0 |
| 2 | Clean Code: Agile Software | Priya Patel | priya.p@college.edu | 2026-10-18 | 2026-11-01 | 0 |

---

### Query 3: Category-Wise Inventory Aggregation with HAVING Filter
```sql
SELECT 
    c.category_name,
    COUNT(b.book_id) AS total_titles,
    SUM(b.total_copies) AS total_physical_volumes,
    SUM(b.available_copies) AS available_on_shelf
FROM categories c
JOIN books b ON c.category_id = b.category_id
GROUP BY c.category_id, c.category_name
HAVING SUM(b.total_copies) >= 5
ORDER BY total_physical_volumes DESC;
```
**Output:**
| category_name | total_titles | total_physical_volumes | available_on_shelf |
| :--- | :--- | :--- | :--- |
| Computer Science | 5 | 26 | 24 |
| Software Engineering | 3 | 14 | 13 |
| Electronics | 2 | 8 | 8 |
| Mathematics | 2 | 7 | 7 |

---

### Query 4: Unpaid Fines Report with Patron Details
```sql
SELECT 
    f.fine_id,
    f.transaction_id,
    (m.first_name || ' ' || m.last_name) AS member_name,
    m.phone,
    b.title AS overdue_book,
    f.fine_amount,
    f.paid_status
FROM fines f
JOIN members m ON f.member_id = m.member_id
JOIN borrow_transactions t ON f.transaction_id = t.transaction_id
JOIN books b ON t.book_id = b.book_id
WHERE f.paid_status = 'Unpaid'
ORDER BY f.fine_amount DESC;
```
**Output:**
| fine_id | transaction_id | member_name | phone | overdue_book | fine_amount | paid_status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 101 | Sarah Jenkins | 9876543210 | Operating System Concepts | ₹35.00 | Unpaid |
| 2 | 104 | Vikram Malhotra | 9822334455 | Computer Networks | ₹20.00 | Unpaid |

---

### Query 5: High-Demand Books Borrowed More Than Once
```sql
SELECT 
    b.book_id,
    b.title,
    c.category_name,
    COUNT(t.transaction_id) AS borrow_frequency
FROM books b
JOIN categories c ON b.category_id = c.category_id
LEFT JOIN borrow_transactions t ON b.book_id = t.book_id
GROUP BY b.book_id
HAVING COUNT(t.transaction_id) >= 1
ORDER BY borrow_frequency DESC;
```
**Output:**
| book_id | title | category_name | borrow_frequency |
| :--- | :--- | :--- | :--- |
| 2 | Introduction to Algorithms | Computer Science | 4 |
| 4 | Clean Code: Agile Software | Software Engineering | 3 |
| 6 | Operating System Concepts | Computer Science | 2 |

---

## 10. Expected Outcome
The completed database system successfully provides:
1. **Persistent Centralized Relational Store:** Eliminates data duplication across books, authors, members, and transactions.
2. **Automated Enforcement of Business Rules:** Automated triggers eliminate manual errors by decrementing shelf inventory upon loan, incrementing copies upon return, and charging overdue fines accurately.
3. **Seamless Multi-Author Expansion:** Librarians can register new authors on the fly right inside the "Add New Book" dialog without workflow interruption.
4. **Auditing and Operational Transparency:** Complete accountability via the `audit_logs` table tracking every system modification.

### System Verification & Interface Artifacts
- **Figure 1: Entity-Relationship Diagram:** Depicts the 8 tables, keys, and normalized cardinalities.
- **Figure 2: System Architecture Diagram:** Illustrates the 3-Tier interaction between UI, Python REST Controller, and SQLite engine.
- **Figure 3: Web Dashboard Overview:** Real-time metrics highlighting 6 critical KPIs (Total Titles, Total Copies, Available Volumes, Borrowed Books, Active Members, Pending Fines).
- **Figure 4: Book Catalog & Add Author Dialog:** Demonstrates catalog listing and the newly integrated dynamic "➕ Add New Author" capability.
- **Figure 5: Issue & Return Circulation Terminal:** Displays active loans, overdue calculations, and one-click return processing.

---

## 11. Conclusion
The Automated Library Management System demonstrates the practical application of core Database Management Systems principles. By applying 3NF normalization, referential integrity rules, event-driven database triggers, and pre-compiled analytical views, the system eliminates operational anomalies, enforces inventory constraints, and automates overdue penalty computations. The integration of dual client interfaces (Python Desktop GUI and Web REST Application) proves that a well-designed relational foundation can support multi-platform operational workflows while preserving data consistency and ACID guarantees.

---

## 12. References
1. PostgreSQL Global Development Group, *PostgreSQL Documentation*, https://www.postgresql.org/docs/
2. Python Software Foundation, *Python Documentation*, https://docs.python.org/3/
3. Pallets Projects, *Flask Documentation*, https://flask.palletsprojects.com/
4. MDN Web Docs, *HTML, CSS, and JavaScript Guides*, https://developer.mozilla.org/
5. W3Schools, *SQL Tutorial*, https://www.w3schools.com/sql/
6. R. Elmasri and S. B. Navathe, *Fundamentals of Database Systems*, Pearson Education.
