"""
Generate interactive presentation.html and Library_Management_System_Presentation.pdf
Provides 16:9 widescreen presentation slides in both HTML and PDF formats.
"""

import os
import subprocess
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
DIAG_DIR = os.path.join(DOCS_DIR, "diagrams")
HTML_PATH = os.path.join(DOCS_DIR, "presentation.html")
PDF_PATH = os.path.join(DOCS_DIR, "Library_Management_System_Presentation.pdf")
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def generate_presentation_deck():
    # File URLs for images
    er_img = "file:///" + os.path.join(DIAG_DIR, "er_diagram.png").replace("\\", "/")
    arch_img = "file:///" + os.path.join(DIAG_DIR, "architecture_diagram.png").replace("\\", "/")
    dash_img = "file:///" + os.path.join(DIAG_DIR, "screenshot_dashboard.png").replace("\\", "/")
    cat_img = "file:///" + os.path.join(DIAG_DIR, "screenshot_catalog.png").replace("\\", "/")
    modal_img = "file:///" + os.path.join(DIAG_DIR, "screenshot_add_book_modal.png").replace("\\", "/")
    loans_img = "file:///" + os.path.join(DIAG_DIR, "screenshot_loans.png").replace("\\", "/")
    fines_img = "file:///" + os.path.join(DIAG_DIR, "screenshot_fines.png").replace("\\", "/")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Library Management System - DBMS Micro Project Presentation</title>
<style>
    @page {{
        size: 16in 9in;
        margin: 0;
    }}
    * {{
        box-sizing: border-box;
    }}
    body {{
        margin: 0;
        padding: 0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        background-color: #0f172a;
        color: #1e293b;
    }}
    .slide {{
        width: 16in;
        height: 9in;
        page-break-after: always;
        position: relative;
        overflow: hidden;
        background-color: #f8fafc;
        padding: 0;
        display: flex;
        flex-direction: column;
    }}
    .slide-header {{
        background-color: #0f172a;
        color: #ffffff;
        padding: 24px 48px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 3px solid #2563eb;
    }}
    .slide-header .tagline {{
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1.5px;
        color: #94a3b8;
        text-transform: uppercase;
        margin-bottom: 4px;
    }}
    .slide-header h2 {{
        margin: 0;
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
    }}
    .slide-header .num-badge {{
        background-color: #2563eb;
        color: #ffffff;
        font-size: 18px;
        font-weight: 700;
        padding: 8px 18px;
        border-radius: 8px;
    }}
    .slide-body {{
        flex: 1;
        padding: 32px 48px;
        display: flex;
        gap: 32px;
    }}
    .card {{
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 24px 28px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        flex: 1;
        display: flex;
        flex-direction: column;
    }}
    .card h3 {{
        margin-top: 0;
        margin-bottom: 16px;
        font-size: 20px;
        font-weight: 700;
        color: #1e40af;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 8px;
    }}
    .card ul {{
        margin: 0;
        padding-left: 20px;
        line-height: 1.6;
        font-size: 16px;
        color: #334155;
    }}
    .card li {{
        margin-bottom: 12px;
    }}
    .card-danger h3 {{ color: #dc2626; }}
    .card-success h3 {{ color: #059669; }}
    
    .img-card {{
        flex: 1.2;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 12px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }}
    .img-card img {{
        max-width: 100%;
        max-height: 5.5in;
        object-fit: contain;
        border-radius: 8px;
        border: 1px solid #cbd5e1;
    }}
    .img-caption {{
        font-size: 13px;
        color: #64748b;
        margin-top: 8px;
        font-style: italic;
    }}

    table.slide-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
        margin-top: 8px;
    }}
    table.slide-table th, table.slide-table td {{
        border: 1px solid #cbd5e1;
        padding: 10px 14px;
        text-align: left;
    }}
    table.slide-table th {{
        background-color: #0f172a;
        color: #ffffff;
        font-weight: 600;
    }}
    table.slide-table tr:nth-child(even) {{
        background-color: #f1f5f9;
    }}

    /* Title Slide Special */
    .title-slide {{
        background-color: #0f172a;
        color: #ffffff;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 0 96px;
    }}
    .title-banner {{
        border-left: 6px solid #2563eb;
        padding-left: 36px;
    }}
    .title-category {{
        font-size: 18px;
        font-weight: 700;
        color: #60a5fa;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 16px;
    }}
    .title-main {{
        font-size: 52px;
        font-weight: 800;
        color: #ffffff;
        margin: 0 0 12px 0;
        letter-spacing: -0.5px;
    }}
    .title-sub {{
        font-size: 22px;
        color: #cbd5e1;
        margin-bottom: 36px;
    }}
    .title-authors {{
        font-size: 18px;
        color: #ffffff;
        line-height: 1.7;
    }}
    .title-meta {{
        font-size: 16px;
        color: #94a3b8;
        margin-top: 24px;
    }}

    /* Navigation toolbar in browser */
    @media screen {{
        .slide {{
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            margin: 20px auto;
            border-radius: 8px;
        }}
        #nav-bar {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(15, 23, 42, 0.9);
            padding: 10px 16px;
            border-radius: 30px;
            display: flex;
            gap: 12px;
            z-index: 999;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        }}
        #nav-bar button {{
            background: #2563eb;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: 600;
        }}
    }}
