"""
Library Management System - Desktop GUI Application (Tkinter)
Zero external dependencies required (Uses standard library tkinter and sqlite3).
Run with: python app_gui.py
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox
import db_manager

# Ensure UTF-8 output on Windows consoles
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System - DBMS Mini Project")
        self.geometry("1100x700")
        self.minsize(900, 600)
        
        # Ensure database is initialized
        db_manager.init_database()

        # Styling
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        
        # Colors & Fonts
        self.configure(bg="#f4f6f9")
        self.style.configure(".", font=("Segoe UI", 10))
        self.style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[12, 6])
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        self.style.configure("Action.TButton", font=("Segoe UI", 9, "bold"), foreground="#ffffff", background="#0d6efd")

        # Top Header Banner
        header = tk.Frame(self, bg="#1e293b", height=60)
        header.pack(fill="x", side="top")
        
        title_lbl = tk.Label(
            header, 
            text="📚 Library Management System", 
            font=("Segoe UI", 15, "bold"), 
            fg="#ffffff", 
            bg="#1e293b",
            padx=15, 
            pady=12
        )
        title_lbl.pack(side="left")

        refresh_btn = tk.Button(
            header,
            text="🔄 Refresh All Data",
            font=("Segoe UI", 9, "bold"),
            bg="#3b82f6",
            fg="white",
            relief="flat",
            padx=10,
            pady=4,
            command=self.refresh_all
        )
        refresh_btn.pack(side="right", padx=15, pady=12)

        # Tabbed Interface
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Create Tabs
        self.tab_dashboard = ttk.Frame(self.notebook)
        self.tab_books = ttk.Frame(self.notebook)
        self.tab_members = ttk.Frame(self.notebook)
        self.tab_issue_return = ttk.Frame(self.notebook)
        self.tab_fines = ttk.Frame(self.notebook)
        self.tab_logs = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_dashboard, text=" 📊 Dashboard ")
        self.notebook.add(self.tab_books, text=" 📖 Book Catalog ")
        self.notebook.add(self.tab_members, text=" 👥 Members ")
        self.notebook.add(self.tab_issue_return, text=" 🔄 Issue / Return ")
        self.notebook.add(self.tab_fines, text=" 💰 Fines Tracker ")
        self.notebook.add(self.tab_logs, text=" 📝 Audit Logs ")

        # Setup Tab Contents
        self.build_dashboard_tab()
        self.build_books_tab()
        self.build_members_tab()
        self.build_issue_return_tab()
        self.build_fines_tab()
        self.build_logs_tab()

        self.refresh_all()

    def refresh_all(self):
        try:
            db_manager.sync_from_postgres_to_sqlite()
        except Exception:
            pass
        self.load_dashboard_data()
        self.load_books_data()
        self.load_members_data()
        self.load_loans_data()
        self.load_fines_data()
        self.load_logs_data()

    # -------------------------------------------------------------
    # 1. DASHBOARD TAB
    # -------------------------------------------------------------
    def build_dashboard_tab(self):
        frame = self.tab_dashboard
        frame.configure(padding=20)

        intro_lbl = tk.Label(
            frame, 
            text="System Overview & Real-Time DBMS Analytics", 
            font=("Segoe UI", 13, "bold"), 
            fg="#334155"
        )
        intro_lbl.pack(anchor="w", pady=(0, 15))

        cards_frame = tk.Frame(frame)
        cards_frame.pack(fill="x", pady=10)

        self.stat_cards = {}
        metrics = [
            ("total_titles", "Total Book Titles", "#3b82f6"),
            ("total_volumes", "Total Copies (Volumes)", "#6366f1"),
            ("available_volumes", "Available on Shelf", "#10b981"),
            ("currently_borrowed", "Currently Borrowed", "#f59e0b"),
            ("active_members", "Active Members", "#8b5cf6"),
            ("pending_fines_amount", "Pending Fines (₹)", "#ef4444")
        ]

        row, col = 0, 0
        for key, label, color in metrics:
            card = tk.Frame(cards_frame, bg="white", relief="ridge", bd=1, padx=20, pady=15)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            cards_frame.columnconfigure(col, weight=1)

            tk.Label(card, text=label, font=("Segoe UI", 10), fg="#64748b", bg="white").pack(anchor="w")
            val_lbl = tk.Label(card, text="0", font=("Segoe UI", 22, "bold"), fg=color, bg="white")
            val_lbl.pack(anchor="w", pady=(5, 0))
            self.stat_cards[key] = val_lbl

            col += 1
            if col > 2:
                col = 0
                row += 1

    def load_dashboard_data(self):
        summary = db_manager.get_dashboard_summary()
        for k, v in summary.items():
            if k in self.stat_cards:
                if k == "pending_fines_amount":
                    self.stat_cards[k].config(text=f"₹{v:.2f}")
                else:
                    self.stat_cards[k].config(text=str(v))

    # -------------------------------------------------------------
    # 2. BOOKS CATALOG TAB
    # -------------------------------------------------------------
    def build_books_tab(self):
        frame = self.tab_books
        frame.configure(padding=15)

        # Controls top bar
        ctrl_frame = tk.Frame(frame)
        ctrl_frame.pack(fill="x", pady=(0, 10))

        tk.Label(ctrl_frame, text="Search Books:").pack(side="left", padx=(0, 5))
        self.book_search_var = tk.StringVar()
        search_entry = ttk.Entry(ctrl_frame, textvariable=self.book_search_var, width=28)
        search_entry.pack(side="left", padx=5)
        search_entry.bind("<Return>", lambda e: self.load_books_data())

        ttk.Button(ctrl_frame, text="Search", command=self.load_books_data).pack(side="left", padx=5)
        ttk.Button(ctrl_frame, text="Clear", command=self.clear_book_search).pack(side="left", padx=5)

        ttk.Button(ctrl_frame, text="➕ Add New Book", command=self.open_add_book_dialog).pack(side="right", padx=5)
        ttk.Button(ctrl_frame, text="🗑️ Delete Selected Book", command=self.delete_selected_book).pack(side="right", padx=5)

        # Treeview table
        columns = ("ID", "ISBN", "Title", "Category", "Authors", "Year", "Total", "Available", "Status")
        self.book_tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        widths = {"ID": 45, "ISBN": 130, "Title": 260, "Category": 140, "Authors": 200, "Year": 60, "Total": 60, "Available": 70, "Status": 90}
        for col in columns:
            self.book_tree.heading(col, text=col)
            self.book_tree.column(col, width=widths.get(col, 80), anchor="center" if col in ["ID", "Year", "Total", "Available", "Status"] else "w")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.book_tree.yview)
        self.book_tree.configure(yscrollcommand=scrollbar.set)
        
        self.book_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def clear_book_search(self):
        self.book_search_var.set("")
        self.load_books_data()

    def load_books_data(self):
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
        search = self.book_search_var.get().strip()
        books = db_manager.get_books(search=search)
        for b in books:
            self.book_tree.insert("", "end", values=(
                b["book_id"],
                b["isbn"],
                b["title"],
                b["category_name"] or "None",
                b["authors"] or "Unknown",
                b["publication_year"] or "-",
                b["total_copies"],
                b["available_copies"],
                b["status"]
            ))

    def open_add_book_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title("Add New Book")
        dlg.geometry("480x460")
        dlg.transient(self)
        dlg.grab_set()

        categories = db_manager.get_categories()

        tk.Label(dlg, text="Title: *", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20, pady=(10, 2))
        title_entry = ttk.Entry(dlg, width=45)
        title_entry.pack(padx=20, fill="x")

        tk.Label(dlg, text="ISBN: *", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20, pady=(10, 2))
        isbn_entry = ttk.Entry(dlg, width=45)
        isbn_entry.pack(padx=20, fill="x")

        tk.Label(dlg, text="Category:", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20, pady=(10, 2))
        cat_var = tk.StringVar()
        cat_combo = ttk.Combobox(dlg, textvariable=cat_var, state="readonly")
        cat_combo['values'] = [f"{c['category_id']}: {c['category_name']}" for c in categories]
        if categories:
            cat_combo.current(0)
        cat_combo.pack(padx=20, fill="x")

        # Author section with "Add Author" option
        auth_header_frame = tk.Frame(dlg)
        auth_header_frame.pack(fill="x", padx=20, pady=(10, 2))
        tk.Label(auth_header_frame, text="Author: *", font=("Segoe UI", 9, "bold")).pack(side="left")

        auth_input_frame = tk.Frame(dlg)
        auth_input_frame.pack(fill="x", padx=20)

        author_var = tk.StringVar()
        author_combo = ttk.Combobox(auth_input_frame, textvariable=author_var, state="readonly")

        def refresh_author_dropdown(select_id=None):
            current_authors = db_manager.get_authors()
            items = [f"{a['author_id']}: {a['author_name']}" for a in current_authors]
            author_combo['values'] = items
            if select_id:
                for idx, a in enumerate(current_authors):
                    if a['author_id'] == select_id:
                        author_combo.current(idx)
                        return
            if items and not author_var.get():
                author_combo.current(0)

        refresh_author_dropdown()
        author_combo.pack(side="left", fill="x", expand=True, padx=(0, 6))

        def open_quick_add_author():
            a_dlg = tk.Toplevel(dlg)
            a_dlg.title("Add New Author")
            a_dlg.geometry("380x270")
            a_dlg.transient(dlg)
            a_dlg.grab_set()

            tk.Label(a_dlg, text="Author Name: *", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20, pady=(15, 2))
            a_name_entry = ttk.Entry(a_dlg, width=35)
            a_name_entry.pack(padx=20, fill="x")
            a_name_entry.focus_set()

            tk.Label(a_dlg, text="Email (Optional):", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20, pady=(10, 2))
            a_email_entry = ttk.Entry(a_dlg, width=35)
            a_email_entry.pack(padx=20, fill="x")

            tk.Label(a_dlg, text="Biography (Optional):", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20, pady=(10, 2))
            a_bio_entry = ttk.Entry(a_dlg, width=35)
            a_bio_entry.pack(padx=20, fill="x")

            def save_new_author():
                a_name = a_name_entry.get().strip()
                a_email = a_email_entry.get().strip()
                a_bio = a_bio_entry.get().strip()
                if not a_name:
                    messagebox.showerror("Validation Error", "Author name cannot be empty!", parent=a_dlg)
                    return
                try:
                    new_id = db_manager.add_author(a_name, a_email, a_bio)
                    refresh_author_dropdown(select_id=new_id)
                    a_dlg.destroy()
                    messagebox.showinfo("Success", f"Author '{a_name}' added and selected!", parent=dlg)
                except Exception as ex:
                    messagebox.showerror("Error", str(ex), parent=a_dlg)

            btn_frame = tk.Frame(a_dlg)
            btn_frame.pack(pady=15)
            ttk.Button(btn_frame, text="Save Author", command=save_new_author).pack(side="left", padx=5)
            ttk.Button(btn_frame, text="Cancel", command=a_dlg.destroy).pack(side="left", padx=5)

        new_auth_btn = ttk.Button(auth_input_frame, text="➕ Add Author", command=open_quick_add_author)
        new_auth_btn.pack(side="right")

        row = tk.Frame(dlg)
        row.pack(fill="x", padx=20, pady=(10, 2))
        
        tk.Label(row, text="Pub Year:", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w")
        year_entry = ttk.Entry(row, width=12)
        year_entry.insert(0, "2024")
        year_entry.grid(row=1, column=0, padx=(0, 10))

        tk.Label(row, text="Total Copies:", font=("Segoe UI", 9, "bold")).grid(row=0, column=1, sticky="w")
        copies_entry = ttk.Entry(row, width=12)
        copies_entry.insert(0, "5")
        copies_entry.grid(row=1, column=1)

        def save_book():
            title = title_entry.get().strip()
            isbn = isbn_entry.get().strip()
            if not title or not isbn:
                messagebox.showerror("Validation Error", "Title and ISBN are required!", parent=dlg)
                return
            try:
                year = int(year_entry.get().strip())
                copies = int(copies_entry.get().strip())
                cat_id = int(cat_var.get().split(":")[0]) if cat_var.get() else None
                author_id = int(author_var.get().split(":")[0]) if author_var.get() else None
                
                db_manager.add_book(title, isbn, cat_id, year, copies, [author_id] if author_id else [])
                messagebox.showinfo("Success", f"Book '{title}' added successfully!", parent=dlg)
                dlg.destroy()
                self.refresh_all()
            except Exception as ex:
                messagebox.showerror("Error", str(ex), parent=dlg)

        ttk.Button(dlg, text="Save Book", command=save_book).pack(pady=20)

    def delete_selected_book(self):
        sel = self.book_tree.selection()
        if not sel:
            messagebox.showwarning("Notice", "Please select a book row to delete!")
            return
        vals = self.book_tree.item(sel[0], "values")
        book_id, title = vals[0], vals[2]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete book '{title}' (ID {book_id})?"):
            try:
                db_manager.delete_book(int(book_id))
                messagebox.showinfo("Success", "Book deleted successfully!")
                self.refresh_all()
            except Exception as ex:
                messagebox.showerror("Action Denied", str(ex))

    # -------------------------------------------------------------
    # 3. MEMBERS TAB
    # -------------------------------------------------------------
    def build_members_tab(self):
        frame = self.tab_members
        frame.configure(padding=15)

        ctrl_frame = tk.Frame(frame)
        ctrl_frame.pack(fill="x", pady=(0, 10))

        tk.Label(ctrl_frame, text="Search Member:").pack(side="left", padx=(0, 5))
        self.member_search_var = tk.StringVar()
        entry = ttk.Entry(ctrl_frame, textvariable=self.member_search_var, width=28)
        entry.pack(side="left", padx=5)
        entry.bind("<Return>", lambda e: self.load_members_data())

        ttk.Button(ctrl_frame, text="Search", command=self.load_members_data).pack(side="left", padx=5)
        ttk.Button(ctrl_frame, text="➕ Register Member", command=self.open_add_member_dialog).pack(side="right", padx=5)

        cols = ("ID", "Name", "Email", "Phone", "Type", "Status", "Joined", "Issued Books", "Unpaid Fine")
        self.member_tree = ttk.Treeview(frame, columns=cols, show="headings", height=15)
        for c in cols:
            self.member_tree.heading(c, text=c)
            self.member_tree.column(c, width=105, anchor="center" if c in ["ID", "Type", "Status", "Joined", "Issued Books", "Unpaid Fine"] else "w")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.member_tree.yview)
        self.member_tree.configure(yscrollcommand=scrollbar.set)
        self.member_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_members_data(self):
        for item in self.member_tree.get_children():
            self.member_tree.delete(item)
        members = db_manager.get_members(search=self.member_search_var.get().strip())
        for m in members:
            self.member_tree.insert("", "end", values=(
                m["member_id"],
                f"{m['first_name']} {m['last_name']}",
                m["email"],
                m["phone"] or "-",
                m["membership_type"],
                m["status"],
                m["membership_date"],
                m["currently_issued"],
                f"₹{m['unpaid_fine']:.2f}"
            ))

    def open_add_member_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title("Register New Member")
        dlg.geometry("400x380")
        dlg.transient(self)
        dlg.grab_set()

        tk.Label(dlg, text="First Name: *", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20, pady=(10, 2))
        fn_entry = ttk.Entry(dlg)
        fn_entry.pack(fill="x", padx=20)

        tk.Label(dlg, text="Last Name: *", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20, pady=(8, 2))
        ln_entry = ttk.Entry(dlg)
        ln_entry.pack(fill="x", padx=20)

        tk.Label(dlg, text="Email: *", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20, pady=(8, 2))
        email_entry = ttk.Entry(dlg)
        email_entry.pack(fill="x", padx=20)

        tk.Label(dlg, text="Phone:", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20, pady=(8, 2))
        phone_entry = ttk.Entry(dlg)
        phone_entry.pack(fill="x", padx=20)

        tk.Label(dlg, text="Membership Type:", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20, pady=(8, 2))
        type_var = tk.StringVar(value="Student")
        type_combo = ttk.Combobox(dlg, textvariable=type_var, values=["Student", "Faculty", "General"], state="readonly")
        type_combo.pack(fill="x", padx=20)

        def save_member():
            fn = fn_entry.get().strip()
            ln = ln_entry.get().strip()
            em = email_entry.get().strip()
            ph = phone_entry.get().strip()
            mtype = type_var.get()
            max_books = 8 if mtype == "Faculty" else 3
            if not fn or not ln or not em:
                messagebox.showerror("Error", "First Name, Last Name, and Email are required!", parent=dlg)
                return
            try:
                db_manager.add_member(fn, ln, em, ph, mtype, max_books)
                messagebox.showinfo("Success", f"Member {fn} {ln} registered!", parent=dlg)
                dlg.destroy()
                self.refresh_all()
            except Exception as ex:
                messagebox.showerror("Error", str(ex), parent=dlg)

        ttk.Button(dlg, text="Register Member", command=save_member).pack(pady=20)

    # -------------------------------------------------------------
    # 4. ISSUE / RETURN TAB
    # -------------------------------------------------------------
    def build_issue_return_tab(self):
        frame = self.tab_issue_return
        frame.configure(padding=15)

        # Quick Issue Form (Top box)
        issue_box = ttk.LabelFrame(frame, text="Issue Book to Member (Demonstrates Borrowing Trigger)", padding=10)
        issue_box.pack(fill="x", pady=(0, 15))

        f = tk.Frame(issue_box)
        f.pack(fill="x")

        tk.Label(f, text="Select Member:").grid(row=0, column=0, sticky="w", padx=5)
        self.issue_member_combo = ttk.Combobox(f, state="readonly", width=32)
        self.issue_member_combo.grid(row=1, column=0, padx=5, pady=5)

        tk.Label(f, text="Select Book (Available only):").grid(row=0, column=1, sticky="w", padx=5)
        self.issue_book_combo = ttk.Combobox(f, state="readonly", width=45)
        self.issue_book_combo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(f, text="Loan Days:").grid(row=0, column=2, sticky="w", padx=5)
        self.loan_days_entry = ttk.Entry(f, width=10)
        self.loan_days_entry.insert(0, "14")
        self.loan_days_entry.grid(row=1, column=2, padx=5, pady=5)

        ttk.Button(f, text="Issue Book", command=self.do_issue_book).grid(row=1, column=3, padx=15, pady=5)

        # Active Loans Table
        loans_lbl = tk.Label(frame, text="Currently Borrowed Books (Active Loans):", font=("Segoe UI", 10, "bold"))
        loans_lbl.pack(anchor="w", pady=(5, 5))

        cols = ("TxID", "Book Title", "Member Name", "Email", "Issue Date", "Due Date", "Days Overdue", "Status")
        self.loans_tree = ttk.Treeview(frame, columns=cols, show="headings", height=10)
        for c in cols:
            self.loans_tree.heading(c, text=c)
            self.loans_tree.column(c, width=110, anchor="center" if c in ["TxID", "Issue Date", "Due Date", "Days Overdue", "Status"] else "w")

        self.loans_tree.pack(fill="both", expand=True)

        btn_bar = tk.Frame(frame)
        btn_bar.pack(fill="x", pady=10)
        ttk.Button(btn_bar, text="📥 Return Selected Book", command=self.do_return_book).pack(side="left")

    def load_loans_data(self):
        # Refresh dropdowns
        members = db_manager.get_members()
        self.issue_member_combo['values'] = [f"{m['member_id']} - {m['first_name']} {m['last_name']} ({m['status']})" for m in members if m['status'] == 'Active']
        if self.issue_member_combo['values']:
            self.issue_member_combo.current(0)

        books = db_manager.get_books()
        self.issue_book_combo['values'] = [f"{b['book_id']} - {b['title']} (Avail: {b['available_copies']})" for b in books if b['available_copies'] > 0]
        if self.issue_book_combo['values']:
            self.issue_book_combo.current(0)

        # Refresh table
        for item in self.loans_tree.get_children():
            self.loans_tree.delete(item)
        loans = db_manager.get_active_loans()
        for l in loans:
            overdue_val = int(l['overdue_days']) if l['overdue_days'] is not None else 0
            self.loans_tree.insert("", "end", values=(
                l["transaction_id"],
                l["book_title"],
                l["member_name"],
                l["member_email"],
                l["issue_date"],
                l["due_date"],
                f"{overdue_val} days" if overdue_val > 0 else "None",
                l["loan_status"]
            ))

    def do_issue_book(self):
        if not self.issue_member_combo.get() or not self.issue_book_combo.get():
            messagebox.showwarning("Notice", "Please select both a member and an available book!")
            return
        try:
            m_id = int(self.issue_member_combo.get().split(" - ")[0])
            b_id = int(self.issue_book_combo.get().split(" - ")[0])
            days = int(self.loan_days_entry.get().strip() or "14")
            
            tx_id = db_manager.issue_book(m_id, b_id, days)
            messagebox.showinfo("Success", f"Book issued successfully! Transaction ID: {tx_id}")
            self.refresh_all()
        except Exception as ex:
            messagebox.showerror("Issue Failed", str(ex))

    def do_return_book(self):
        sel = self.loans_tree.selection()
        if not sel:
            messagebox.showwarning("Notice", "Select an active loan row from the table to return!")
            return
        vals = self.loans_tree.item(sel[0], "values")
        tx_id, title, member = vals[0], vals[1], vals[2]

        if messagebox.askyesno("Confirm Return", f"Confirm return of '{title}' by {member}?"):
            try:
                fine = db_manager.return_book(int(tx_id))
                msg = f"Book '{title}' returned successfully!"
                if fine > 0:
                    msg += f"\n\n⚠️ OVERDUE NOTICE: A fine of ₹{fine:.2f} has been calculated and charged to {member}!"
                messagebox.showinfo("Return Processed", msg)
                self.refresh_all()
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

    # -------------------------------------------------------------
    # 5. FINES TAB
    # -------------------------------------------------------------
    def build_fines_tab(self):
        frame = self.tab_fines
        frame.configure(padding=15)

        tk.Label(frame, text="Overdue Fines & Penalty Management", font=("Segoe UI", 12, "bold"), fg="#1e293b").pack(anchor="w", pady=(0, 10))

        cols = ("Fine ID", "Tx ID", "Member ID", "Member Name", "Book Title", "Fine Amount (₹)", "Status", "Paid Date")
        self.fines_tree = ttk.Treeview(frame, columns=cols, show="headings", height=15)
        for c in cols:
            self.fines_tree.heading(c, text=c)
            self.fines_tree.column(c, width=110, anchor="center" if c in ["Fine ID", "Tx ID", "Member ID", "Fine Amount (₹)", "Status", "Paid Date"] else "w")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.fines_tree.yview)
        self.fines_tree.configure(yscrollcommand=scrollbar.set)
        self.fines_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        bottom = tk.Frame(frame)
        bottom.pack(fill="x", pady=10)
        ttk.Button(bottom, text="💵 Mark Fine as Paid", command=self.do_pay_fine).pack(side="left")

    def load_fines_data(self):
        for item in self.fines_tree.get_children():
            self.fines_tree.delete(item)
        fines = db_manager.get_fines()
        for f in fines:
            self.fines_tree.insert("", "end", values=(
                f["fine_id"],
                f["transaction_id"],
                f["member_id"],
                f["member_name"],
                f["book_title"],
                f"₹{f['fine_amount']:.2f}",
                f["paid_status"],
                f["paid_date"] or "-"
            ))

    def do_pay_fine(self):
        sel = self.fines_tree.selection()
        if not sel:
            messagebox.showwarning("Notice", "Please select a fine from the table!")
            return
        vals = self.fines_tree.item(sel[0], "values")
        fine_id, status = vals[0], vals[6]
        if status == "Paid":
            messagebox.showinfo("Notice", "This fine is already paid!")
            return
        if messagebox.askyesno("Confirm Payment", f"Mark Fine ID {fine_id} as Paid?"):
            db_manager.pay_fine(int(fine_id))
            messagebox.showinfo("Success", "Fine recorded as Paid!")
            self.refresh_all()

    # -------------------------------------------------------------
    # 6. AUDIT LOGS TAB
    # -------------------------------------------------------------
    def build_logs_tab(self):
        frame = self.tab_logs
        frame.configure(padding=15)

        tk.Label(frame, text="DBMS Audit Trail (Trigger Invocations & Event History)", font=("Segoe UI", 12, "bold"), fg="#1e293b").pack(anchor="w", pady=(0, 10))

        cols = ("Log ID", "Table", "Action", "Description", "Timestamp")
        self.logs_tree = ttk.Treeview(frame, columns=cols, show="headings", height=15)
        for c in cols:
            self.logs_tree.heading(c, text=c)
            self.logs_tree.column(c, width=120 if c != "Description" else 400, anchor="center" if c in ["Log ID", "Table", "Action", "Timestamp"] else "w")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.logs_tree.yview)
        self.logs_tree.configure(yscrollcommand=scrollbar.set)
        self.logs_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_logs_data(self):
        for item in self.logs_tree.get_children():
            self.logs_tree.delete(item)
        logs = db_manager.get_audit_logs()
        for l in logs:
            self.logs_tree.insert("", "end", values=(
                l["log_id"],
                l["table_name"],
                l["action_type"],
                l["description"],
                l["created_at"]
            ))


if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
