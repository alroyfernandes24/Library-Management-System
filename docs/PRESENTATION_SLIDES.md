# 📊 Library Management System — Micro Project Presentation Deck
## Database Management Systems (DBMS) Presentation & Viva Slides

---

### Slide 1: Title Slide
- **Title:** Library Management System
- **Subtitle:** Automated Relational Architecture, Active Triggers, and Multi-Client Frontends
- **Tech Stack:** Python 3 (Tkinter & Web REST) • SQLite 3 / MySQL 8.0 • 3NF Normalization
- **Presented by:**
  - Atharva Doke – Roll No: 11388
  - Aditya Chitimilla – Roll No: 11385
  - Alroy Fernandes – Roll No: 11393
- **Class:** S.E. CSE | Academic Year: 2026–27 | Guide: Prof. Afreen Sayed
- **Institution:** Fr. Conceicao Rodrigues College of Engineering, Bandra (W), Mumbai
- **Speaker Note:** *"Good morning respected faculty and examiner. Today we present our DBMS Micro Project: an Automated Library Management System built with strict relational integrity, automated trigger-driven fine calculation, and dual desktop and web client applications."*

---

### Slide 2: Project Overview
- **Core Operations:**
  - Complete catalog management across genres and multi-author book mappings.
  - Patron quota enforcement (Student: 3 books, Faculty: 8 books).
  - Automated stock decrementation on issue and restoration on return.
  - Automated overdue fine imposition (₹5.00/day) via active database triggers.
  - Dual responsive frontends: Python Tkinter Desktop GUI & Bootstrap 5 Web Client.
- **Embedded Visual:** Live Web Dashboard KPI metrics (Total Titles, Total Volumes, Shelf Stock, Active Patrons, Dues).
- **Speaker Note:** *"Our system eliminates paper ledgers and manual calculation errors, centralizing all inventory and circulation data into an automated relational database engine."*

---

### Slide 3: Problem Statement & Proposed Solution
- **Traditional Record Challenges:**
  - *Data Redundancy:* Author names and book details repeatedly transcribed across ledgers.
  - *Update Anomalies:* Updating author or category information causes inconsistencies.
  - *Deletion Anomalies:* Deleting loan history inadvertently deletes book or member records.
  - *Stock Drift:* Absence of constraints allows books to be issued with zero physical copies.
  - *Manual Fine Calculation:* Calculating late fees manually leads to human error and revenue loss.
  - *No Audit Trail:* Lack of tamper-proof logging for catalog mutations.
- **Proposed Relational Solution:**
  - *Centralized Relational Store:* 3NF normalized schema across 8 dedicated tables.
  - *Check Constraints:* `CHECK(available_copies <= total_copies AND available_copies >= 0)`.
  - *Event Triggers:* Autonomous database triggers sync stock and calculate fines.
  - *Dynamic Author Creation:* Register new authors on-the-fly during book entry.
  - *Referential Integrity:* `ON DELETE CASCADE` prevents orphaned child records.
  - *Permanent Auditing:* `audit_logs` table records every database mutation with timestamps.
- **Speaker Note:** *"By moving from flat files or registers to a relational DBMS, we enforce ACID properties and guarantee data integrity at the database layer rather than relying on error-prone manual entry."*

---

### Slide 4: Project Objectives
1. **3NF Normalized Relational Design:** Eliminate insertion, update, and deletion anomalies across 8 dedicated tables with composite junction entities.
2. **Autonomous Event-Driven Database Triggers:** Deploy triggers for automatic stock decrementation on issue, stock restoration on return, and ₹5/day overdue fine computation.
3. **Strict Referential & Domain Integrity Constraints:** Implement PKs, FKs, domain CHECK constraints, and UNIQUE rules ensuring shelf stock can never fall below zero.
4. **Multi-Author Attribution & Dynamic Author Registration:** Resolve Many-to-Many book-author relationships with dynamic author registration from the Add Book interface.
5. **Dual User Interface Deployment:** Provide accessible frontends (Desktop Tkinter GUI and Bootstrap 5 REST Client) for catalog browsing and SQL analytics.
- **Speaker Note:** *"Our main goal was not just building an interface, but leveraging the full power of a DBMS: triggers, views, normalization, and constraints."*

