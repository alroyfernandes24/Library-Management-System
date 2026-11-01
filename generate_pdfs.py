"""
PDF Generator for Library Management System
Generates two high-quality academic PDFs:
1. Library_Management_System_Project_Report.pdf (Complete submission report)
2. Teacher_Presentation_and_Viva_Guide.pdf (Presentation & Viva cheat sheet)
Uses Microsoft Edge headless rendering engine for pixel-perfect PDF output.
"""

import os
import subprocess
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
]

def get_edge_path():
    for p in EDGE_PATHS:
        if os.path.exists(p):
            return p
    raise FileNotFoundError("Microsoft Edge executable not found.")

def convert_html_to_pdf(html_path, pdf_path):
    edge = get_edge_path()
    file_url = "file:///" + os.path.abspath(html_path).replace("\\", "/")
    cmd = [
        edge,
        "--headless=new",
        "--disable-gpu",
        f"--print-to-pdf={os.path.abspath(pdf_path)}",
        "--no-pdf-header-footer",
        file_url
    ]
    subprocess.run(cmd, check=True)
    time.sleep(1)
    if os.path.exists(pdf_path):
        print(f"[+] Successfully generated PDF: {os.path.basename(pdf_path)} ({os.path.getsize(pdf_path)} bytes)")
    else:
        raise RuntimeError(f"Failed to generate {pdf_path}")


COMMON_CSS = """
<style>
    @page {
        size: A4;
        margin: 18mm 16mm 18mm 16mm;
    }
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #1e293b;
        line-height: 1.6;
        font-size: 10.5pt;
    }
    h1, h2, h3, h4 {
        color: #0f172a;
        font-weight: 700;
        margin-top: 18pt;
        margin-bottom: 8pt;
    }
    h1 { font-size: 20pt; border-bottom: 2px solid #2563eb; padding-bottom: 4pt; }
    h2 { font-size: 14pt; border-bottom: 1px solid #cbd5e1; padding-bottom: 3pt; color: #1e40af; }
    h3 { font-size: 11.5pt; color: #334155; }
    
    p { margin-top: 0; margin-bottom: 8pt; }
    
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 12pt 0;
        font-size: 9.5pt;
    }
    th, td {
        border: 1px solid #cbd5e1;
        padding: 6pt 8pt;
        text-align: left;
    }
    th {
        background-color: #f1f5f9;
        font-weight: 600;
        color: #0f172a;
    }
    tr:nth-child(even) {
        background-color: #f8fafc;
    }
    
    code {
        font-family: Consolas, "Courier New", monospace;
        font-size: 9pt;
        background-color: #f1f5f9;
        padding: 1.5pt 4pt;
        border-radius: 3pt;
        color: #b91c1c;
    }
    pre {
        background-color: #0f172a;
        color: #f8fafc;
        padding: 10pt;
        border-radius: 5pt;
        font-family: Consolas, "Courier New", monospace;
        font-size: 8.5pt;
        line-height: 1.45;
        overflow-x: auto;
        margin: 10pt 0;
    }
    pre code {
        background-color: transparent;
        color: inherit;
        padding: 0;
    }
    
    .cover-page {
        page-break-after: always;
        text-align: center;
        padding-top: 80pt;
    }
    .cover-title {
        font-size: 26pt;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 10pt;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .cover-subtitle {
        font-size: 13pt;
        color: #475569;
        margin-bottom: 40pt;
    }
    .cover-badge {
        display: inline-block;
        background-color: #eff6ff;
        color: #1d4ed8;
        padding: 6pt 16pt;
        border-radius: 20pt;
        font-size: 11pt;
        font-weight: 600;
        border: 1px solid #bfdbfe;
        margin-bottom: 60pt;
    }
    .cover-meta {
        font-size: 11pt;
        margin-top: 100pt;
        border-top: 1px solid #e2e8f0;
        padding-top: 20pt;
    }
    
    .page-break {
        page-break-before: always;
    }
    
    .callout {
        background-color: #f0fdf4;
        border-left: 4px solid #16a34a;
        padding: 8pt 12pt;
        margin: 10pt 0;
        border-radius: 0 4pt 4pt 0;
    }
    .callout-warning {
        background-color: #fffbeb;
        border-left: 4px solid #d97402;
    }
    
    .q-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 6pt;
        padding: 10pt;
        margin-bottom: 10pt;
    }
    .q-title {
        font-weight: 700;
        color: #1e40af;
        margin-bottom: 4pt;
    }
    .diagram-box {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        padding: 10pt;
        font-family: Consolas, monospace;
        font-size: 8.5pt;
        line-height: 1.4;
        margin: 12pt 0;
        border-radius: 4pt;
        white-space: pre;
    }
</style>
"""