</style>
</head>
<body>

<!-- SLIDE 1: TITLE SLIDE -->
<div class="slide title-slide">
    <div class="title-banner">
        <div class="title-category">DATABASE MANAGEMENT SYSTEMS | MICRO PROJECT</div>
        <h1 class="title-main">Library Management System</h1>
        <div class="title-sub">Python (Tkinter & Web REST) &bull; SQLite 3 / MySQL 8.0 &bull; 3NF Relational Architecture</div>
        <div class="title-authors">
            <strong>Presented by:</strong><br>
            Atharva Doke (11388) &bull; Aditya Chitimilla (11385) &bull; Alroy Fernandes (11393)
        </div>
        <div class="title-meta">
            Class: S.E. CSE &bull; Academic Year: 2026–27 &bull; Guide: Prof. Afreen Sayed<br>
            Fr. Conceicao Rodrigues College of Engineering, Bandra (W), Mumbai<br>
            Department of Computer Science & Engineering
        </div>
    </div>
</div>

<!-- SLIDE 2: PROJECT OVERVIEW -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="tagline">DBMS Micro Project</div>
            <h2>Project Overview</h2>
        </div>
        <div class="num-badge">2</div>
    </div>
    <div class="slide-body">
        <div class="card">
            <h3>Automating Library Workflows</h3>
            <ul>
                <li><strong>Purpose:</strong> Comprehensive database solution eliminating manual ledger and spreadsheet record-keeping.</li>
                <li><strong>Catalog Management:</strong> Organizes physical book titles across academic genres with multi-author mapping.</li>
                <li><strong>Member Borrowing Quotas:</strong> Enforces borrowing quotas (Student: 3 books, Faculty: 8 books).</li>
                <li><strong>Automated Stock Updates:</strong> Decrements stock on checkout and restores stock on return via triggers.</li>
                <li><strong>Automated Late Fines:</strong> Date-difference trigger computes ₹5.00/day penalties automatically upon return.</li>
                <li><strong>Dual Interfaces:</strong> Python Tkinter Desktop GUI and Bootstrap 5 responsive Web Portal.</li>
            </ul>
        </div>
        <div class="img-card">
            <img src="{dash_img}" alt="Dashboard">
            <div class="img-caption">Real-Time Web Dashboard with Live Database Statistics</div>
        </div>
    </div>
</div>

