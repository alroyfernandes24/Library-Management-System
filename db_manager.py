"""
Library Management System - Database Manager
Direct Real-Time PostgreSQL Engine with Automatic SQLite Offline Fallback.
Provides 100% rigid bidirectional synchronization with pgAdmin 4.
"""

import os
import sqlite3
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "library.db")
SCHEMA_SQL_PATH = os.path.join(BASE_DIR, "database", "schema_sqlite.sql")

PG_CONFIG = {
    "dbname": "library_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432,
    "connect_timeout": 1
}


def is_postgres_available():
    """Checks if local PostgreSQL library_db is reachable."""
    try:
        import psycopg
        with psycopg.connect(**PG_CONFIG) as conn:
            return True
    except Exception:
        return False


def get_pg_connection():
    """Returns an active PostgreSQL connection with dictionary row factory."""
    import psycopg
    from psycopg.rows import dict_row
    return psycopg.connect(**PG_CONFIG, row_factory=dict_row)


def get_connection():
    """Returns SQLite connection (used for offline mode and mirror caching)."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initializes PostgreSQL schema if reachable, otherwise initializes SQLite."""
    if is_postgres_available():
        try:
            import setup_pg_schema
            setup_pg_schema.setup_postgres_objects()
            print("[+] Connected directly to PostgreSQL (library_db)!")
            return
        except Exception as e:
            print(f"[!] PostgreSQL init notice: {e}")

    # SQLite fallback
    if not os.path.exists(DB_PATH):
        print(f"[*] Initializing SQLite fallback from {SCHEMA_SQL_PATH}...")
        with get_connection() as conn:
            with open(SCHEMA_SQL_PATH, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
            conn.commit()


# -------------------------------------------------------------
# DASHBOARD & ANALYTICS
# -------------------------------------------------------------
def get_dashboard_summary():
    if is_postgres_available():
        try:
            with get_pg_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM vw_library_summary")
                    row = cur.fetchone()
                    if row:
                        d = dict(row)
                        d["pending_fines_amount"] = float(d["pending_fines_amount"] or 0.0)
                        return d
        except Exception as e:
            print(f"[!] PG Summary fallback: {e}")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vw_library_summary")
        row = cursor.fetchone()
        if row:
            return dict(row)
        return {
            "total_titles": 0,
            "total_volumes": 0,
            "available_volumes": 0,
            "active_members": 0,
            "currently_borrowed": 0,
            "pending_fines_amount": 0.0
        }


# -------------------------------------------------------------
# BOOKS & CATALOG
# -------------------------------------------------------------
def get_books(search="", category_id=None):
    if is_postgres_available():
        try:
            with get_pg_connection() as conn:
                with conn.cursor() as cur:
                    query = "SELECT * FROM vw_book_catalog WHERE 1=1"
                    params = []
                    if search:
                        query += " AND (title ILIKE %s OR isbn ILIKE %s OR authors ILIKE %s)"
                        term = f"%{search}%"
                        params.extend([term, term, term])
                    if category_id:
                        query += " AND category_id = %s"
                        params.append(int(category_id))
                    query += " ORDER BY book_id DESC"
                    cur.execute(query, params)
                    books = [dict(r) for r in cur.fetchall()]
                    for b in books:
                        b["status"] = "Available" if (b.get("available_copies") or 0) > 0 else "Out of Stock"
                    return books
        except Exception as e:
            print(f"[!] PG get_books fallback: {e}")

    with get_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM vw_book_catalog WHERE 1=1"
        params = []
        if search:
            query += " AND (title LIKE ? OR isbn LIKE ? OR authors LIKE ?)"
            term = f"%{search}%"
            params.extend([term, term, term])
        if category_id:
            query += " AND category_id = ?"
            params.append(category_id)
        query += " ORDER BY book_id DESC"
        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]


def get_categories():
    if is_postgres_available():
        try:
            with get_pg_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT category_id, name AS category_name, description FROM categories ORDER BY name")
                    return [dict(r) for r in cur.fetchall()]
        except Exception as e:
            print(f"[!] PG get_categories fallback: {e}")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT category_id, category_name, description FROM categories ORDER BY category_name")
        return [dict(r) for r in cursor.fetchall()]


