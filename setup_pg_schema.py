import psycopg

def setup_postgres_objects():
    print("[*] Setting up PostgreSQL schema and compatibility views...")
    with psycopg.connect("dbname=library_db user=postgres password=postgres host=localhost port=5432") as conn:
        with conn.cursor() as cur:
            # 1. Audit logs table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    log_id SERIAL PRIMARY KEY,
                    table_name VARCHAR(50) NOT NULL,
                    action_type VARCHAR(20) NOT NULL,
                    description TEXT NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # 2. Fines table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS fines (
                    fine_id SERIAL PRIMARY KEY,
                    transaction_id INT REFERENCES loans(loan_id) ON DELETE CASCADE,
                    member_id INT REFERENCES members(member_id) ON DELETE CASCADE,
                    fine_amount NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
                    paid_status VARCHAR(20) NOT NULL DEFAULT 'Unpaid',
                    paid_date DATE
                );
            """)

            # 3. Drop existing view if needed to update column definitions
            cur.execute("DROP VIEW IF EXISTS vw_book_catalog CASCADE;")
            cur.execute("""
                CREATE OR REPLACE VIEW vw_book_catalog AS
                SELECT 
                    b.book_id,
                    b.isbn,
                    b.title,
                    b.category_id,
                    c.name AS category_name,
                    COALESCE(string_agg(a.name, ', ' ORDER BY a.name), 'No Author Listed') AS authors,
                    b.publication_year,
                    b.total_copies,
                    b.available_copies,
                    (b.total_copies - b.available_copies) AS borrowed_copies,
                    b.price,
                    b.rack_location,
                    CASE 
                        WHEN b.available_copies > 0 THEN 'Available'
                        ELSE 'Out of Stock'
                    END AS status,
                    CASE 
                        WHEN b.available_copies = 0 THEN 'Out of Stock'
                        WHEN b.available_copies <= 2 THEN 'Low Availability'
                        ELSE 'Available'
                    END AS availability_status
                FROM books b
                LEFT JOIN categories c ON b.category_id = c.category_id
                LEFT JOIN book_authors ba ON b.book_id = ba.book_id
                LEFT JOIN authors a ON ba.author_id = a.author_id
                GROUP BY b.book_id, b.isbn, b.title, b.category_id, c.name, b.publication_year, b.total_copies, b.available_copies, b.price, b.rack_location;
            """)

            # 4. vw_active_loans view
            cur.execute("DROP VIEW IF EXISTS vw_active_loans CASCADE;")
            cur.execute("""
                CREATE OR REPLACE VIEW vw_active_loans AS
                SELECT 
                    l.loan_id AS transaction_id,
                    l.loan_id,
                    l.book_id,
                    b.title AS book_title,
                    b.isbn,
                    l.member_id,
                    m.member_code,
                    (m.first_name || ' ' || m.last_name) AS member_name,
                    (m.first_name || ' ' || m.last_name) AS borrower_name,
                    m.email AS member_email,
                    m.email AS borrower_email,
                    m.phone AS member_phone,
                    m.phone AS borrower_phone,
                    l.issue_date,
                    l.due_date,
                    l.status,
                    l.status AS loan_status,
                    GREATEST(0, (CURRENT_DATE - l.due_date)) AS overdue_days,
                    GREATEST(0, (CURRENT_DATE - l.due_date)) AS days_overdue,
                    CASE 
                        WHEN CURRENT_DATE > l.due_date THEN ((CURRENT_DATE - l.due_date)::numeric * 1.00)
                        ELSE 0.00
                    END AS estimated_fine,
                    l.notes
                FROM loans l
                JOIN books b ON l.book_id = b.book_id
                JOIN members m ON l.member_id = m.member_id
                WHERE l.return_date IS NULL;
            """)

            # 5. vw_library_summary view
            cur.execute("DROP VIEW IF EXISTS vw_library_summary CASCADE;")
            cur.execute("""
                CREATE OR REPLACE VIEW vw_library_summary AS
                SELECT 
                    (SELECT COUNT(*) FROM books) AS total_titles,
                    (SELECT COALESCE(SUM(total_copies), 0) FROM books) AS total_volumes,
                    (SELECT COALESCE(SUM(available_copies), 0) FROM books) AS available_volumes,
                    (SELECT COUNT(*) FROM members WHERE status = 'Active') AS active_members,
                    (SELECT COUNT(*) FROM loans WHERE return_date IS NULL) AS currently_borrowed,
                    (SELECT COALESCE(SUM(fine_amount), 0) FROM loans WHERE fine_paid = false) AS pending_fines_amount;
            """)

            # 6. Make sure authors and categories have alias views or easy columns if needed
            conn.commit()
            print("[+] PostgreSQL objects and views successfully created!")

if __name__ == '__main__':
    setup_postgres_objects()