<!-- SLIDE 3: PROBLEM STATEMENT -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="tagline">DBMS Micro Project</div>
            <h2>Problem Statement & Proposed Solution</h2>
        </div>
        <div class="num-badge">3</div>
    </div>
    <div class="slide-body">
        <div class="card card-danger">
            <h3>Traditional Record Challenges</h3>
            <ul>
                <li><strong>Data Redundancy:</strong> Author names and book details repeatedly transcribed across paper ledgers.</li>
                <li><strong>Update Anomalies:</strong> Changing an author's name causes widespread inconsistencies across records.</li>
                <li><strong>Deletion Anomalies:</strong> Deleting a loan history inadvertently deletes the borrower or book record.</li>
                <li><strong>Negative Stock Drift:</strong> Spreadsheets lack constraints, allowing loans when shelf count is zero.</li>
                <li><strong>Manual Fine Calculations:</strong> Human error and bias in calculating overdue days lead to revenue loss.</li>
                <li><strong>No Audit Trail:</strong> Absence of tamper-proof logs for catalog updates and fine payments.</li>
            </ul>
        </div>
        <div class="card card-success">
            <h3>Proposed Relational Solution</h3>
            <ul>
                <li><strong>Centralized Database:</strong> 3NF normalized schema eliminating redundancy across 8 tables.</li>
                <li><strong>Integrity Constraints:</strong> <code>CHECK(available &le; total AND &ge; 0)</code> ensures zero stock corruption.</li>
                <li><strong>Database Triggers:</strong> Autonomous triggers execute stock adjustments and calculate late fines.</li>
                <li><strong>Dynamic Author Creation:</strong> Register new contributing authors directly during book addition.</li>
                <li><strong>Referential Actions:</strong> <code>ON DELETE CASCADE</code> prevents orphaned child transactions.</li>
                <li><strong>Permanent Audit Log:</strong> <code>audit_logs</code> table tracks every mutation with timestamps.</li>
            </ul>
        </div>
    </div>
</div>

<!-- SLIDE 4: OBJECTIVES -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="tagline">DBMS Micro Project</div>
            <h2>Project Objectives</h2>
        </div>
        <div class="num-badge">4</div>
    </div>
    <div class="slide-body" style="flex-direction: column; gap: 14px;">
        <div class="card" style="padding: 16px 24px; flex: none;">
            <h3 style="font-size: 17px; margin-bottom: 6px;">1. 3NF Normalized Relational Database Design</h3>
            <p style="margin: 0; font-size: 15px; color: #475569;">Eliminate insertion, update, and deletion anomalies across 8 dedicated tables with composite junction entities.</p>
        </div>
        <div class="card" style="padding: 16px 24px; flex: none;">
            <h3 style="font-size: 17px; margin-bottom: 6px;">2. Autonomous Event-Driven Database Triggers</h3>
            <p style="margin: 0; font-size: 15px; color: #475569;">Deploy triggers for automatic stock decrementation on issue, stock restoration on return, and ₹5/day overdue fine computation.</p>
        </div>
        <div class="card" style="padding: 16px 24px; flex: none;">
            <h3 style="font-size: 17px; margin-bottom: 6px;">3. Strict Referential & Domain Integrity Constraints</h3>
            <p style="margin: 0; font-size: 15px; color: #475569;">Implement PKs, FKs, domain CHECK constraints, and UNIQUE rules ensuring shelf stock can never fall below zero.</p>
        </div>
        <div class="card" style="padding: 16px 24px; flex: none;">
            <h3 style="font-size: 17px; margin-bottom: 6px;">4. Multi-Author Attribution & On-The-Fly Author Creation</h3>
            <p style="margin: 0; font-size: 15px; color: #475569;">Resolve Many-to-Many book-author relationships with dynamic author registration from the Add Book interface.</p>
        </div>
        <div class="card" style="padding: 16px 24px; flex: none;">
            <h3 style="font-size: 17px; margin-bottom: 6px;">5. Dual User Interface Deployment</h3>
            <p style="margin: 0; font-size: 15px; color: #475569;">Provide accessible frontends (Desktop Tkinter GUI and Bootstrap 5 REST Client) for catalog browsing and SQL analytics.</p>
        </div>
    </div>
</div>

