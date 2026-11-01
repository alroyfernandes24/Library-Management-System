import sqlite3
import psycopg
from datetime import datetime

def sync_database():
    print("[*] Starting complete synchronization between SQLite and PostgreSQL...")
    s_conn = sqlite3.connect('library.db')
    s_conn.row_factory = sqlite3.Row
    s_cur = s_conn.cursor()

    p_conn = psycopg.connect('dbname=library_db user=postgres password=postgres host=localhost port=5432')
    p_cur = p_conn.cursor()

    # 1. Truncate dependent child tables in PostgreSQL
    print("[*] 1. Clearing old records in PostgreSQL to ensure 100% ID alignment...")
    p_cur.execute("TRUNCATE TABLE loans, book_authors, books, members, authors, categories CASCADE;")

    # 2. Sync Categories
    print("[*] 2. Syncing categories...")
    s_cur.execute('SELECT category_id, category_name, description FROM categories ORDER BY category_id')
    for row in s_cur.fetchall():
        p_cur.execute('''
            INSERT INTO categories (category_id, name, description)
            VALUES (%s, %s, %s)
        ''', (row['category_id'], row['category_name'], row['description']))
    p_cur.execute("SELECT setval('categories_category_id_seq', (SELECT COALESCE(MAX(category_id), 1) FROM categories));")

    # 3. Sync Authors
    print("[*] 3. Syncing authors...")
    s_cur.execute('SELECT author_id, author_name, email, biography FROM authors ORDER BY author_id')
    seen_emails = set()
    for row in s_cur.fetchall():
        aid = row['author_id']
        name = row['author_name']
        email = row['email']
        bio = row['biography']

        # Ensure emails are unique if not null
        if email:
            if email in seen_emails:
                email = f"author{aid}_{email}"
            seen_emails.add(email)

        p_cur.execute('''
            INSERT INTO authors (author_id, name, email, biography)
            VALUES (%s, %s, %s, %s)
        ''', (aid, name, email, bio))
    p_cur.execute("SELECT setval('authors_author_id_seq', (SELECT COALESCE(MAX(author_id), 1) FROM authors));")

    # 4. Sync Books (All 52 books)
    print("[*] 4. Syncing all books (IDs 1 to 52)...")
    s_cur.execute('SELECT book_id, isbn, title, category_id, publication_year, total_copies, available_copies FROM books ORDER BY book_id')
    for row in s_cur.fetchall():
        cid = row['category_id']
        p_cur.execute('''
            INSERT INTO books (book_id, isbn, title, category_id, publication_year, total_copies, available_copies, price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 499.00)
        ''', (row['book_id'], row['isbn'], row['title'], cid, row['publication_year'], row['total_copies'], row['available_copies']))
    p_cur.execute("SELECT setval('books_book_id_seq', (SELECT COALESCE(MAX(book_id), 1) FROM books));")

    # 5. Sync Book_Authors
    print("[*] 5. Syncing book_authors...")
    s_cur.execute('SELECT book_id, author_id FROM book_authors')
    for row in s_cur.fetchall():
        p_cur.execute('''
            INSERT INTO book_authors (book_id, author_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        ''', (row['book_id'], row['author_id']))

    # 6. Sync Members
    print("[*] 6. Syncing members...")
    valid_types = {'Standard', 'Premium', 'Student', 'Faculty'}
    valid_statuses = {'Active', 'Suspended', 'Expired'}
    s_cur.execute('SELECT member_id, first_name, last_name, email, phone, membership_type, status, membership_date FROM members ORDER BY member_id')
    seen_member_emails = set()
    for row in s_cur.fetchall():
        mid = row['member_id']
        code = f"LIB-M{mid:04d}"
        m_email = row['email']
        if m_email in seen_member_emails:
            m_email = f"member{mid}_{m_email}"
        seen_member_emails.add(m_email)

        m_type = row['membership_type']
        if m_type not in valid_types:
            m_type = 'Student' if 'student' in str(m_type).lower() else 'Standard'

        m_status = row['status']
        if m_status not in valid_statuses:
            m_status = 'Active'

        m_date = row['membership_date'] or datetime.now().strftime("%Y-%m-%d")

        p_cur.execute('''
            INSERT INTO members (member_id, member_code, first_name, last_name, email, phone, membership_type, status, joined_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (mid, code, row['first_name'], row['last_name'], m_email, row['phone'], m_type, m_status, m_date))
    p_cur.execute("SELECT setval('members_member_id_seq', (SELECT COALESCE(MAX(member_id), 1) FROM members));")

    # 7. Sync Loans
    print("[*] 7. Syncing borrow transactions / loans...")
    valid_loan_statuses = {'Issued', 'Returned', 'Overdue'}
    s_cur.execute('SELECT transaction_id, book_id, member_id, issue_date, due_date, return_date, status FROM borrow_transactions ORDER BY transaction_id')
    for row in s_cur.fetchall():
        l_status = row['status']
        if l_status not in valid_loan_statuses:
            l_status = 'Returned' if row['return_date'] else 'Issued'

        p_cur.execute('''
            INSERT INTO loans (loan_id, book_id, member_id, issue_date, due_date, return_date, status, fine_amount, fine_paid)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 0.00, false)
        ''', (row['transaction_id'], row['book_id'], row['member_id'], row['issue_date'], row['due_date'], row['return_date'], l_status))
    p_cur.execute("SELECT setval('loans_loan_id_seq', (SELECT COALESCE(MAX(loan_id), 1) FROM loans));")

    p_conn.commit()
    print("[+] FULL SYNCHRONIZATION COMPLETE!")

    # Verify query
    print("\n========================================================")
    print("PostgreSQL Query Verification (Exact query from user screenshot):")
    print("SELECT book_id, title, isbn, total_copies, available_copies")
    print("FROM books")
    print("ORDER BY book_id DESC LIMIT 3;")
    print("========================================================")
    p_cur.execute("""
        SELECT book_id, title, isbn, total_copies, available_copies
        FROM books
        ORDER BY book_id DESC LIMIT 3;
    """)
    for r in p_cur.fetchall():
        print(f"ID: {r[0]} | Title: {r[1]} | ISBN: {r[2]} | Total: {r[3]} | Available: {r[4]}")

    p_cur.execute("SELECT count(*) FROM books;")
    print(f"\nTotal books in PostgreSQL: {p_cur.fetchone()[0]}")

if __name__ == '__main__':
    sync_database()