def generate_report_html():
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Library Management System - DBMS Project Report</title>
    {COMMON_CSS}
</head>
<body>

<!-- 1. COVER PAGE -->
<div class="cover-page">
    <div style="font-size: 14pt; font-weight: 700; color: #64748b; margin-bottom: 15pt;">DEPARTMENT OF COMPUTER SCIENCE &amp; ENGINEERING</div>
    <div class="cover-title">Library Management System</div>
    <div class="cover-subtitle">A Database Management Systems (DBMS) Mini Project Report</div>
    
    <div class="cover-badge">Third Normal Form (3NF) &bull; Automated Triggers &bull; Stored Procedures</div>
    
    <!-- TEAM MEMBERS SECTION -->
    <div style="margin: 25pt auto 30pt auto; max-width: 480px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8pt; padding: 14pt 20pt; text-align: left; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size: 10.5pt; font-weight: 700; color: #1e40af; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10pt; border-bottom: 2px solid #3b82f6; padding-bottom: 4pt;">
            Project Submitted By (Team Members)
        </div>
        <table style="width: 100%; border: none; margin: 0; font-size: 10.5pt; background: transparent;">
            <tr style="background: transparent;">
                <td style="border: none; padding: 5pt 0; font-weight: 600; color: #0f172a;">1. Atharva Doke</td>
                <td style="border: none; padding: 5pt 0; text-align: right; color: #475569;">Roll No: <strong style="color: #1e40af;">11388</strong></td>
            </tr>
            <tr style="background: transparent;">
                <td style="border: none; padding: 5pt 0; font-weight: 600; color: #0f172a;">2. Aditya Chitimilla</td>
                <td style="border: none; padding: 5pt 0; text-align: right; color: #475569;">Roll No: <strong style="color: #1e40af;">11385</strong></td>
            </tr>
            <tr style="background: transparent;">
                <td style="border: none; padding: 5pt 0; font-weight: 600; color: #0f172a;">3. Alroy Fernandes</td>
                <td style="border: none; padding: 5pt 0; text-align: right; color: #475569;">Roll No: <strong style="color: #1e40af;">11393</strong></td>
            </tr>
        </table>
    </div>

    <div class="cover-meta" style="margin-top: 30pt;">
        <p><strong>Course:</strong> Database Management Systems (CS304 / IT304)</p>
        <p><strong>Academic Year:</strong> 2026 – 2027</p>
        <p><strong>Database Engine:</strong> SQLite 3 &amp; MySQL 8.0</p>
        <p><strong>Application Layer:</strong> Python 3 (Web Server &amp; Desktop GUI)</p>
    </div>
</div>

<!-- 2. ABSTRACT & INTRODUCTION -->
<div class="page-break"></div>
<h1>1. Executive Summary &amp; Problem Statement</h1>

<h3>1.1 Executive Summary</h3>
<p>
This project demonstrates the complete engineering lifecycle of an <strong>Automated Library Management System</strong> built upon a Third Normal Form (3NF) relational database architecture. The system models physical libraries with categories, multi-author books, membership categories, borrow transactions with real-time stock decrement, overdue penalty computation (₹5/day), and an immutable audit trail.
</p>

<h3>1.2 Problem Definition</h3>
<p>Traditional flat file and spreadsheet solutions suffer from severe data anomalies:</p>
<ul>
    <li><strong>Redundancy &amp; Inconsistency:</strong> Multiple copies of student and book details lead to conflicting records.</li>
    <li><strong>Anomalies:</strong> Updating author information in one record leaves others inconsistent (Update Anomaly); deleting a borrow record risks deleting book catalog data (Deletion Anomaly).</li>
    <li><strong>Manual Overdue Tracking:</strong> Fines computed manually result in delays and mathematical inaccuracies.</li>
    <li><strong>Concurrency Violations:</strong> Books issued beyond available copies cause inventory corruption without database-level constraints.</li>
</ul>

<h3>1.3 Objectives</h3>
<ul>
    <li>Design an 8-table relational schema eliminating partial and transitive functional dependencies (3NF).</li>
    <li>Enforce referential integrity with foreign key cascading and nullification rules.</li>
    <li>Shift critical business logic from application code into the database engine using <strong>SQL Triggers</strong> and <strong>Stored Procedures</strong>.</li>
    <li>Provide zero-configuration, instant execution via Python's built-in standard libraries.</li>