---

### Slide 5: Scope of the Project
- **Book Catalog & Author Management:** Full CRUD on books and genres, on-the-fly author creation, ISBN validation, and real-time shelf tracking.
- **Membership Registry:** Tiered quotas (Student: 3, Faculty: 8), email uniqueness, and real-time loan tracking.
- **Circulation & Fines:** Controlled checkouts, return date auto-stamping, trigger-based late fee imposition, and fine receipt settlement.
- **Audit Trails & Analytics:** System event logging, pre-compiled analytical views, and live KPI dashboards.
- **Boundaries / Outside Scope:** Physical RFID barcode scanners, online external payment gateways (fines are cleared by librarians), and inter-library courier networks.
- **Speaker Note:** *"The scope covers the full operational lifecycle of a campus library while clearly scoping hardware and payment gateways out of this micro project."*

---

### Slide 6: Proposed System Architecture (3-Tier)
- **Tier 1: Presentation Layer:** Python Tkinter Desktop GUI for circulation counters and HTML5/Bootstrap 5 Web Portal for campus-wide access.
- **Tier 2: Application / Business Logic Layer:** Python REST controller (`db_manager.py` and `app_web.py`) enforcing quota rules, transactional boundaries, and input validation.
- **Tier 3: Relational Database Engine:** SQLite 3 (or MySQL 8.0) enforcing primary/foreign keys, domain checks, event triggers, and analytical views.
- **ACID Guarantees:** Ensures atomic borrow and return operations without race conditions.
- **Speaker Note:** *"Our 3-tier architecture decouples UI from the database engine, ensuring business rules and integrity constraints are enforced at the database layer."*

---

### Slide 7: Database Design: Entity-Relationship Model
- **Entities & Relationships:**
  - `CATEGORIES` (1) ——— (N) `BOOKS` (Genre classification)
  - `BOOKS` (N) ——— (M) `AUTHORS` (Resolved via `BOOK_AUTHORS` composite junction entity)
  - `MEMBERS` (1) ——— (N) `BORROW_TRANSACTIONS` (Quota-governed loans)
  - `BOOKS` (1) ——— (N) `BORROW_TRANSACTIONS` (Books issued across transactions)
  - `BORROW_TRANSACTIONS` (1) ——— (0..1) `FINES` (Overdue loans incur at most one fine record)
  - `AUDIT_LOGS` (Independent system-wide event logging)
- **Speaker Note:** *"Here is our ER diagram. Notice the junction entity `BOOK_AUTHORS` with a composite primary key that neatly normalizes the Many-to-Many relationship between books and authors."*

---

### Slide 8: Relational Schema & Key Constraints
| Table Name | Primary Key | Foreign Key(s) | Constraints & Domain Rules |
| :--- | :--- | :--- | :--- |
| `categories` | `category_id` | None | `category_name UNIQUE, NOT NULL` |
| `authors` | `author_id` | None | `author_name NOT NULL` |
| `books` | `book_id` | `category_id` $\rightarrow$ `categories` | `isbn UNIQUE`, `CHECK(available_copies <= total_copies)` |
| `book_authors` | `(book_id, author_id)` | `book_id` $\rightarrow$ `books`, `author_id` $\rightarrow$ `authors` | `ON DELETE CASCADE` (Composite PK, M:N) |
| `members` | `member_id` | None | `email UNIQUE`, `CHECK(max_books_allowed > 0)` |
| `borrow_transactions` | `transaction_id` | `book_id` $\rightarrow$ `books`, `member_id` $\rightarrow$ `members` | `ON DELETE CASCADE` |
| `fines` | `fine_id` | `transaction_id` $\rightarrow$ `borrow_transactions`, `member_id` $\rightarrow$ `members` | `transaction_id UNIQUE`, `fine_amount >= 0` |
| `audit_logs` | `log_id` | None | System timestamp tracking |
- **Speaker Note:** *"Every table is in 3NF. We enforce referential actions like `ON DELETE CASCADE` so deleting a transaction safely removes its associated fine record without leaving orphaned rows."*

---