<!-- SLIDE 5: SCOPE OF THE PROJECT -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="tagline">DBMS Micro Project</div>
            <h2>Scope of the Project</h2>
        </div>
        <div class="num-badge">5</div>
    </div>
    <div class="slide-body">
        <div class="card">
            <h3>Book & Author Catalog</h3>
            <ul>
                <li>Full CRUD on books and genre classifications</li>
                <li>Dynamic on-the-fly author creation</li>
                <li>ISBN format and uniqueness validation</li>
                <li>Real-time shelf availability tracking</li>
            </ul>
        </div>
        <div class="card">
            <h3>Member Registry</h3>
            <ul>
                <li>Student tier (3 books quota)</li>
                <li>Faculty tier (8 books quota)</li>
                <li>Email uniqueness enforcement</li>
                <li>Real-time active loans counter</li>
            </ul>
        </div>
        <div class="card">
            <h3>Circulation & Fines</h3>
            <ul>
                <li>Controlled checkout with quota validation</li>
                <li>Return date auto-stamping</li>
                <li>Trigger-based fine assessment (₹5/day)</li>
                <li>Fine clearance receipt processing</li>
            </ul>
        </div>
        <div class="card">
            <h3>Audit & Boundaries</h3>
            <ul>
                <li>Tamper-evident audit logging</li>
                <li>Pre-compiled analytical views</li>
                <li><em>Outside scope:</em> Online payment gateways</li>
                <li><em>Outside scope:</em> RFID barcode scanners</li>
            </ul>
        </div>
    </div>
</div>

<!-- SLIDE 6: ARCHITECTURE -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="tagline">DBMS Micro Project</div>
            <h2>Proposed System Architecture (3-Tier)</h2>
        </div>
        <div class="num-badge">6</div>
    </div>
    <div class="slide-body">
        <div class="img-card" style="flex: 2;">
            <img src="{arch_img}" alt="Architecture Diagram">
            <div class="img-caption">Connected 3-Tier Layered Architecture</div>
        </div>
        <div class="card" style="flex: 1;">
            <h3>Layered Highlights</h3>
            <ul>
                <li><strong>Tier 1: Presentation</strong><br>Tkinter Desktop GUI + HTML5 Bootstrap 5 Web Client.</li>
                <li><strong>Tier 2: Business Logic</strong><br>Python REST API controller enforcing quota checks and input validation.</li>
                <li><strong>Tier 3: Relational Engine</strong><br>SQLite 3 / MySQL 8.0 enforcing foreign keys and triggers.</li>
                <li><strong>ACID Guarantees</strong><br>Atomic checkout and return transaction management.</li>
            </ul>
        </div>
    </div>
</div>

<!-- SLIDE 7: ER MODEL -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="tagline">DBMS Micro Project</div>
            <h2>Database Design: Entity-Relationship Model</h2>
        </div>
        <div class="num-badge">7</div>
    </div>
    <div class="slide-body">
        <div class="img-card" style="flex: 2;">
            <img src="{er_img}" alt="ER Diagram">
            <div class="img-caption">3NF Normalized Entity-Relationship Diagram</div>
        </div>
        <div class="card" style="flex: 1;">
            <h3>Entity Relationships</h3>
            <ul>
                <li><strong>Categories (1) &mdash; (N) Books:</strong> One category classifies multiple titles.</li>
                <li><strong>Books (M) &mdash; (N) Authors:</strong> Resolved via <code>book_authors</code> junction entity.</li>
                <li><strong>Members (1) &mdash; (N) Transactions:</strong> Patrons borrow multiple books.</li>
                <li><strong>Books (1) &mdash; (N) Transactions:</strong> Books are loaned across transactions.</li>
                <li><strong>Transactions (1) &mdash; (0..1) Fines:</strong> Late returns incur fine records.</li>
            </ul>
        </div>
    </div>
</div>

<!-- SLIDE 8: SCHEMA & KEYS -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="tagline">DBMS Micro Project</div>
            <h2>Relational Schema & Key Constraints</h2>
        </div>
        <div class="num-badge">8</div>
    </div>
    <div class="slide-body" style="padding: 20px 48px;">
        <div class="card" style="padding: 16px;">
            <table class="slide-table">
                <thead>
                    <tr>
                        <th>Table Name</th>
                        <th>Primary Key (PK)</th>
                        <th>Foreign Key(s) (FK)</th>
                        <th>Constraints & Rules</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><code>categories</code></td><td><code>category_id</code></td><td>None</td><td><code>category_name UNIQUE</code></td></tr>
                    <tr><td><code>authors</code></td><td><code>author_id</code></td><td>None</td><td><code>author_name NOT NULL</code></td></tr>
                    <tr><td><code>books</code></td><td><code>book_id</code></td><td><code>category_id</code></td><td><code>isbn UNIQUE</code>, <code>CHECK(available &le; total)</code></td></tr>
                    <tr><td><code>book_authors</code></td><td><code>(book_id, author_id)</code></td><td><code>book_id, author_id</code></td><td><code>ON DELETE CASCADE</code> (Composite PK)</td></tr>
                    <tr><td><code>members</code></td><td><code>member_id</code></td><td>None</td><td><code>email UNIQUE</code>, <code>CHECK(max_books &gt; 0)</code></td></tr>
                    <tr><td><code>borrow_transactions</code></td><td><code>transaction_id</code></td><td><code>book_id, member_id</code></td><td><code>ON DELETE CASCADE</code></td></tr>
                    <tr><td><code>fines</code></td><td><code>fine_id</code></td><td><code>transaction_id, member_id</code></td><td><code>transaction_id UNIQUE</code>, <code>fine_amount &ge; 0</code></td></tr>
                    <tr><td><code>audit_logs</code></td><td><code>log_id</code></td><td>None</td><td>Automated timestamp tracking</td></tr>
                </tbody>
            </table>
        </div>
    </div>