</ul>

<!-- 4. SYSTEM ARCHITECTURE & ER MODEL -->
<div class="page-break"></div>
<h1>2. System Architecture &amp; ER Modeling</h1>

<h3>2.1 Three-Tier System Architecture</h3>
<div class="diagram-box">
+-------------------------------------------------------------------------+
|                        TIER 1: PRESENTATION LAYER                       |
|   • Modern Web UI (Bootstrap 5, AJAX)    • Desktop GUI (Tkinter App)    |
+------------------------------------+------------------------------------+
                                     | JSON REST API / Direct Function Calls
                                     v
+-------------------------------------------------------------------------+
|                     TIER 2: APPLICATION LOGIC LAYER                     |
|   • app_web.py / app_gui.py              • db_manager.py                |
|   • Parameterized Queries (Anti-SQLi)    • Error & Connection Handlers  |
+------------------------------------+------------------------------------+
                                     | Parameterized SQL Queries
                                     v
+-------------------------------------------------------------------------+
|                      TIER 3: DATABASE ENGINE (RDBMS)                    |
|   • 8 Relational Tables (3NF)            • Automated SQL Triggers       |
|   • Precomputed Reporting Views          • Immutable Audit Logs         |
+-------------------------------------------------------------------------+
</div>

<h3>2.2 Entity-Relationship (ER) Schema</h3>
<p>The schema captures 8 relational entities:</p>
<ul>
    <li><code>CATEGORIES</code> (1:M with <code>BOOKS</code>)</li>
    <li><code>AUTHORS</code> (M:N with <code>BOOKS</code> via <code>BOOK_AUTHORS</code>)</li>
    <li><code>BOOKS</code> (1:M with <code>BORROW_TRANSACTIONS</code>)</li>
    <li><code>MEMBERS</code> (1:M with <code>BORROW_TRANSACTIONS</code>)</li>
    <li><code>BORROW_TRANSACTIONS</code> (1:1 with <code>FINES</code>)</li>
    <li><code>AUDIT_LOGS</code> (Independent operational log)</li>
</ul>

<div class="diagram-box">
 [CATEGORIES] 1 ----- M [BOOKS] 1 ----- M [BOOK_AUTHORS] M ----- 1 [AUTHORS]
                          1
                          |
                          M
               [BORROW_TRANSACTIONS] M ----- 1 [MEMBERS]
                          1
                          |
                          1
                       [FINES]
</div>

<!-- 5. NORMALIZATION ANALYSIS -->
<div class="page-break"></div>
<h1>3. Relational Schema &amp; Normalization Proofs</h1>

<h3>3.1 First Normal Form (1NF)</h3>
<p>
<strong>Requirement:</strong> Each column must be atomic, with no multi-valued attributes or repeating groups.<br>
<strong>Proof:</strong> In traditional unnormalized designs, multiple authors are stored as a CSV string inside a <code>books</code> row (e.g. <code>"Silberschatz, Korth"</code>). We decomposed this relationship into a junction table:
<br><code>book_authors(<u>book_id</u>, <u>author_id</u>)</code>
<br>Each column is indivisible and atomic, fulfilling 1NF.
</p>

<h3>3.2 Second Normal Form (2NF)</h3>
<p>
<strong>Requirement:</strong> The relation must be in 1NF and contain zero partial functional dependencies on composite primary keys.<br>
<strong>Proof:</strong> In <code>book_authors</code>, the primary key is composite <code>(book_id, author_id)</code>. All non-key attributes describing an author (such as <code>author_name</code>) reside solely in the <code>authors</code> table, while attributes describing books reside in <code>books</code>. No non-prime attribute depends on a subset of the candidate key.
</p>

<h3>3.3 Third Normal Form (3NF)</h3>
<p>
<strong>Requirement:</strong> The relation must be in 2NF with no transitive dependencies (i.e. $X \rightarrow Y$ and $Y \rightarrow Z$).<br>
<strong>Proof:</strong> In the <code>books</code> relation, storing category details directly would cause a transitive dependency:
<br><code>book_id &rarr; category_id &rarr; category_name</code>
<br>We decoupled category attributes into <code>categories(<u>category_id</u>, category_name, description)</code>. Non-key attributes in <code>books</code> now depend strictly and solely on the primary key <code>book_id</code>.
</p>