### Slide 9: SQL Implementation Matrix
- **DDL:** `CREATE TABLE`, `DROP TABLE`, `ALTER TABLE`, Primary/Foreign keys, `CHECK`, `UNIQUE`, `NOT NULL`.
- **DML:** Parameterized `INSERT INTO`, conditional `UPDATE`, and cascaded `DELETE`.
- **DQL:** `INNER JOIN`, `LEFT JOIN`, `GROUP_CONCAT`, `WHERE`, `LIKE`, `ORDER BY`, `LIMIT`.
- **Triggers:**
  - `trg_after_issue_book`: Decrements `available_copies` on `books` after loan insertion.
  - `trg_after_return_book`: Increments `available_copies` when `return_date` is updated.
  - `trg_calculate_fine_on_return`: Computes $(\text{return\_date} - \text{due\_date}) \times 5.00$ and inserts into `fines`.
- **Views:** `vw_book_catalog`, `vw_active_loans`, `vw_library_summary`.
- **Speaker Note:** *"We implemented the three classic SQL triggers to automate routine catalog updates and financial penalties without any human intervention."*

---

### Slide 10: SQL Queries & Execution Results
- **Query 1:** Catalog listing with multi-author string aggregation (`GROUP_CONCAT`) and genre category joins.
- **Query 2:** Active loans retrieval calculating days overdue in real time using conditional `CASE` expressions and Julian date arithmetic (`JULIANDAY(DATE('now')) - JULIANDAY(t.due_date)`).
- **Speaker Note:** *"These queries showcase our use of advanced SQL: conditional CASE logic, date arithmetic, and multi-table joins."*

---

### Slide 11: Advanced SQL Queries & Aggregate Analytics
- **Query 3:** Category inventory distribution aggregating total physical volumes (`SUM`) and titles (`COUNT`) filtered by `HAVING SUM(b.total_copies) >= 5`.
- **Query 4:** Outstanding unpaid fines report joining `fines`, `members`, `borrow_transactions`, and `books` to generate actionable penalty recovery lists.
- **Speaker Note:** *"Notice the use of the `HAVING` clause in Query 3, which filters aggregated groups rather than individual rows, answering managerial questions about book stock."*

---

### Slide 12: Application Interface & Dynamic Author Creation
- **Screenshots:**
  - Book catalog listing with live keyword search and genre filter.
  - Add New Book modal highlighting the newly implemented **"➕ Add New Author"** sub-interface.
- **Key Highlight:** When adding a book, if the author does not yet exist in the database, the librarian can register the author immediately without leaving the form or losing entered book details.
- **Speaker Note:** *"We resolved the workflow bottleneck where adding a book by a new author previously failed: now librarians can dynamically register new authors right inside the dialog."*

---

### Slide 13: Circulation Desk & Dues Settlement
- **Screenshots:**
  - Active loans interface with due date indicators and one-click return processing.
  - Fines tracker displaying assessed penalties, patron contact numbers, and one-click "Mark as Paid" receipt actions.
- **Speaker Note:** *"Clicking 'Return Book' triggers the database trigger, updates stock on the shelf instantly, and if late, generates an entry in the fines table."*

---

### Slide 14: Expected Outcome & Conclusion
- **Key Outcomes:**
  - Persistent, centralized, 3NF-normalized data store.
  - Automated business logic through database triggers.
  - Zero stock corruption via check constraints.
  - Seamless on-the-fly author addition.
  - Transparent audit trail tracking all catalog changes.
- **DBMS Concepts Demonstrated:** Normalization (1NF-3NF), Referential Integrity, DDL/DML/DQL, Triggers, Views, and ACID Transactions.
- **Speaker Note:** *"In conclusion, this project demonstrates how relational database principles translate into a robust, anomaly-free administrative application."*

---

### Slide 15: References & Thank You
- **References:**
  - R. Elmasri & S. B. Navathe, *Fundamentals of Database Systems*, 7th ed., Pearson, 2017.
  - A. Silberschatz, H. F. Korth, & S. Sudarshan, *Database System Concepts*, 7th ed., McGraw-Hill, 2019.
  - SQLite 3 Official Documentation (Triggers & Foreign Keys).
  - MySQL 8.0 Reference Manual.
  - Python Software Foundation (sqlite3 DB-API).
- **Speaker Note:** *"Thank you for your time. We are now ready for your questions and the viva examination."*