</div>

<!-- SLIDE 9: SQL IMPLEMENTATION -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="tagline">DBMS Micro Project</div>
            <h2>SQL Implementation Matrix</h2>
        </div>
        <div class="num-badge">9</div>
    </div>
    <div class="slide-body">
        <div class="card">
            <h3>DDL & Constraints</h3>
            <ul>
                <li><code>CREATE TABLE</code> with autoincrement</li>
                <li><code>PRIMARY KEY</code> & <code>FOREIGN KEY</code></li>
                <li><code>UNIQUE (isbn, email)</code></li>
                <li><code>CHECK (available_copies &ge; 0)</code></li>
                <li><code>ON DELETE CASCADE</code></li>
            </ul>
        </div>
        <div class="card">
            <h3>DML & Transactions</h3>
            <ul>
                <li>Parameterized <code>INSERT INTO</code></li>
                <li>Conditional <code>UPDATE</code> return date</li>
                <li>Cascaded <code>DELETE</code> safe execution</li>
                <li><code>BEGIN TRANSACTION</code></li>
                <li><code>COMMIT</code> & <code>ROLLBACK</code></li>
            </ul>
        </div>
        <div class="card">
            <h3>DQL & Joins</h3>
            <ul>
                <li><code>INNER JOIN</code> & <code>LEFT JOIN</code></li>
                <li><code>GROUP_CONCAT(authors)</code></li>
                <li><code>WHERE</code>, <code>LIKE</code>, <code>BETWEEN</code></li>
                <li><code>ORDER BY</code> & <code>LIMIT</code></li>
                <li>Correlated Subqueries</li>
            </ul>
        </div>
        <div class="card">
            <h3>Triggers & Views</h3>
            <ul>
                <li>Auto stock decrement on loan</li>
                <li>Auto stock restore on return</li>
                <li>Auto fine calculation (₹5/day)</li>
                <li><code>vw_book_catalog</code></li>
                <li><code>vw_active_loans</code></li>
            </ul>
        </div>
    </div>
</div>

<!-- SLIDE 10: SQL QUERIES -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="tagline">DBMS Micro Project</div>
            <h2>SQL Queries & Execution Results</h2>
        </div>
        <div class="num-badge">10</div>
    </div>
    <div class="slide-body">
        <div class="card">
            <h3>Query 1: Multi-Author Catalog Aggregation</h3>
            <p style="font-family: monospace; font-size: 13px; background: #f1f5f9; padding: 8px; border-radius: 4px;">
                SELECT b.book_id, b.title, c.category_name, GROUP_CONCAT(a.author_name, ', ') AS authors, b.available_copies<br>
                FROM books b<br>
                LEFT JOIN categories c ON b.category_id = c.category_id<br>
                LEFT JOIN book_authors ba ON b.book_id = ba.book_id<br>
                LEFT JOIN authors a ON ba.author_id = a.author_id<br>
                GROUP BY b.book_id;
            </p>
            <ul>
                <li>Resolves Many-to-Many junction entity.</li>
                <li>Aggregates authors into single comma-delimited string.</li>
            </ul>
        </div>
        <div class="card">
            <h3>Query 2: Active Loans with Overdue Counter</h3>
            <p style="font-family: monospace; font-size: 13px; background: #f1f5f9; padding: 8px; border-radius: 4px;">
                SELECT t.transaction_id, b.title, (m.first_name || ' ' || m.last_name) AS member_name, t.due_date,<br>
                CASE WHEN DATE('now') > t.due_date THEN CAST(JULIANDAY(DATE('now')) - JULIANDAY(t.due_date) AS INT) ELSE 0 END AS days_overdue<br>
                FROM borrow_transactions t<br>
                JOIN books b ON t.book_id = b.book_id<br>
                JOIN members m ON t.member_id = m.member_id<br>
                WHERE t.return_date IS NULL;
            </p>
            <ul>
                <li>Calculates days past due using Julian date math.</li>
                <li>Instantly surfaces overdue patrons.</li>
            </ul>
        </div>
    </div>
