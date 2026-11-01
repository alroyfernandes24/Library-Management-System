# 📚 Library Management System - DBMS Mini Project

A complete, production-grade **Database Management System (DBMS) Mini Project** featuring normalized 3NF schema, automated SQL triggers, stored procedures, precomputed views, sample datasets, and **both Web & Desktop UI interfaces**.

---

## 🚀 Quick Start (Zero External Installation Required)

This project is built using Python's standard library (`sqlite3`, `tkinter`, `http.server`). You **do NOT need to run `pip install`**!

### Option 1: Run Modern Web Application (Recommended)
Open your terminal in this project folder and run:
```bash
python app_web.py
```
Then open your web browser and navigate to:
👉 **`http://localhost:5000`**

**Features:**
- 📊 Interactive Dashboard with real-time statistics
- 📖 Book Catalog with search and addition modal
- 👥 Members Directory with borrowing quotas
- 🔄 Book Issue & Return with automated stock decrement/increment
- 💰 Fine tracking with ₹5/day overdue penalty computation
- ⚡ Live SQL Console to test custom queries during Viva / Presentation
- 📝 Trigger-driven Audit Trail

---

### Option 2: Run Desktop GUI (Tkinter)
If you prefer a standalone desktop window:
```bash
python app_gui.py
```

---

## 🗄️ Database Architecture & Files

The project includes ready-to-use scripts for both **SQLite** and **MySQL**:

```
DBMS_Project/
├── database/
│   ├── schema_mysql.sql       # Full MySQL script (DDL, Triggers, Stored Procedures, Views, Sample Data)
│   ├── schema_sqlite.sql      # SQLite script (Executed automatically on first run)
│   └── sample_queries.sql     # 15+ Academic Queries for Lab / Viva (Joins, Subqueries, Aggregations)
│
├── web/
│   └── index.html             # Responsive Bootstrap 5 Web Interface
│
├── app_web.py                 # Lightweight Web Application Server (localhost:5000)
├── app_gui.py                 # Desktop Tkinter GUI Application
├── db_manager.py              # Central database access and business logic layer
├── PROJECT_REPORT.md          # Complete Mini Project Documentation & Viva Q&A Guide
└── README.md                  # Setup & usage instructions
```

---

## 🐬 Using with MySQL Workbench / XAMPP (Optional)

If your college requires you to present inside **MySQL Workbench** or **phpMyAdmin**:
1. Open MySQL Workbench or phpMyAdmin.
2. Open [database/schema_mysql.sql](file:///c:/Users/athar.DESKTOP-SSO72R4/Desktop/DBMS_Project/database/schema_mysql.sql).
3. Execute the entire script. It will create `library_db`, all 8 tables, triggers, stored procedures, views, and insert initial mock records.
4. Open [database/sample_queries.sql](file:///c:/Users/athar.DESKTOP-SSO72R4/Desktop/DBMS_Project/database/sample_queries.sql) to run test queries for your lab record.

---

## 📋 Core DBMS Features Implemented

1. **Third Normal Form (3NF) Compliance:**
   - No multi-valued attributes (handled via `book_authors` junction table).
   - No partial functional dependencies.
   - No transitive dependencies.

2. **Automated Business Logic (Triggers):**
   - `trg_after_issue_book`: Automatically reduces `available_copies` when a book is issued.
   - `trg_after_return_book`: Automatically restores `available_copies` on return.
   - `trg_calculate_fine_on_return`: Automatically computes ₹5/day penalty when return date exceeds due date.
   - `trg_before_issue_check`: Prevents issuing if out-of-stock or if member has reached their quota.

3. **Precomputed Views:**
   - `vw_book_catalog`: Combined book details with concatenated author names.
   - `vw_active_loans`: Currently borrowed books with dynamic overdue day calculation.
   - `vw_outstanding_fines`: Defaulters list with contact details and unpaid amounts.
   - `vw_library_summary`: High-speed aggregated dashboard metrics.

4. **Stored Procedures (MySQL):**
   - `sp_IssueBook`
   - `sp_ReturnBook`
   - `sp_PayFine`

---

## 📖 Project Documentation & Viva Guide
Read [PROJECT_REPORT.md](file:///c:/Users/athar.DESKTOP-SSO72R4/Desktop/DBMS_Project/PROJECT_REPORT.md) for the full mini-project report, ER diagrams, normalization proofs, and the top 15 DBMS viva questions with answers.
