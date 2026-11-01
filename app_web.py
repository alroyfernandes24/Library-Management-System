"""
Library Management System - Web Application Server
Zero external pip dependencies required (Uses built-in http.server and sqlite3).
Run with: python app_web.py
Access at: http://localhost:5000
"""

import json
import os
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
import db_manager

# Ensure UTF-8 output on Windows consoles
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

PORT = 5000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")


class LibraryRequestHandler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        response_bytes = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(response_bytes)

    def send_file(self, filepath, content_type="text/html; charset=utf-8"):
        if not os.path.exists(filepath):
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"File not found")
            return
        with open(filepath, "rb") as f:
            content = f.read()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            self.send_file(os.path.join(WEB_DIR, "index.html"))
        elif path.startswith("/assets/"):
            rel_file = path.replace("/assets/", "").replace("/", os.sep)
            file_path = os.path.join(WEB_DIR, "assets", rel_file)
            ctype = "text/css" if path.endswith(".css") else ("application/javascript" if path.endswith(".js") else "text/plain")
            self.send_file(file_path, ctype)
        elif path == "/api/sync":
            try:
                db_manager.sync_from_postgres_to_sqlite()
                self.send_json({"success": True, "message": "Synced from PostgreSQL"})
            except Exception as e:
                self.send_json({"success": False, "error": str(e)})
        elif path == "/api/summary":
            self.send_json(db_manager.get_dashboard_summary())
        elif path == "/api/books":
            search = query.get("search", [""])[0]
            cat_id = query.get("category_id", [None])[0]
            if cat_id:
                cat_id = int(cat_id)
            self.send_json(db_manager.get_books(search, cat_id))
        elif path == "/api/categories":
            self.send_json(db_manager.get_categories())
        elif path == "/api/authors":
            self.send_json(db_manager.get_authors())
        elif path == "/api/members":
            search = query.get("search", [""])[0]
            self.send_json(db_manager.get_members(search))
        elif path == "/api/loans":
            self.send_json(db_manager.get_active_loans())
        elif path == "/api/fines":
            self.send_json(db_manager.get_fines())
        elif path == "/api/logs":
            self.send_json(db_manager.get_audit_logs())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        data = json.loads(body) if body else {}

        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        try:
            if path == "/api/books":
                book_id = db_manager.add_book(
                    title=data["title"],
                    isbn=data["isbn"],
                    category_id=data.get("category_id"),
                    publication_year=data.get("publication_year", 2024),
                    total_copies=data.get("total_copies", 1),
                    author_ids=data.get("author_ids", []),
                    new_author_name=data.get("new_author_name")
                )
                self.send_json({"success": True, "book_id": book_id})

            elif path == "/api/authors":
                author_id = db_manager.add_author(
                    author_name=data["author_name"],
                    email=data.get("email", ""),
                    biography=data.get("biography", "")
                )
                self.send_json({"success": True, "author_id": author_id})

            elif path == "/api/members":
                member_id = db_manager.add_member(
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    email=data["email"],
                    phone=data.get("phone", ""),
                    membership_type=data.get("membership_type", "Student"),
                    max_books=data.get("max_books", 3)
                )
                self.send_json({"success": True, "member_id": member_id})

            elif path == "/api/issue":
                tx_id = db_manager.issue_book(
                    member_id=data["member_id"],
                    book_id=data["book_id"],
                    loan_days=data.get("loan_days", 14)
                )
                self.send_json({"success": True, "transaction_id": tx_id})

            elif path == "/api/return":
                fine = db_manager.return_book(transaction_id=data["transaction_id"])
                self.send_json({"success": True, "fine": fine})

            elif path == "/api/fines/pay":
                db_manager.pay_fine(fine_id=data["fine_id"])
                self.send_json({"success": True})

            elif path == "/api/sql":
                result = db_manager.execute_custom_sql(data.get("query", ""))
                self.send_json(result)

            else:
                self.send_response(404)
                self.end_headers()

        except Exception as e:
            self.send_json({"error": str(e)}, status=400)

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        try:
            if path == "/api/books":
                book_id = int(query["id"][0])
                db_manager.delete_book(book_id)
                self.send_json({"success": True})
            else:
                self.send_response(404)
                self.end_headers()
        except Exception as e:
            self.send_json({"error": str(e)}, status=400)


def run_server():
    db_manager.init_database()
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, LibraryRequestHandler)
    print("=" * 60)
    print(f"[*] Library Management System Web Server Running!")
    print(f"[*] Open in your browser: http://localhost:{PORT}")
    print("=" * 60)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Server shutting down...")
        httpd.server_close()


if __name__ == "__main__":
    run_server()