<!-- 6. DATA DICTIONARY -->
<div class="page-break"></div>
<h1>4. Data Dictionary &amp; Table Specifications</h1>

<table>
    <thead>
        <tr>
            <th>Table Name</th>
            <th>Primary Key</th>
            <th>Foreign Keys</th>
            <th>Integrity Constraints &amp; Rules</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>categories</code></td>
            <td><code>category_id</code></td>
            <td>None</td>
            <td><code>category_name UNIQUE NOT NULL</code></td>
        </tr>
        <tr>
            <td><code>authors</code></td>
            <td><code>author_id</code></td>
            <td>None</td>
            <td><code>author_name NOT NULL</code></td>
        </tr>
        <tr>
            <td><code>books</code></td>
            <td><code>book_id</code></td>
            <td><code>category_id &rarr; categories</code></td>
            <td><code>isbn UNIQUE</code>, <code>CHECK(available_copies &le; total_copies)</code></td>
        </tr>
        <tr>
            <td><code>book_authors</code></td>
            <td><code>(book_id, author_id)</code></td>
            <td><code>book_id &rarr; books</code>, <code>author_id &rarr; authors</code></td>
            <td><code>ON DELETE CASCADE</code> on both foreign keys</td>
        </tr>
        <tr>
            <td><code>members</code></td>
            <td><code>member_id</code></td>
            <td>None</td>
            <td><code>email UNIQUE</code>, <code>CHECK(membership_type IN ('Student','Faculty','General'))</code></td>
        </tr>
        <tr>
            <td><code>borrow_transactions</code></td>
            <td><code>transaction_id</code></td>
            <td><code>book_id &rarr; books</code>, <code>member_id &rarr; members</code></td>
            <td><code>status IN ('Issued','Returned','Overdue')</code></td>
        </tr>
        <tr>
            <td><code>fines</code></td>
            <td><code>fine_id</code></td>
            <td><code>transaction_id &rarr; borrow_transactions</code></td>
            <td><code>transaction_id UNIQUE</code>, <code>fine_amount &ge; 0</code></td>
        </tr>
        <tr>
            <td><code>audit_logs</code></td>
            <td><code>log_id</code></td>
            <td>None</td>
            <td><code>created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP</code></td>
        </tr>
    </tbody>
</table>

<!-- 7. TRIGGERS, VIEWS, PROCEDURES -->
<div class="page-break"></div>
<h1>5. Database Logic: Triggers, Views &amp; Procedures</h1>

<h3>5.1 Automated Stock Management Triggers</h3>
<pre><code>-- Decrement Available Stock on Book Issue
CREATE TRIGGER trg_after_issue_book
AFTER INSERT ON borrow_transactions
WHEN NEW.status = 'Issued'
BEGIN
    UPDATE books 
    SET available_copies = available_copies - 1
    WHERE book_id = NEW.book_id;

    INSERT INTO audit_logs (table_name, action_type, description)
    VALUES ('borrow_transactions', 'ISSUE', 
            'Book ID ' || NEW.book_id || ' issued to Member ID ' || NEW.member_id);
END;

-- Restore Stock on Return
CREATE TRIGGER trg_after_return_book
AFTER UPDATE OF return_date ON borrow_transactions
WHEN OLD.return_date IS NULL AND NEW.return_date IS NOT NULL
BEGIN
    UPDATE books 
    SET available_copies = available_copies + 1
    WHERE book_id = NEW.book_id;

    INSERT INTO audit_logs (table_name, action_type, description)
    VALUES ('borrow_transactions', 'RETURN', 
            'Book ID ' || NEW.book_id || ' returned by Member ID ' || NEW.member_id);
END;</code></pre>

<h3>5.2 Automated Overdue Fine Trigger (₹5.00 / day)</h3>
<pre><code>CREATE TRIGGER trg_calculate_fine_on_return
AFTER UPDATE OF return_date ON borrow_transactions
WHEN OLD.return_date IS NULL AND NEW.return_date IS NOT NULL AND julianday(NEW.return_date) > julianday(NEW.due_date)
BEGIN
    INSERT INTO fines (transaction_id, member_id, fine_amount, paid_status)
    VALUES (
        NEW.transaction_id,
        NEW.member_id,
        ROUND((julianday(NEW.return_date) - julianday(NEW.due_date)) * 5.0, 2),
        'Unpaid'
    );
END;</code></pre>

<!-- 8. COMPLEX SQL QUERIES -->
<div class="page-break"></div>
<h1>6. Complex SQL Queries &amp; Verification Testing</h1>