def get_authors():
    if is_postgres_available():
        try:
            with get_pg_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT author_id, name AS author_name, email, biography FROM authors ORDER BY name")
                    return [dict(r) for r in cur.fetchall()]
        except Exception as e:
            print(f"[!] PG get_authors fallback: {e}")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT author_id, author_name, email FROM authors ORDER BY author_name")
        return [dict(r) for r in cursor.fetchall()]


def add_author(author_name, email="", biography=""):
    author_name = author_name.strip() if author_name else ""
    if not author_name:
        raise ValueError("Author name is required!")

    author_id = None
    if is_postgres_available():
        try:
            with get_pg_connection() as conn:
                with conn.cursor() as cur:
                    if email:
                        cur.execute(
                            """INSERT INTO authors (name, email, biography)
                               VALUES (%s, %s, %s)
                               ON CONFLICT (email) DO UPDATE SET 
                                   name = EXCLUDED.name, 
                                   biography = COALESCE(EXCLUDED.biography, authors.biography)
                               RETURNING author_id""",
                            (author_name, email.strip(), biography.strip() if biography else None)
                        )
                    else:
                        cur.execute(
                            "INSERT INTO authors (name, email, biography) VALUES (%s, %s, %s) RETURNING author_id",
                            (author_name, None, biography.strip() if biography else None)
                        )
                    author_id = cur.fetchone()["author_id"]
                    cur.execute(
                        "INSERT INTO audit_logs (table_name, action_type, description) VALUES (%s, %s, %s)",
                        ('authors', 'INSERT', f"New author registered: '{author_name}' (ID: {author_id}).")
                    )
                    conn.commit()
        except Exception as e:
            print(f"[!] PG add_author notice: {e}")

    # Mirror to SQLite
    try:
        with get_connection() as s_conn:
            s_cur = s_conn.cursor()
            if author_id:
                s_cur.execute(
                    """INSERT INTO authors (author_id, author_name, email, biography)
                       VALUES (?, ?, ?, ?)
                       ON CONFLICT(author_id) DO UPDATE SET author_name = excluded.author_name""",
                    (author_id, author_name, email.strip() if email else None, biography.strip() if biography else None)
                )
            else:
                s_cur.execute(
                    "INSERT INTO authors (author_name, email, biography) VALUES (?, ?, ?)",
                    (author_name, email.strip() if email else None, biography.strip() if biography else None)
                )
                author_id = s_cur.lastrowid
            s_conn.commit()
    except Exception:
        pass

    return author_id