</div>

<!-- SLIDE 11: ADVANCED ANALYTICS -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="tagline">DBMS Micro Project</div>
            <h2>Advanced Queries & Aggregate Analytics</h2>
        </div>
        <div class="num-badge">11</div>
    </div>
    <div class="slide-body">
        <div class="card">
            <h3>Query 3: Category Inventory Aggregates</h3>
            <p style="font-family: monospace; font-size: 13px; background: #f1f5f9; padding: 8px; border-radius: 4px;">
                SELECT c.category_name, COUNT(b.book_id) AS titles, SUM(b.total_copies) AS volumes, SUM(b.available_copies) AS shelf<br>
                FROM categories c<br>
                JOIN books b ON c.category_id = b.category_id<br>
                GROUP BY c.category_id<br>
                HAVING SUM(b.total_copies) >= 5<br>
                ORDER BY volumes DESC;
            </p>
            <ul>
                <li>Demonstrates <code>COUNT</code>, <code>SUM</code>, <code>GROUP BY</code>, and <code>HAVING</code>.</li>
                <li>Results: Computer Science (26 vol), Software Eng (14 vol), Electronics (8 vol).</li>
            </ul>
        </div>
        <div class="card">
            <h3>Query 4: Outstanding Unpaid Fines</h3>
            <p style="font-family: monospace; font-size: 13px; background: #f1f5f9; padding: 8px; border-radius: 4px;">
                SELECT f.fine_id, (m.first_name || ' ' || m.last_name) AS member, m.phone, b.title, f.fine_amount<br>
                FROM fines f<br>
                JOIN members m ON f.member_id = m.member_id<br>
                JOIN borrow_transactions t ON f.transaction_id = t.transaction_id<br>
                JOIN books b ON t.book_id = b.book_id<br>
                WHERE f.paid_status = 'Unpaid';
            </p>
            <ul>
                <li>4-table relational join generating dues recovery list.</li>
                <li>Enables administrative collection.</li>
            </ul>
        </div>
    </div>
</div>

<!-- SLIDE 12: APPLICATION INTERFACE & NEW AUTHOR FEATURE -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="tagline">DBMS Micro Project</div>
            <h2>Application Interface & Dynamic Author Creation</h2>
        </div>
        <div class="num-badge">12</div>
    </div>
    <div class="slide-body">
        <div class="img-card">
            <img src="{cat_img}" alt="Catalog">
            <div class="img-caption">Book Catalog Interface with Search & Filters</div>
        </div>
        <div class="img-card">
            <img src="{modal_img}" alt="Add Author Feature">
            <div class="img-caption">New Feature: Dynamic "➕ Add New Author" within Add Book Modal</div>
        </div>
    </div>
</div>

<!-- SLIDE 13: DATABASE REPORTS -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="tagline">DBMS Micro Project</div>
            <h2>Circulation Desk & Dues Settlement</h2>
        </div>
        <div class="num-badge">13</div>
    </div>
    <div class="slide-body">
        <div class="img-card">
            <img src="{loans_img}" alt="Active Loans">
            <div class="img-caption">Circulation Desk: Active Loans & One-Click Return Processing</div>
        </div>
        <div class="img-card">
            <img src="{fines_img}" alt="Fines Tracker">
            <div class="img-caption">Fines Tracker: Overdue Penalties & Administrative Clearance</div>
        </div>
    </div>
</div>