<h3>Query 1: Multi-Table Join across M:N Relationship</h3>
<pre><code>SELECT b.title, c.category_name, a.author_name
FROM books b
JOIN categories c ON b.category_id = c.category_id
JOIN book_authors ba ON b.book_id = ba.book_id
JOIN authors a ON ba.author_id = a.author_id
ORDER BY b.title;</code></pre>

<h3>Query 2: Defaulter Identification via Correlated Subquery</h3>
<pre><code>SELECT m.member_id, m.first_name, m.last_name, m.email
FROM members m
WHERE EXISTS (
    SELECT 1 
    FROM borrow_transactions t 
    WHERE t.member_id = m.member_id 
      AND t.return_date IS NULL 
      AND DATE('now') > t.due_date
);</code></pre>

<h3>6.1 System Verification &amp; Test Cases</h3>
<table>
    <thead>
        <tr>
            <th>Test ID</th>
            <th>Operation Under Test</th>
            <th>Input Data</th>
            <th>Expected Database Output</th>
            <th>Status</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>TC-01</td>
            <td>Book Addition</td>
            <td>Title: "Distributed Systems", Copies: 5</td>
            <td>Inserted with auto-increment ID; copies = 5</td>
            <td><strong>PASS</strong></td>
        </tr>
        <tr>
            <td>TC-02</td>
            <td>Book Borrow Trigger</td>
            <td>Book ID: 1, Member ID: 1</td>
            <td>Available copies decremented from 8 to 7</td>
            <td><strong>PASS</strong></td>
        </tr>
        <tr>
            <td>TC-03</td>
            <td>Quota Enforcement</td>
            <td>Student with 4 active loans</td>
            <td>Insert blocked by business rule constraint</td>
            <td><strong>PASS</strong></td>
        </tr>
        <tr>
            <td>TC-04</td>
            <td>Overdue Fine Trigger</td>
            <td>Return date 8 days past due date</td>
            <td>Fine record of ₹40.00 created automatically</td>
            <td><strong>PASS</strong></td>
        </tr>
        <tr>
            <td>TC-05</td>
            <td>Fine Settlement</td>
            <td>Mark Fine ID 1 as Paid</td>
            <td>Status updated to 'Paid'; paid_date set to today</td>
            <td><strong>PASS</strong></td>
        </tr>
    </tbody>
</table>

<!-- 9. CONCLUSION -->
<div class="page-break"></div>
<h1>7. Conclusion &amp; Academic Findings</h1>
<p>
The <strong>Library Management System</strong> project confirms that embedding data validation, relationship decomposition (3NF), and business rules directly inside an RDBMS engine produces resilient, anomaly-free systems.
</p>
<div class="callout">
    <strong>Key Technical Takeaways:</strong>
    <ul>
        <li><strong>Data Integrity at Storage Layer:</strong> By relying on SQL triggers rather than frontend JavaScript or Python logic for stock tracking and fines, data corruption is made impossible regardless of the client tool used.</li>
        <li><strong>Referential Consistency:</strong> Junction tables and cascading foreign keys guarantee that records can never be orphaned.</li>
        <li><strong>Portability:</strong> Standard library implementation guarantees execution across any workstation without environment setup bottlenecks.</li>
    </ul>
</div>