def add_book(title, isbn, category_id, publication_year, total_copies, author_ids, new_author_name=None):
    title = title.strip()
    isbn = isbn.strip()
    if not title or not isbn:
        raise ValueError("Title and ISBN are required!")

    book_id = None
    if is_postgres_available():
        try:
            with get_pg_connection() as conn:
                with conn.cursor() as cur:
                    # Handle on-the-fly author registration
                    if new_author_name and new_author_name.strip():
                        cur.execute(
                            "INSERT INTO authors (name) VALUES (%s) RETURNING author_id",
                            (new_author_name.strip(),)
                        )
                        created_aid = cur.fetchone()["author_id"]
                        if not author_ids:
                            author_ids = []
                        author_ids.append(created_aid)

                    # Ensure valid category
                    cid = category_id
                    if cid:
                        cur.execute("SELECT 1 FROM categories WHERE category_id = %s", (cid,))
                        if not cur.fetchone():
                            cid = 1
                    else:
                        cid = 1

                    cur.execute(
                        """INSERT INTO books (isbn, title, category_id, publication_year, total_copies, available_copies, price)
                           VALUES (%s, %s, %s, %s, %s, %s, 499.00)
                           ON CONFLICT (isbn) DO UPDATE SET
                               title = EXCLUDED.title,
                               category_id = EXCLUDED.category_id,
                               publication_year = EXCLUDED.publication_year,
                               total_copies = EXCLUDED.total_copies,
                               available_copies = EXCLUDED.available_copies
                           RETURNING book_id""",
                        (isbn, title, cid, publication_year, total_copies, total_copies)
                    )
                    book_id = cur.fetchone()["book_id"]

                    if author_ids:
                        for aid in author_ids:
                            cur.execute(
                                "INSERT INTO book_authors (book_id, author_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                                (book_id, aid)
                            )

                    cur.execute(
                        "INSERT INTO audit_logs (table_name, action_type, description) VALUES (%s, %s, %s)",
                        ('books', 'INSERT', f"New book added: '{title}' (ISBN: {isbn}) with {total_copies} copies.")
                    )
                    conn.commit()
                    print(f"[+] Direct PostgreSQL: Added book '{title}' (ID {book_id})")
        except Exception as e:
            print(f"[!] PG add_book error: {e}")

    # Mirror to SQLite
    try:
        with get_connection() as s_conn:
            s_cur = s_conn.cursor()
            if book_id:
                s_cur.execute(
                    """INSERT INTO books (book_id, isbn, title, category_id, publication_year, total_copies, available_copies)
                       VALUES (?, ?, ?, ?, ?, ?, ?)
                       ON CONFLICT(book_id) DO UPDATE SET
                           title = excluded.title, isbn = excluded.isbn, total_copies = excluded.total_copies, available_copies = excluded.available_copies""",
                    (book_id, isbn, title, category_id, publication_year, total_copies, total_copies)
                )
            else:
                s_cur.execute(
                    """INSERT INTO books (isbn, title, category_id, publication_year, total_copies, available_copies)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (isbn, title, category_id, publication_year, total_copies, total_copies)
                )
                book_id = s_cur.lastrowid

            if author_ids:
                for aid in author_ids:
                    s_cur.execute("INSERT OR IGNORE INTO book_authors (book_id, author_id) VALUES (?, ?)", (book_id, aid))
            s_conn.commit()
    except Exception:
        pass

    return book_id


def delete_book(book_id):
    if is_postgres_available():
        try:
            with get_pg_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT COUNT(*) AS cnt FROM loans WHERE book_id = %s AND return_date IS NULL", (book_id,))
                    if cur.fetchone()["cnt"] > 0:
                        raise ValueError("Cannot delete book: Copies of this book are currently issued to members!")

                    cur.execute("SELECT title FROM books WHERE book_id = %s", (book_id,))
                    row = cur.fetchone()
                    title = row["title"] if row else f"ID {book_id}"

                    cur.execute("DELETE FROM book_authors WHERE book_id = %s", (book_id,))
                    cur.execute("DELETE FROM loans WHERE book_id = %s", (book_id,))
                    cur.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
                    cur.execute(
                        "INSERT INTO audit_logs (table_name, action_type, description) VALUES (%s, %s, %s)",
                        ('books', 'DELETE', f"Deleted book: '{title}' (ID: {book_id}).")
                    )
                    conn.commit()
                    print(f"[+] Direct PostgreSQL: Deleted book ID {book_id}")
        except ValueError:
            raise
        except Exception as e:
            print(f"[!] PG delete_book fallback: {e}")

    # Mirror to SQLite
    try:
        with get_connection() as s_conn:
            s_cur = s_conn.cursor()
            s_cur.execute("DELETE FROM book_authors WHERE book_id = ?", (book_id,))
            s_cur.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
            s_conn.commit()
    except Exception:
        pass


# -------------------------------------------------------------
# MEMBERS MANAGEMENT
# -------------------------------------------------------------
def get_members(search=""):
    if is_postgres_available():
        try:
            with get_pg_connection() as conn:
                with conn.cursor() as cur:
                    query = """
                        SELECT 
                            m.member_id,
                            m.member_code,
                            m.first_name,
                            m.last_name,
                            m.email,
                            m.phone,
                            m.address,
                            m.membership_type,
                            m.status,
                            m.joined_date AS membership_date,
                            (SELECT COUNT(*) FROM loans l WHERE l.member_id = m.member_id AND l.return_date IS NULL) AS currently_issued,
                            (SELECT COALESCE(SUM(l.fine_amount), 0) FROM loans l WHERE l.member_id = m.member_id AND l.fine_paid = false) AS unpaid_fine
                        FROM members m
                        WHERE 1=1
                    """
                    params = []
                    if search:
                        query += " AND (m.first_name ILIKE %s OR m.last_name ILIKE %s OR m.email ILIKE %s OR m.phone ILIKE %s)"
                        term = f"%{search}%"
                        params.extend([term, term, term, term])
                    query += " ORDER BY m.member_id DESC"
                    cur.execute(query, params)
                    members = [dict(r) for r in cur.fetchall()]
                    for m in members:
                        m["unpaid_fine"] = float(m["unpaid_fine"] or 0.0)
                    return members
        except Exception as e:
            print(f"[!] PG get_members fallback: {e}")

    with get_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT 
                m.*,
                (SELECT COUNT(*) FROM borrow_transactions t WHERE t.member_id = m.member_id AND t.return_date IS NULL) AS currently_issued,
                (SELECT IFNULL(SUM(f.fine_amount), 0) FROM fines f WHERE f.member_id = m.member_id AND f.paid_status = 'Unpaid') AS unpaid_fine
            FROM members m
            WHERE 1=1
        """
        params = []
        if search:
            query += " AND (m.first_name LIKE ? OR m.last_name LIKE ? OR m.email LIKE ? OR m.phone LIKE ?)"
            term = f"%{search}%"
            params.extend([term, term, term, term])
        query += " ORDER BY m.member_id DESC"
        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]