<!-- SLIDE 14: OUTCOMES & CONCLUSION -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="tagline">DBMS Micro Project</div>
            <h2>Expected Outcome & Conclusion</h2>
        </div>
        <div class="num-badge">14</div>
    </div>
    <div class="slide-body">
        <div class="card card-success">
            <h3>Key System Outcomes</h3>
            <ul>
                <li><strong>Centralized & Persistent Data:</strong> 3NF schema eliminates duplication across catalog, members, and transactions.</li>
                <li><strong>Automated Business Logic:</strong> Event triggers handle stock adjustments and fine calculation without manual intervention.</li>
                <li><strong>Zero Stock Anomalies:</strong> Database constraints prevent negative inventory.</li>
                <li><strong>Seamless Author Addition:</strong> Dynamic author creation directly in the book entry dialog.</li>
                <li><strong>Tamper-Proof Audit Logging:</strong> Every insert, update, and return is permanently recorded.</li>
            </ul>
        </div>
        <div class="card">
            <h3>Conclusion & DBMS Concepts Proven</h3>
            <ul>
                <li>Demonstrates real-world application of relational database engineering.</li>
                <li>Implemented Normalization (1NF to 3NF), Referential Keys, Triggers, Views, and Transactions.</li>
                <li>Proved that a clean relational core supports both Desktop (Tkinter) and Web (REST) interfaces seamlessly.</li>
            </ul>
        </div>
    </div>
</div>

<!-- SLIDE 15: REFERENCES & THANK YOU -->
<div class="slide title-slide" style="align-items: center; text-align: center;">
    <h1 style="font-size: 52px; font-weight: 800; color: #ffffff; margin-bottom: 8px;">Thank You!</h1>
    <p style="font-size: 22px; color: #94a3b8; margin-top: 0; margin-bottom: 32px;">Questions & Viva Discussion Welcome</p>

    <div style="background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 24px 36px; text-align: left; max-width: 800px; width: 100%;">
        <div style="font-size: 15px; font-weight: 700; color: #60a5fa; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 12px;">
            Academic & Technical References
        </div>
        <ul style="color: #cbd5e1; font-size: 15px; line-height: 1.8; margin: 0; padding-left: 20px;">
            <li>R. Elmasri & S. B. Navathe, <em>Fundamentals of Database Systems</em>, 7th ed., Pearson, 2017.</li>
            <li>A. Silberschatz, H. F. Korth, & S. Sudarshan, <em>Database System Concepts</em>, 7th ed., McGraw-Hill, 2019.</li>
            <li>SQLite 3 Documentation &mdash; <a href="https://www.sqlite.org/docs.html" style="color: #60a5fa;">https://www.sqlite.org/docs.html</a></li>
            <li>MySQL 8.0 Reference Manual &mdash; <a href="https://dev.mysql.com/doc/refman/8.0/en/" style="color: #60a5fa;">https://dev.mysql.com/doc/refman/8.0/en/</a></li>
            <li>Python Software Foundation (sqlite3 DB-API) &mdash; <a href="https://docs.python.org/3/library/sqlite3.html" style="color: #60a5fa;">https://docs.python.org/3/library/sqlite3.html</a></li>
        </ul>
    </div>
</div>

<!-- BROWSER NAVIGATION BAR -->
<div id="nav-bar">
    <button onclick="window.print()">🖨️ Print to PDF</button>
    <button onclick="document.documentElement.requestFullscreen()">⛶ Fullscreen</button>
</div>

</body>
</html>
"""

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[*] HTML presentation generated: {HTML_PATH}")

    # Generate PDF slide deck
    file_url = "file:///" + os.path.abspath(HTML_PATH).replace("\\", "/")
    cmd = [
        EDGE_PATH,
        "--headless=new",
        "--disable-gpu",
        f"--print-to-pdf={PDF_PATH}",
        "--no-pdf-header-footer",
        file_url
    ]
    subprocess.run(cmd, check=True)
    time.sleep(1)

    if os.path.exists(PDF_PATH):
        print(f"[+] Successfully generated PDF Presentation: {PDF_PATH} ({os.path.getsize(PDF_PATH)} bytes)")
    else:
        raise RuntimeError("Failed to generate PDF presentation")


if __name__ == "__main__":
    generate_presentation_deck()