</body>
</html>
"""


def generate_guide_html():
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Teacher Presentation &amp; Viva Voce Guide</title>
    {COMMON_CSS}
</head>
<body>

<h1>Teacher Presentation &amp; Viva Voce Guide</h1>
<p style="margin-bottom: 4pt;"><strong>Project:</strong> Library Management System (DBMS Mini Project)</p>
<p style="color: #475569; font-size: 10pt; margin-bottom: 12pt;">
    <strong>Team Members:</strong> 
    Atharva Doke (11388) &bull; Aditya Chitimilla (11385) &bull; Alroy Fernandes (11393)
</p>

<div class="callout">
    <strong>How to Handle the Teacher's #1 Question:</strong><br>
    <em>"If you add or delete in the UI, does it actually reflect in the database?"</em><br>
    <strong>Answer:</strong> <em>"Yes Ma'am/Sir! Every UI button executes a genuine SQL query on our SQLite/MySQL database. Let me demonstrate live right now."</em>
</div>

<h2>30-Second Live Verification Routine</h2>
<ol>
    <li><strong>Step 1:</strong> In the Web or Desktop UI, click <strong>"Add New Book"</strong>. Enter:
        <ul>
            <li>Title: <code>Cloud Architecture Principles</code></li>
            <li>ISBN: <code>978-0139999999</code></li>
            <li>Copies: <code>5</code></li>
        </ul>
    </li>
    <li><strong>Step 2:</strong> Save the book. Show that it appears in the catalog.</li>
    <li><strong>Step 3 (The Terminal Proof):</strong> Open a command prompt or run <code>verify_database.bat</code> and press <code>1</code>. Show the examiner that <code>Cloud Architecture Principles</code> is recorded directly in the SQL <code>books</code> table!</li>
    <li><strong>Step 4 (Trigger Demonstration):</strong> Issue this book to any member. Refresh the table or view: <code>available_copies</code> has dropped from <code>5</code> to <code>4</code> automatically due to trigger <code>trg_after_issue_book</code>!</li>
</ol>

<h2>Top 10 Viva Voce Questions &amp; Model Answers</h2>

<div class="q-box">
    <div class="q-title">Q1: Why did you create the separate table book_authors?</div>
    <div><strong>Answer:</strong> Books and Authors have a <strong>Many-to-Many (M:N) relationship</strong>. If we stored multiple authors in a single column in <code>books</code>, it would violate <strong>First Normal Form (1NF)</strong>. The junction table decomposes M:N into two 1:M relationships using composite primary key <code>(book_id, author_id)</code>.</div>
</div>

<div class="q-box">
    <div class="q-title">Q2: Is fine calculation done in Python or SQL?</div>
    <div><strong>Answer:</strong> It is performed in SQL by the database trigger <strong><code>trg_calculate_fine_on_return</code></strong>. When a return date is updated, if <code>return_date > due_date</code>, the DBMS calculates: <code>(return_date - due_date) &times; ₹5.00</code> and inserts an unpaid record into the <code>fines</code> table.</div>
</div>

<div class="q-box">
    <div class="q-title">Q3: How is inventory prevented from becoming negative?</div>
    <div><strong>Answer:</strong> The database enforces a <code>CHECK (available_copies &ge; 0)</code> constraint, and our application checks <code>available_copies > 0</code> prior to inserting into <code>borrow_transactions</code>.</div>
</div>

<div class="q-box">
    <div class="q-title">Q4: What is the purpose of database Views in your project?</div>
    <div><strong>Answer:</strong> We use <strong><code>vw_book_catalog</code></strong> and <strong><code>vw_active_loans</code></strong> for data abstraction. They join multiple tables and perform author name aggregation (<code>GROUP_CONCAT</code>), allowing queries to run without repeatedly rewriting complex joins.</div>
</div>

<div class="q-box">
    <div class="q-title">Q5: What is the difference between ON DELETE CASCADE and ON DELETE SET NULL here?</div>
    <div><strong>Answer:</strong> We use <code>CASCADE</code> on <code>book_authors</code> so deleting a book removes its author associations. In <code>books(category_id)</code>, we use <code>SET NULL</code> so deleting a category does not accidentally delete books.</div>
</div>

<div class="q-box">
    <div class="q-title">Q6: What are the ACID properties in your database?</div>
    <div><strong>Answer:</strong> Atomicity (transaction rollbacks on failure), Consistency (PK, FK, and CHECK constraints), Isolation (concurrency control), and Durability (WAL logs written permanently to disk in <code>library.db</code>).</div>
</div>

</body>
</html>
"""


def main():
    report_html_path = os.path.join(BASE_DIR, "report_temp.html")
    report_pdf_path = os.path.join(BASE_DIR, "Library_Management_System_Project_Report.pdf")

    guide_html_path = os.path.join(BASE_DIR, "guide_temp.html")
    guide_pdf_path = os.path.join(BASE_DIR, "Teacher_Presentation_and_Viva_Guide.pdf")

    print("[*] Generating HTML sources...")
    with open(report_html_path, "w", encoding="utf-8") as f:
        f.write(generate_report_html())

    with open(guide_html_path, "w", encoding="utf-8") as f:
        f.write(generate_guide_html())

    print("[*] Converting to PDF via Edge Headless...")
    convert_html_to_pdf(report_html_path, report_pdf_path)
    convert_html_to_pdf(guide_html_path, guide_pdf_path)

    # Clean up temporary HTML files
    os.remove(report_html_path)
    os.remove(guide_html_path)
    print("[+] All PDF reports generated successfully!")


if __name__ == "__main__":
    main()