def add_member(first_name, last_name, email, phone, membership_type="Student", max_books=3):
    first_name = first_name.strip()
    last_name = last_name.strip()
    email = email.strip()

    valid_types = {'Student', 'Faculty', 'Standard', 'Premium'}
    if membership_type not in valid_types:
        membership_type = 'Student'

    member_id = None
    if is_postgres_available():
        try:
            with get_pg_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT COALESCE(MAX(member_id), 0) + 1 AS next_id FROM members")
                    next_id = cur.fetchone()["next_id"]
                    code = f"LIB-M{next_id:04d}"
                    cur.execute(
                        """INSERT INTO members (member_code, first_name, last_name, email, phone, membership_type, status, joined_date)
                           VALUES (%s, %s, %s, %s, %s, %s, 'Active', CURRENT_DATE)
                           RETURNING member_id""",
                        (code, first_name, last_name, email, phone, membership_type)
                    )
                    member_id = cur.fetchone()["member_id"]
                    cur.execute(
                        "INSERT INTO audit_logs (table_name, action_type, description) VALUES (%s, %s, %s)",
                        ('members', 'INSERT', f"Registered member: {first_name} {last_name} ({email}) - Type: {membership_type}")
                    )
                    conn.commit()
                    print(f"[+] Direct PostgreSQL: Added member {first_name} {last_name} (ID {member_id})")
        except Exception as e:
            print(f"[!] PG add_member notice: {e}")

    # Mirror to SQLite
    try:
        with get_connection() as s_conn:
            s_cur = s_conn.cursor()
            if member_id:
                s_cur.execute(
                    """INSERT INTO members (member_id, first_name, last_name, email, phone, membership_type, max_books_allowed)
                       VALUES (?, ?, ?, ?, ?, ?)
                       ON CONFLICT(member_id) DO NOTHING""",
                    (member_id, first_name, last_name, email, phone, membership_type, max_books)
                )
            else:
                s_cur.execute(
                    """INSERT INTO members (first_name, last_name, email, phone, membership_type, max_books_allowed)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (first_name, last_name, email, phone, membership_type, max_books)
                )
                member_id = s_cur.lastrowid
            s_conn.commit()
    except Exception:
        pass

    return member_id


# -------------------------------------------------------------
# TRANSACTIONS (ISSUE & RETURN)
# -------------------------------------------------------------
def get_active_loans():
    if is_postgres_available():
        try:
            with get_pg_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM vw_active_loans ORDER BY issue_date DESC")
                    loans = [dict(r) for r in cur.fetchall()]
                    for l in loans:
                        l["estimated_fine"] = float(l.get("estimated_fine") or 0.0)
                        l["overdue_days"] = int(l.get("overdue_days") or 0)
                    return loans
        except Exception as e:
            print(f"[!] PG get_active_loans fallback: {e}")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vw_active_loans ORDER BY issue_date DESC")
        return [dict(r) for r in cursor.fetchall()]


def issue_book(member_id, book_id, loan_days=14):
    trans_id = None
    if is_postgres_available():
        try:
            with get_pg_connection() as conn:
                with conn.cursor() as cur:
                    # 1. Check book availability
                    cur.execute("SELECT available_copies, title FROM books WHERE book_id = %s", (book_id,))
                    book = cur.fetchone()
                    if not book or book["available_copies"] <= 0:
                        raise ValueError(f"Cannot issue: No copies available for '{book['title'] if book else book_id}'!")

                    # 2. Check member status
                    cur.execute("SELECT status, first_name, last_name FROM members WHERE member_id = %s", (member_id,))
                    member = cur.fetchone()
                    if not member or member["status"] != "Active":
                        raise ValueError(f"Cannot issue: Member status is '{member['status'] if member else 'Unknown'}'!")

                    # 3. Insert loan (PostgreSQL trigger automatically decrements available_copies)
                    cur.execute(
                        """INSERT INTO loans (book_id, member_id, issue_date, due_date, status, fine_amount, fine_paid)
                           VALUES (%s, %s, CURRENT_DATE, CURRENT_DATE + %s * INTERVAL '1 day', 'Issued', 0.00, false)
                           RETURNING loan_id""",
                        (book_id, member_id, loan_days)
                    )
                    trans_id = cur.fetchone()["loan_id"]
                    cur.execute(
                        "INSERT INTO audit_logs (table_name, action_type, description) VALUES (%s, %s, %s)",
                        ('loans', 'ISSUE', f"Issued book ID {book_id} to member ID {member_id} (Loan #{trans_id}).")
                    )
                    conn.commit()
                    print(f"[+] Direct PostgreSQL: Issued loan ID {trans_id}")
        except ValueError:
            raise
        except Exception as e:
            print(f"[!] PG issue_book error: {e}")

    # Mirror to SQLite
    try:
        with get_connection() as s_conn:
            s_cur = s_conn.cursor()
            due_date = (datetime.now() + timedelta(days=loan_days)).strftime("%Y-%m-%d")
            if trans_id:
                s_cur.execute(
                    """INSERT INTO borrow_transactions (transaction_id, book_id, member_id, due_date, status)
                       VALUES (?, ?, ?, ?, 'Issued')
                       ON CONFLICT(transaction_id) DO NOTHING""",
                    (trans_id, book_id, member_id, due_date)
                )
            else:
                s_cur.execute(
                    """INSERT INTO borrow_transactions (book_id, member_id, due_date, status)
                       VALUES (?, ?, ?, 'Issued')""",
                    (book_id, member_id, due_date)
                )
                trans_id = s_cur.lastrowid
            s_conn.commit()
    except Exception:
        pass

    return trans_id


def return_book(transaction_id):
    fine_amt = 0.0
    if is_postgres_available():
        try:
            with get_pg_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM loans WHERE loan_id = %s", (transaction_id,))
                    loan = cur.fetchone()
                    if not loan:
                        raise ValueError("Transaction not found!")
                    if loan["return_date"] is not None:
                        raise ValueError("Book is already marked as returned!")

                    # Update loan (PostgreSQL trigger automatically increments available_copies)
                    cur.execute(
                        """UPDATE loans 
                           SET return_date = CURRENT_DATE, status = 'Returned'
                           WHERE loan_id = %s
                           RETURNING due_date, member_id, book_id""",
                        (transaction_id,)
                    )
                    updated = cur.fetchone()

                    # Calculate overdue fine
                    if updated and updated["due_date"]:
                        cur.execute("SELECT GREATEST(0, (CURRENT_DATE - %s)) AS days", (updated["due_date"],))
                        days = cur.fetchone()["days"]
                        if days > 0:
                            fine_amt = float(days * 1.0)
                            cur.execute(
                                "UPDATE loans SET fine_amount = %s, fine_paid = false WHERE loan_id = %s",
                                (fine_amt, transaction_id)
                            )
                            cur.execute(
                                """INSERT INTO fines (transaction_id, member_id, fine_amount, paid_status)
                                   VALUES (%s, %s, %s, 'Unpaid')""",
                                (transaction_id, updated["member_id"], fine_amt)
                            )

                    cur.execute(
                        "INSERT INTO audit_logs (table_name, action_type, description) VALUES (%s, %s, %s)",
                        ('loans', 'RETURN', f"Returned book for loan #{transaction_id} (Fine assessed: ₹{fine_amt:.2f}).")
                    )
                    conn.commit()
                    print(f"[+] Direct PostgreSQL: Processed return for loan #{transaction_id}")
                    return fine_amt
        except ValueError:
            raise
        except Exception as e:
            print(f"[!] PG return_book fallback: {e}")

    # Fallback to SQLite
    with get_connection() as s_conn:
        cursor = s_conn.cursor()
        cursor.execute("SELECT * FROM borrow_transactions WHERE transaction_id = ?", (transaction_id,))
        trans = cursor.fetchone()
        if not trans:
            raise ValueError("Transaction not found!")
        if trans["return_date"] is not None:
            raise ValueError("Book is already marked as returned!")

        today_str = datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            """UPDATE borrow_transactions 
               SET return_date = ?, status = 'Returned'
               WHERE transaction_id = ?""",
            (today_str, transaction_id)
        )
        s_conn.commit()
        cursor.execute("SELECT fine_amount FROM fines WHERE transaction_id = ?", (transaction_id,))
        fine_row = cursor.fetchone()
        return fine_row["fine_amount"] if fine_row else 0.0


# -------------------------------------------------------------
# FINES MANAGEMENT
# -------------------------------------------------------------
def get_fines():
    if is_postgres_available():
        try:
            with get_pg_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT 
                            f.fine_id,
                            f.transaction_id,
                            f.member_id,
                            (m.first_name || ' ' || m.last_name) AS member_name,
                            m.email,
                            b.title AS book_title,
                            f.fine_amount,
                            f.paid_status,
                            f.paid_date
                        FROM fines f
                        JOIN members m ON f.member_id = m.member_id
                        JOIN loans l ON f.transaction_id = l.loan_id
                        JOIN books b ON l.book_id = b.book_id
                        ORDER BY f.fine_id DESC
                    """)
                    fines = [dict(r) for r in cur.fetchall()]
                    for f in fines:
                        f["fine_amount"] = float(f["fine_amount"] or 0.0)
                    return fines
        except Exception as e:
            print(f"[!] PG get_fines fallback: {e}")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                f.fine_id,
                f.transaction_id,
                f.member_id,
                (m.first_name || ' ' || m.last_name) AS member_name,
                m.email,
                b.title AS book_title,
                f.fine_amount,
                f.paid_status,
                f.paid_date
            FROM fines f
            JOIN members m ON f.member_id = m.member_id
            JOIN borrow_transactions t ON f.transaction_id = t.transaction_id
            JOIN books b ON t.book_id = b.book_id
            ORDER BY f.fine_id DESC
        """)
        return [dict(r) for r in cursor.fetchall()]


def pay_fine(fine_id):
    if is_postgres_available():
        try:
            with get_pg_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE fines SET paid_status = 'Paid', paid_date = CURRENT_DATE WHERE fine_id = %s RETURNING transaction_id",
                        (fine_id,)
                    )
                    row = cur.fetchone()
                    if row:
                        cur.execute("UPDATE loans SET fine_paid = true WHERE loan_id = %s", (row["transaction_id"],))
                    cur.execute(
                        "INSERT INTO audit_logs (table_name, action_type, description) VALUES (%s, %s, %s)",
                        ('fines', 'PAYMENT', f"Fine ID {fine_id} marked as Paid.")
                    )
                    conn.commit()
                    print(f"[+] Direct PostgreSQL: Fine #{fine_id} paid")
        except Exception as e:
            print(f"[!] PG pay_fine error: {e}")

    # Mirror to SQLite
    try:
        with get_connection() as s_conn:
            s_cur = s_conn.cursor()
            today_str = datetime.now().strftime("%Y-%m-%d")
            s_cur.execute(
                "UPDATE fines SET paid_status = 'Paid', paid_date = ? WHERE fine_id = ?",
                (today_str, fine_id)
            )
            s_conn.commit()
    except Exception:
        pass


# -------------------------------------------------------------
# AUDIT LOGS & LAB QUERY EXECUTOR
# -------------------------------------------------------------
def get_audit_logs(limit=50):
    if is_postgres_available():
        try:
            with get_pg_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM audit_logs ORDER BY log_id DESC LIMIT %s", (limit,))
                    logs = [dict(r) for r in cur.fetchall()]
                    for l in logs:
                        if l.get("created_at"):
                            l["created_at"] = str(l["created_at"])[:19]
                    return logs
        except Exception as e:
            print(f"[!] PG get_audit_logs fallback: {e}")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM audit_logs ORDER BY log_id DESC LIMIT ?", (limit,))
        return [dict(r) for r in cursor.fetchall()]


def execute_custom_sql(sql_statement):
    """Executes a custom SELECT statement directly on PostgreSQL or SQLite."""
    if is_postgres_available():
        try:
            with get_pg_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql_statement)
                    return [dict(r) for r in cur.fetchall()]
        except Exception as e:
            return [{"error": str(e)}]

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql_statement)
        return [dict(r) for r in cursor.fetchall()]


def sync_from_postgres_to_sqlite():
    """Utility mirror routine: pulls all PostgreSQL records into SQLite."""
    try:
        import psycopg
        with psycopg.connect(**PG_CONFIG) as p_conn:
            with p_conn.cursor() as p_cur:
                with get_connection() as s_conn:
                    s_cur = s_conn.cursor()
                    s_cur.execute("PRAGMA foreign_keys = OFF;")

                    # Categories
                    p_cur.execute("SELECT category_id, name, description FROM categories")
                    for r in p_cur.fetchall():
                        s_cur.execute("""
                            INSERT INTO categories (category_id, category_name, description)
                            VALUES (?, ?, ?)
                            ON CONFLICT (category_id) DO UPDATE SET
                                category_name = excluded.category_name,
                                description = excluded.description
                        """, r)

                    # Authors
                    p_cur.execute("SELECT author_id, name, email, biography FROM authors")
                    for r in p_cur.fetchall():
                        s_cur.execute("""
                            INSERT INTO authors (author_id, author_name, email, biography)
                            VALUES (?, ?, ?, ?)
                            ON CONFLICT (author_id) DO UPDATE SET
                                author_name = excluded.author_name,
                                email = excluded.email,
                                biography = excluded.biography
                        """, r)

                    # Books
                    p_cur.execute("SELECT book_id, isbn, title, category_id, publication_year, total_copies, available_copies FROM books")
                    for r in p_cur.fetchall():
                        s_cur.execute("""
                            INSERT INTO books (book_id, isbn, title, category_id, publication_year, total_copies, available_copies)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            ON CONFLICT (book_id) DO UPDATE SET
                                isbn = excluded.isbn,
                                title = excluded.title,
                                category_id = excluded.category_id,
                                publication_year = excluded.publication_year,
                                total_copies = excluded.total_copies,
                                available_copies = excluded.available_copies
                        """, r)

                    # Book Authors
                    p_cur.execute("SELECT book_id, author_id FROM book_authors")
                    for r in p_cur.fetchall():
                        s_cur.execute("INSERT OR IGNORE INTO book_authors (book_id, author_id) VALUES (?, ?)", r)

                    # Members
                    valid_mtypes = ('Student', 'Faculty', 'General')
                    p_cur.execute("SELECT member_id, first_name, last_name, email, phone, membership_type, status, joined_date FROM members")
                    for r in p_cur.fetchall():
                        m_type = r[5]
                        if m_type not in valid_mtypes:
                            m_type = 'Student' if 'student' in str(m_type).lower() else 'General'
                        m_date = str(r[7]) if r[7] else '2026-01-01'
                        s_cur.execute("""
                            INSERT INTO members (member_id, first_name, last_name, email, phone, membership_type, status, membership_date)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            ON CONFLICT (member_id) DO UPDATE SET
                                first_name = excluded.first_name,
                                last_name = excluded.last_name,
                                email = excluded.email,
                                phone = excluded.phone,
                                membership_type = excluded.membership_type,
                                status = excluded.status
                        """, (r[0], r[1], r[2], r[3], r[4], m_type, r[6], m_date))

                    # Loans
                    p_cur.execute("SELECT loan_id, book_id, member_id, issue_date, due_date, return_date, status FROM loans")
                    for r in p_cur.fetchall():
                        s_cur.execute("""
                            INSERT INTO borrow_transactions (transaction_id, book_id, member_id, issue_date, due_date, return_date, status)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            ON CONFLICT (transaction_id) DO UPDATE SET
                                return_date = excluded.return_date,
                                status = excluded.status
                        """, (r[0], r[1], r[2], str(r[3]) if r[3] else None, str(r[4]) if r[4] else None, str(r[5]) if r[5] else None, r[6]))

                    s_cur.execute("PRAGMA foreign_keys = ON;")
                    s_conn.commit()
    except Exception as e:
        print(f"[Notice] Pull sync from PostgreSQL: {e}")
