"""
Capture automated screenshots of the Library Management System web interface
using Selenium Edge WebDriver with live SQLite data.
"""

import os
import time
import threading
from http.server import HTTPServer
from app_web import LibraryRequestHandler, PORT
from selenium import webdriver
from selenium.webdriver.edge.options import Options

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIAG_DIR = os.path.join(BASE_DIR, "diagrams")
os.makedirs(DIAG_DIR, exist_ok=True)


def run_test_server():
    httpd = HTTPServer(("", PORT), LibraryRequestHandler)
    httpd.serve_forever()


def capture_all():
    # Start server in background thread
    t = threading.Thread(target=run_test_server, daemon=True)
    t.start()
    time.sleep(1.5)

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,850")
    driver = webdriver.Edge(options=opts)

    try:
        url = f"http://localhost:{PORT}"
        print(f"[*] Navigating to {url}...")
        driver.get(url)
        time.sleep(2)

        # 1. Dashboard screenshot
        dash_path = os.path.join(DIAG_DIR, "screenshot_dashboard.png")
        driver.save_screenshot(dash_path)
        print(f"[+] Saved {dash_path}")

        # 2. Book Catalog Tab
        driver.execute_script("showSection('books')")
        time.sleep(1.5)
        catalog_path = os.path.join(DIAG_DIR, "screenshot_catalog.png")
        driver.save_screenshot(catalog_path)
        print(f"[+] Saved {catalog_path}")

        # 3. Add Book Modal with Add Author expanded
        driver.execute_script("new bootstrap.Modal(document.getElementById('addBookModal')).show();")
        time.sleep(1)
        driver.execute_script("toggleNewAuthorSection(true);")
        time.sleep(1)
        modal_path = os.path.join(DIAG_DIR, "screenshot_add_book_modal.png")
        driver.save_screenshot(modal_path)
        print(f"[+] Saved {modal_path}")

        # Close modal
        driver.execute_script("bootstrap.Modal.getInstance(document.getElementById('addBookModal')).hide();")
        time.sleep(0.5)

        # 4. Issue & Loans Tab
        driver.execute_script("showSection('loans')")
        time.sleep(1.5)
        loans_path = os.path.join(DIAG_DIR, "screenshot_loans.png")
        driver.save_screenshot(loans_path)
        print(f"[+] Saved {loans_path}")

        # 5. Fines Tab
        driver.execute_script("showSection('fines')")
        time.sleep(1.5)
        fines_path = os.path.join(DIAG_DIR, "screenshot_fines.png")
        driver.save_screenshot(fines_path)
        print(f"[+] Saved {fines_path}")

        # 6. Audit Logs Tab
        driver.execute_script("showSection('logs')")
        time.sleep(1.5)
        logs_path = os.path.join(DIAG_DIR, "screenshot_audit_logs.png")
        driver.save_screenshot(logs_path)
        print(f"[+] Saved {logs_path}")

        print("[*] All screenshots captured successfully!")

    finally:
        driver.quit()


if __name__ == "__main__":
    capture_all()
