"""
Generate Library_Management_System_Presentation.pptx (16:9 Widescreen)
Using python-pptx with 15 professional slides matching the sample template.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
DIAG_DIR = os.path.join(DOCS_DIR, "diagrams")
PPTX_PATH = os.path.join(DOCS_DIR, "Library_Management_System_Presentation.pptx")

# Color Palette
NAVY = RGBColor(15, 23, 42)        # #0f172a
BLUE = RGBColor(37, 99, 235)       # #2563eb
LIGHT_BG = RGBColor(248, 250, 252) # #f8fafc
WHITE = RGBColor(255, 255, 255)
DARK_TEXT = RGBColor(30, 41, 59)   # #1e293b
MUTED_TEXT = RGBColor(100, 116, 139) # #64748b
ACCENT_GREEN = RGBColor(16, 185, 129) # #10b981
CARD_BG = RGBColor(241, 245, 249)  # #f1f5f9
BORDER_COLOR = RGBColor(203, 213, 225) # #cbd5e1


def set_slide_background(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_header(slide, title_text, slide_number, category_text="DATABASE MANAGEMENT SYSTEMS  |  MICRO PROJECT"):
    # Header bar
    header_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
    header_box.fill.solid()
    header_box.fill.fore_color.rgb = NAVY
    header_box.line.color.rgb = NAVY

    # Category Text
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.8)
    tf.margin_top = Inches(0.18)
    p0 = tf.paragraphs[0]
    p0.text = category_text.upper()
    p0.font.name = "Segoe UI"
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(148, 163, 184)

    # Title Text
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(20)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    # Slide Number pill on right
    num_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(12.2), Inches(0.28), Inches(0.6), Inches(0.45))
    num_box.fill.solid()
    num_box.fill.fore_color.rgb = BLUE
    num_box.line.color.rgb = BLUE
    ntf = num_box.text_frame
    np = ntf.paragraphs[0]
    np.text = str(slide_number)
    np.font.name = "Segoe UI"
    np.font.size = Pt(13)
    np.font.bold = True
    np.font.color.rgb = WHITE
    np.alignment = PP_ALIGN.CENTER


def add_card(slide, left, top, width, height, title, body_bullets, header_color=BLUE):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = BORDER_COLOR
    card.line.width = Pt(1)

    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.2)

    if title:
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Segoe UI"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = header_color
        p.space_after = Pt(8)

    for i, bullet in enumerate(body_bullets):
        p = tf.add_paragraph()
        p.text = f"•  {bullet}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(6)


def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ==========================================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, NAVY)

    # Decorative accent bar
    accent = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(0.12), Inches(4.8))
    accent.fill.solid()
    accent.fill.fore_color.rgb = BLUE
    accent.line.fill.background()

    # Main Title text frame
    title_box = s1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(11.0), Inches(4.8))
    tf1 = title_box.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "DATABASE MANAGEMENT SYSTEMS  |  MICRO PROJECT"
    p0.font.name = "Segoe UI"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(96, 165, 250)
    p0.space_after = Pt(14)

    p1 = tf1.add_paragraph()
    p1.text = "Library Management System"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_after = Pt(8)

    p2 = tf1.add_paragraph()
    p2.text = "Python (Tkinter & Web REST)  •  SQLite 3 / MySQL 8.0  •  3NF Relational Architecture"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(15)
    p2.font.color.rgb = RGBColor(226, 232, 240)
    p2.space_after = Pt(28)

    p3 = tf1.add_paragraph()
    p3.text = "Presented by:"
    p3.font.name = "Segoe UI"
    p3.font.size = Pt(12)
    p3.font.bold = True
    p3.font.color.rgb = RGBColor(148, 163, 184)
    p3.space_after = Pt(4)

    p4 = tf1.add_paragraph()
    p4.text = "Atharva Doke (11388)   •   Aditya Chitimilla (11385)   •   Alroy Fernandes (11393)"
    p4.font.name = "Segoe UI"
    p4.font.size = Pt(14)
    p4.font.bold = True
    p4.font.color.rgb = WHITE
    p4.space_after = Pt(20)

    p5 = tf1.add_paragraph()
    p5.text = "Class: S.E. CSE   |   Academic Year 2026–27   |   Guide: Prof. Afreen Sayed\nFr. Conceicao Rodrigues College of Engineering, Bandra (W), Mumbai"
    p5.font.name = "Segoe UI"
    p5.font.size = Pt(12)
    p5.font.color.rgb = RGBColor(148, 163, 184)

    # ==========================================================
    # SLIDE 2: PROJECT OVERVIEW
    # ==========================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, LIGHT_BG)
    add_header(s2, "Project Overview", 2)

    # Left content box
    add_card(
        s2, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3),
        "Automating Library Operations with Relational Integrity",
        [
            "A comprehensive database application engineered to eliminate manual registers and spreadsheet errors.",
            "Centralizes cataloging across titles, genres, and multi-author attributions.",
            "Enforces patron borrowing limits (Student: 3, Faculty: 8) with real-time checkout validation.",
            "Automates stock decrementation on issue and restoration on return via database triggers.",
            "Computes late fines automatically at ₹5.00/day using date-difference trigger mechanics.",
            "Features dual interfaces: Desktop GUI (Tkinter) and Responsive Web App (HTML5/Bootstrap 5)."
        ]
    )

    # Right side image: Dashboard Screenshot
    dash_img = os.path.join(DIAG_DIR, "screenshot_dashboard.png")
    if os.path.exists(dash_img):
        s2.shapes.add_picture(dash_img, Inches(6.7), Inches(1.5), width=Inches(5.8))

    # ==========================================================
    # SLIDE 3: PROBLEM STATEMENT & PROPOSED SOLUTION
    # ==========================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, LIGHT_BG)
    add_header(s3, "Problem Statement & Proposed Solution", 3)

    add_card(
        s3, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3),
        "Traditional Library Record Challenges",
        [
            "Data Redundancy: Titles and author names duplicated across multiple checkout sheets.",
            "Update Anomalies: Editing author or category names leads to widespread discrepancies.",
            "Deletion Anomalies: Deleting past checkout records risks erasing book or member profiles.",
            "Stock Inconsistencies: No database-level constraints allow negative copy counts.",
            "Manual Overdue Calculations: Human fine calculation is prone to bias and revenue leakage.",
            "No Audit Trail: Lack of tamper-proof logging for catalog changes and fine receipts."
        ],
        header_color=RGBColor(220, 38, 38)
    )

    add_card(
        s3, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3),
        "Proposed Relational DBMS Solution",
        [
            "Centralized Relational Store: 3NF normalized schema eliminating redundancy across 8 tables.",
            "Domain Constraints: CHECK constraints ensure available_copies <= total_copies and >= 0.",
            "Automated Event Triggers: Database triggers calculate fines and sync stock instantly.",
            "Dynamic Author Creation: Register new authors on-the-fly during new book addition.",
            "Referential Integrity: Cascading deletes prevent orphaned child records.",
            "Transparent Auditing: Automatic event logging records every system modification."
        ],
        header_color=ACCENT_GREEN
    )

    # ==========================================================
    # SLIDE 4: PROJECT OBJECTIVES
    # ==========================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, LIGHT_BG)
    add_header(s4, "Project Objectives", 4)

    objectives = [
        ("1. 3NF Normalized Relational Design", "Eliminate insertion, update, and deletion anomalies across 8 dedicated tables with composite junction entities."),
        ("2. Active Database Triggers", "Deploy autonomous triggers for automatic stock decrementation, inventory restoration, and ₹5/day fine computation."),
        ("3. Strict Referential & Domain Integrity", "Implement PKs, FKs, CHECK constraints, and UNIQUE rules ensuring physical volumes never fall below zero."),
        ("4. Seamless Multi-Author Attribution", "Handle Many-to-Many book-author relationships with on-the-fly author creation from the Add Book modal."),
        ("5. Dual User Interface Deployment", "Provide accessible frontends (Desktop Tkinter GUI & Web Bootstrap REST Client) with real-time analytics.")
    ]

    for i, (title, desc) in enumerate(objectives):
        top_y = Inches(1.4 + i * 1.1)
        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_y, Inches(11.7), Inches(0.95))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = BORDER_COLOR
        card.line.width = Pt(1)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.3)
        tf.margin_top = Inches(0.12)
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = "Segoe UI"
        p0.font.size = Pt(12)
        p0.font.bold = True
        p0.font.color.rgb = BLUE
        p0.space_after = Pt(2)

        p1 = tf.add_paragraph()
        p1.text = desc
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(10)
        p1.font.color.rgb = DARK_TEXT

    # ==========================================================
    # SLIDE 5: SCOPE OF THE PROJECT
    # ==========================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, LIGHT_BG)
    add_header(s5, "Scope of the Project", 5)

    modules = [
        ("Book Catalog & Authors", ["Full CRUD on books & genres", "Dynamic author registration", "ISBN uniqueness validation", "Real-time shelf status"]),
        ("Patron Membership", ["Student tier (3 books quota)", "Faculty tier (8 books quota)", "Email & phone uniqueness", "Active loan quota tracking"]),
        ("Circulation & Fines", ["Issue with availability check", "Return date auto-stamping", "Trigger-based fine calculation", "Fine settlement tracking"]),
        ("Audit & Outside Scope", ["Tamper-evident audit trail", "Pre-compiled analytical views", "Outside: Payment gateways", "Outside: RFID / Courier"])
    ]

    for i, (mod_title, mod_bullets) in enumerate(modules):
        left_x = Inches(0.8 + i * 2.95)
        add_card(s5, left_x, Inches(1.5), Inches(2.8), Inches(5.3), mod_title, mod_bullets)

    # ==========================================================
    # SLIDE 6: PROPOSED SYSTEM ARCHITECTURE
    # ==========================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, LIGHT_BG)
    add_header(s6, "Proposed System Architecture (3-Tier)", 6)

    arch_img = os.path.join(DIAG_DIR, "architecture_diagram.png")
    if os.path.exists(arch_img):
        s6.shapes.add_picture(arch_img, Inches(0.8), Inches(1.5), width=Inches(8.0))

    add_card(
        s6, Inches(9.1), Inches(1.5), Inches(3.4), Inches(5.3),
        "Architectural Highlights",
        [
            "Tier 1: Dual Frontends (Python Tkinter & Web Bootstrap 5).",
            "Tier 2: Application Controller enforcing quota validation and parameter safety.",
            "Tier 3: Relational DBMS Engine (SQLite 3 / MySQL 8.0).",
            "ACID Compliance ensures atomic borrow and return transactions.",
            "Pre-compiled database views optimize analytical queries."
        ]
    )

    # ==========================================================
    # SLIDE 7: DATABASE DESIGN: ER MODEL
    # ==========================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, LIGHT_BG)
    add_header(s7, "Database Design: Entity-Relationship Model", 7)

    er_img = os.path.join(DIAG_DIR, "er_diagram.png")
    if os.path.exists(er_img):
        s7.shapes.add_picture(er_img, Inches(0.8), Inches(1.4), width=Inches(8.4))

    add_card(
        s7, Inches(9.4), Inches(1.4), Inches(3.1), Inches(5.4),
        "Core Entities & Mappings",
        [
            "Categories 1 : N Books (Genre classification).",
            "Books N : M Authors resolved via Book_Authors junction entity.",
            "Members 1 : N Borrow_Transactions (Quota-governed loans).",
            "Books 1 : N Borrow_Transactions.",
            "Borrow_Transactions 1 : 0..1 Fines (Optional late fee penalty).",
            "Audit_Logs tracks all system mutations."
        ]
    )

    # ==========================================================
    # SLIDE 8: RELATIONAL SCHEMA & KEYS
    # ==========================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, LIGHT_BG)
    add_header(s8, "Relational Schema & Key Constraints", 8)

    # Table layout
    rows = 9
    cols = 4
    table_shape = s8.shapes.add_table(rows, cols, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.2))
    table = table_shape.table
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(2.4)
    table.columns[2].width = Inches(3.2)
    table.columns[3].width = Inches(3.9)

    headers = ["Table Name", "Primary Key (PK)", "Foreign Key(s) (FK)", "Key Constraints & Domain Rules"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE

    schema_data = [
        ("categories", "category_id", "None", "category_name UNIQUE, NOT NULL"),
        ("authors", "author_id", "None", "author_name NOT NULL"),
        ("books", "book_id", "category_id -> categories", "isbn UNIQUE, CHECK(available <= total)"),
        ("book_authors", "(book_id, author_id)", "book_id, author_id", "Composite PK, ON DELETE CASCADE (M:N)"),
        ("members", "member_id", "None", "email UNIQUE, CHECK(max_books > 0)"),
        ("borrow_transactions", "transaction_id", "book_id, member_id", "ON DELETE CASCADE, status DEFAULT 'Issued'"),
        ("fines", "fine_id", "transaction_id, member_id", "transaction_id UNIQUE, fine_amount >= 0"),
        ("audit_logs", "log_id", "None", "Timestamped system audit trail")
    ]

    for i, row in enumerate(schema_data):
        for j, val in enumerate(row):
            cell = table.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if i % 2 == 0 else CARD_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Segoe UI"
            p.font.size = Pt(9.5)
            p.font.color.rgb = DARK_TEXT

    # ==========================================================
    # SLIDE 9: SQL IMPLEMENTATION
    # ==========================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, LIGHT_BG)
    add_header(s9, "SQL Concepts & Implementation Matrix", 9)

    sql_pillars = [
        ("DDL & Integrity", ["CREATE TABLE, ALTER, DROP", "PRIMARY & FOREIGN KEY", "CHECK (copies >= 0)", "UNIQUE (isbn, email)"]),
        ("DML & Transactions", ["INSERT INTO book_authors", "UPDATE return_date", "DELETE with CASCADE", "BEGIN, COMMIT, ROLLBACK"]),
        ("DQL & Joins", ["INNER JOIN & LEFT JOIN", "GROUP_CONCAT authors", "WHERE, LIKE, BETWEEN", "ORDER BY & LIMIT"]),
        ("Triggers & Views", ["Stock dec on issue", "Stock inc on return", "Overdue fine ₹5/day", "Pre-compiled analytics"])
    ]

    for i, (title, bullets) in enumerate(sql_pillars):
        left_x = Inches(0.8 + i * 2.95)
        add_card(s9, left_x, Inches(1.5), Inches(2.8), Inches(5.3), title, bullets)

    # ==========================================================
    # SLIDE 10: SQL QUERIES & DATABASE RESULTS
    # ==========================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, LIGHT_BG)
    add_header(s10, "SQL Queries & Database Execution Results", 10)

    # Query 1 Card
    add_card(
        s10, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3),
        "Query 1: Catalog with Grouped Authors",
        [
            "SQL: SELECT b.book_id, b.isbn, b.title, c.category_name, GROUP_CONCAT(a.author_name) AS authors FROM books b LEFT JOIN book_authors ba ON b.book_id=ba.book_id LEFT JOIN authors a ON ba.author_id=a.author_id GROUP BY b.book_id;",
            "Demonstrates: Many-to-Many junction join, string aggregation, and categorization.",
            "Output: Cleanly lists titles with multi-author strings (e.g. 'Kernighan, Ritchie')."
        ]
    )

    # Query 2 Card
    add_card(
        s10, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3),
        "Query 2: Active Loans with Overdue Counter",
        [
            "SQL: SELECT t.transaction_id, b.title, (m.first_name || ' ' || m.last_name) AS member_name, t.due_date, CASE WHEN DATE('now') > t.due_date THEN CAST(JULIANDAY(DATE('now')) - JULIANDAY(t.due_date) AS INT) ELSE 0 END AS days_overdue FROM borrow_transactions t JOIN books b ON t.book_id = b.book_id JOIN members m ON t.member_id = m.member_id WHERE t.return_date IS NULL;",
            "Demonstrates: Conditional CASE logic, Julian date arithmetic, multi-table inner joins.",
            "Output: Instantly identifies overdue borrowers (e.g. 33 days overdue)."
        ]
    )

    # ==========================================================
    # SLIDE 11: QUERY OUTPUT EXAMPLES & AGGREGATE ANALYTICS
    # ==========================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, LIGHT_BG)
    add_header(s11, "Advanced SQL Queries & Aggregate Analytics", 11)

    add_card(
        s11, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3),
        "Query 3: Category Inventory Distribution",
        [
            "SQL: SELECT c.category_name, COUNT(b.book_id) AS titles, SUM(b.total_copies) AS volumes, SUM(b.available_copies) AS shelf FROM categories c JOIN books b ON c.category_id = b.category_id GROUP BY c.category_id HAVING SUM(b.total_copies) >= 5 ORDER BY volumes DESC;",
            "Demonstrates: Multiple aggregate functions (COUNT, SUM), GROUP BY, and HAVING filtering.",
            "Output: CS: 26 volumes (24 shelf); SE: 14 volumes (13 shelf); Math: 7 volumes."
        ]
    )

    add_card(
        s11, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3),
        "Query 4: Outstanding Unpaid Fines",
        [
            "SQL: SELECT f.fine_id, (m.first_name || ' ' || m.last_name) AS member, m.phone, b.title, f.fine_amount FROM fines f JOIN members m ON f.member_id = m.member_id JOIN borrow_transactions t ON f.transaction_id = t.transaction_id JOIN books b ON t.book_id = b.book_id WHERE f.paid_status = 'Unpaid';",
            "Demonstrates: Four-table JOIN, currency formatting, status filtering.",
            "Output: Accurately produces recovery list for administrative follow-up."
        ]
    )

    # ==========================================================
    # SLIDE 12: APPLICATION INTERFACE & NEW AUTHOR FEATURE
    # ==========================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, LIGHT_BG)
    add_header(s12, "Application Interface & Dynamic Author Creation", 12)

    cat_img = os.path.join(DIAG_DIR, "screenshot_catalog.png")
    modal_img = os.path.join(DIAG_DIR, "screenshot_add_book_modal.png")

    if os.path.exists(cat_img):
        s12.shapes.add_picture(cat_img, Inches(0.8), Inches(1.5), width=Inches(5.6))
    if os.path.exists(modal_img):
        s12.shapes.add_picture(modal_img, Inches(6.8), Inches(1.5), width=Inches(5.7))

    # Caption card at bottom
    add_card(
        s12, Inches(0.8), Inches(5.8), Inches(11.7), Inches(1.2),
        "Key Feature: On-The-Fly Author Registration in Add Book Dialog",
        [
            "Librarians can click '➕ Add New Author' directly inside the book entry dialog.",
            "Creates author record, registers audit trail, and auto-selects newly created author seamlessly."
        ]
    )

    # ==========================================================
    # SLIDE 13: DATABASE REPORTS & ANALYTICS
    # ==========================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13, LIGHT_BG)
    add_header(s13, "Circulation Desk, Fines & Audit Reports", 13)

    loans_img = os.path.join(DIAG_DIR, "screenshot_loans.png")
    fines_img = os.path.join(DIAG_DIR, "screenshot_fines.png")

    if os.path.exists(loans_img):
        s13.shapes.add_picture(loans_img, Inches(0.8), Inches(1.5), width=Inches(5.6))
    if os.path.exists(fines_img):
        s13.shapes.add_picture(fines_img, Inches(6.8), Inches(1.5), width=Inches(5.7))

    add_card(
        s13, Inches(0.8), Inches(5.8), Inches(11.7), Inches(1.2),
        "Real-Time Circulation & Fine Settlement Workflows",
        [
            "Instant one-click book returns with automated trigger-driven stock and fine computation.",
            "Transparent fine collection tracking and tamper-evident audit logging for all database events."
        ]
    )

    # ==========================================================
    # SLIDE 14: EXPECTED OUTCOME & CONCLUSION
    # ==========================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14, LIGHT_BG)
    add_header(s14, "Expected Outcome & Conclusion", 14)

    add_card(
        s14, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3),
        "Achieved Project Outcomes",
        [
            "Centralized & Persistent Data: Fully normalized 3NF relational schema.",
            "Eliminated Data Redundancy: Relational separation across books, authors, members, and transactions.",
            "Automated Business Logic: Event triggers handle inventory counts and fine assessments without human error.",
            "Zero Inventory Corruption: Database constraints prevent negative book balances.",
            "Tamper-Proof Audit Logging: Every catalog change and payment is logged with exact timestamps."
        ]
    )

    add_card(
        s14, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3),
        "Conclusion & DBMS Concepts Demonstrated",
        [
            "Combines Python, SQLite, and modern Web technologies to solve real-world library administration challenges.",
            "Demonstrated core DBMS principles: Normalization (1NF to 3NF), Referential Integrity, DDL/DML/DQL mastery.",
            "Proved event-driven automation via SQLite Triggers and Views.",
            "Delivered dual intuitive interfaces ensuring reliable, multi-client access."
        ],
        header_color=ACCENT_GREEN
    )

    # ==========================================================
    # SLIDE 15: REFERENCES & THANK YOU
    # ==========================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15, NAVY)

    # Thank you banner
    ty_box = s15.shapes.add_textbox(Inches(1.5), Inches(1.2), Inches(10.3), Inches(2.2))
    ttf = ty_box.text_frame
    tp0 = ttf.paragraphs[0]
    tp0.text = "Thank You!"
    tp0.font.name = "Segoe UI"
    tp0.font.size = Pt(40)
    tp0.font.bold = True
    tp0.font.color.rgb = WHITE
    tp0.alignment = PP_ALIGN.CENTER

    tp1 = ttf.add_paragraph()
    tp1.text = "Questions & Viva Discussion Welcome"
    tp1.font.name = "Segoe UI"
    tp1.font.size = Pt(18)
    tp1.font.color.rgb = RGBColor(148, 163, 184)
    tp1.alignment = PP_ALIGN.CENTER

    # References Card
    ref_card = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.0), Inches(3.6), Inches(9.3), Inches(3.0))
    ref_card.fill.solid()
    ref_card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    ref_card.line.color.rgb = RGBColor(51, 65, 85)
    rtf = ref_card.text_frame
    rtf.word_wrap = True
    rtf.margin_left = Inches(0.4)
    rtf.margin_top = Inches(0.25)

    rp0 = rtf.paragraphs[0]
    rp0.text = "ACADEMIC & TECHNICAL REFERENCES"
    rp0.font.name = "Segoe UI"
    rp0.font.size = Pt(12)
    rp0.font.bold = True
    rp0.font.color.rgb = RGBColor(96, 165, 250)
    rp0.space_after = Pt(10)

    refs = [
        "R. Elmasri & S. B. Navathe, Fundamentals of Database Systems, 7th ed., Pearson, 2017.",
        "A. Silberschatz, H. F. Korth, & S. Sudarshan, Database System Concepts, 7th ed., McGraw-Hill, 2019.",
        "SQLite 3 Official Documentation (Triggers, Foreign Keys & Constraints) -- https://www.sqlite.org/docs.html",
        "Python Software Foundation, sqlite3 Database API Specification -- https://docs.python.org/3/library/sqlite3.html",
        "MySQL 8.0 Reference Manual (Stored Procedures, Triggers & Views) -- https://dev.mysql.com/doc/refman/8.0/en/"
    ]
    for r in refs:
        p = rtf.add_paragraph()
        p.text = f"•  {r}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10.5)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.space_after = Pt(4)

    # Save presentation
    try:
        prs.save(PPTX_PATH)
        print(f"[+] PPTX successfully generated: {PPTX_PATH} ({os.path.getsize(PPTX_PATH)} bytes)")
    except PermissionError:
        alt_path = os.path.join(BASE_DIR, "Library_Management_System_Presentation_Updated.pptx")
        prs.save(alt_path)
        print(f"[+] Original file in use. Saved updated PPTX to: {alt_path} ({os.path.getsize(alt_path)} bytes)")


if __name__ == "__main__":
    create_presentation()
