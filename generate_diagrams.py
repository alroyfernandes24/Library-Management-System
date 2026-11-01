"""
Generate high-resolution diagram graphics for Library Management System:
- diagrams/er_diagram.png
- diagrams/architecture_diagram.png
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIAG_DIR = os.path.join(BASE_DIR, "diagrams")
os.makedirs(DIAG_DIR, exist_ok=True)


def draw_er_diagram():
    fig, ax = plt.subplots(figsize=(15, 10), dpi=300)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 10)
    ax.axis("off")
    fig.patch.set_facecolor("#f8fafc")

    # Title Banner
    ax.text(7.5, 9.6, "Library Management System — Entity-Relationship (ER) Diagram", 
            ha="center", va="center", fontsize=16, fontweight="bold", color="#0f172a")
    ax.text(7.5, 9.25, "Relational Entities, Attributes, Keys, and Cardinality Constraints (3NF Normalized)", 
            ha="center", va="center", fontsize=10.5, color="#475569")

    # Helper function to draw an entity box
    def draw_entity(x, y, w, h, title, pk_list, fk_list, attr_list, header_color="#2563eb"):
        # Outer card box
        card = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.04,rounding_size=0.15",
            edgecolor="#94a3b8", facecolor="#ffffff", linewidth=1.5
        )
        ax.add_patch(card)
        
        # Header banner
        header = patches.FancyBboxPatch(
            (x, y + h - 0.55), w, 0.55,
            boxstyle="round,pad=0.02,rounding_size=0.1",
            edgecolor=header_color, facecolor=header_color, linewidth=1
        )
        ax.add_patch(header)
        ax.text(x + w / 2, y + h - 0.28, title, ha="center", va="center", 
                fontsize=10.5, fontweight="bold", color="#ffffff")

        # Attributes text
        curr_y = y + h - 0.78
        for pk in pk_list:
            ax.text(x + 0.15, curr_y, f"[PK] {pk}", fontsize=8.5, fontweight="bold", color="#b91c1c")
            curr_y -= 0.28
        for fk in fk_list:
            ax.text(x + 0.15, curr_y, f"[FK] {fk}", fontsize=8.2, fontweight="bold", color="#2563eb")
            curr_y -= 0.28
        for att in attr_list:
            ax.text(x + 0.15, curr_y, f"- {att}", fontsize=8.0, color="#334155")
            curr_y -= 0.28

    # Helper function for relationship diamond
    def draw_rel(x, y, text, color="#059669"):
        diamond = patches.RegularPolygon(
            (x, y), numVertices=4, radius=0.45,
            orientation=0, edgecolor=color, facecolor="#ecfdf5", linewidth=1.5
        )
        ax.add_patch(diamond)
        ax.text(x, y, text, ha="center", va="center", fontsize=8.0, fontweight="bold", color=color)

    # Helper function for connector line
    def draw_line(x1, y1, x2, y2, label_start="", label_end=""):
        ax.plot([x1, x2], [y1, y2], color="#475569", lw=1.6, zorder=1)
        if label_start:
            ax.text(x1, y1 + 0.15, label_start, fontsize=8.5, fontweight="bold", color="#1e293b")
        if label_end:
            ax.text(x2, y2 + 0.15, label_end, fontsize=8.5, fontweight="bold", color="#1e293b")

    # 1. CATEGORIES (Top Left)
    draw_entity(0.6, 6.2, 2.8, 2.2, "CATEGORIES", 
                ["category_id"], [], 
                ["category_name (UK)", "description"], "#0284c7")

    # 2. AUTHORS (Bottom Left)
    draw_entity(0.6, 1.2, 2.8, 2.5, "AUTHORS", 
                ["author_id"], [], 
                ["author_name", "email", "biography"], "#0284c7")

    # 3. BOOKS (Middle Left)
    draw_entity(4.5, 4.8, 3.2, 3.8, "BOOKS", 
                ["book_id"], 
                ["category_id"], 
                ["isbn (UK)", "title", "publication_year", "total_copies", "available_copies"], 
                "#1d4ed8")

    # 4. BOOK_AUTHORS (Junction table between Books and Authors)
    draw_entity(4.5, 1.2, 3.2, 2.4, "BOOK_AUTHORS", 
                ["book_id", "author_id"], 
                ["book_id -> BOOKS", "author_id -> AUTHORS"], 
                ["(Composite PK: M:N)"], "#7c3aed")

    # 5. MEMBERS (Top Right)
    draw_entity(11.5, 5.0, 3.0, 3.6, "MEMBERS", 
                ["member_id"], [], 
                ["first_name", "last_name", "email (UK)", "phone", "membership_date", "membership_type", "status", "max_books"], 
                "#0284c7")

    # 6. BORROW_TRANSACTIONS (Middle Center)
    draw_entity(8.3, 4.8, 2.8, 3.8, "BORROW_TX", 
                ["transaction_id"], 
                ["book_id", "member_id"], 
                ["issue_date", "due_date", "return_date", "status"], 
                "#1d4ed8")

    # 7. FINES (Bottom Right)
    draw_entity(8.3, 1.0, 2.8, 2.7, "FINES", 
                ["fine_id"], 
                ["transaction_id (UK)", "member_id"], 
                ["fine_amount", "paid_status", "paid_date"], 
                "#dc2626")

    # 8. AUDIT_LOGS (Bottom Center-Right standalone)
    draw_entity(11.5, 1.0, 3.0, 2.7, "AUDIT_LOGS", 
                ["log_id"], [], 
                ["table_name", "action_type", "description", "created_at"], 
                "#475569")

    # Connectors & Cardinalities
    # Categories -> Books (1 : N)
    draw_line(3.4, 7.3, 4.0, 7.3)
    draw_rel(4.0, 7.3, "has")
    draw_line(4.0, 7.3, 4.5, 7.3, "1", "N")

    # Books -> Book_Authors (1 : N)
    draw_line(6.1, 4.8, 6.1, 3.6)
    draw_rel(6.1, 4.2, "links")
    draw_line(6.1, 4.2, 6.1, 3.6, "1", "N")

    # Authors -> Book_Authors (1 : N)
    draw_line(3.4, 2.4, 4.0, 2.4)
    draw_rel(4.0, 2.4, "writes")
    draw_line(4.0, 2.4, 4.5, 2.4, "1", "N")

    # Books -> Borrow_Transactions (1 : N)
    draw_line(7.7, 6.7, 8.0, 6.7)
    draw_rel(8.0, 6.7, "issued")
    draw_line(8.0, 6.7, 8.3, 6.7, "1", "N")

    # Members -> Borrow_Transactions (1 : N)
    draw_line(11.5, 6.7, 11.2, 6.7)
    draw_rel(11.2, 6.7, "borrows")
    draw_line(11.2, 6.7, 11.1, 6.7, "1", "N")

    # Borrow_Transactions -> Fines (1 : 0..1)
    draw_line(9.7, 4.8, 9.7, 3.7)
    draw_rel(9.7, 4.25, "incurs", color="#b91c1c")
    draw_line(9.7, 4.25, 9.7, 3.7, "1", "0..1")

    # Legend at bottom left
    leg_box = patches.FancyBboxPatch(
        (0.6, 4.0), 3.4, 1.8,
        boxstyle="round,pad=0.03,rounding_size=0.1",
        edgecolor="#cbd5e1", facecolor="#ffffff", linewidth=1.2
    )
    ax.add_patch(leg_box)
    ax.text(0.8, 5.5, "Diagram Legend", fontsize=9.5, fontweight="bold", color="#0f172a")
    ax.text(0.8, 5.15, "[PK] Primary Key    [FK] Foreign Key", fontsize=8.0, color="#1e293b")
    ax.text(0.8, 4.8, "Blue Boxes: Core Master Entities", fontsize=8.0, color="#2563eb")
    ax.text(0.8, 4.5, "Purple Box: Junction Table (M:N)", fontsize=8.0, color="#7c3aed")
    ax.text(0.8, 4.2, "Red Box: Dependent Trans. / Fines", fontsize=8.0, color="#dc2626")

    output_path = os.path.join(DIAG_DIR, "er_diagram.png")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[+] ER Diagram generated: {output_path}")


def draw_architecture_diagram():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")
    fig.patch.set_facecolor("#f8fafc")

    # Title
    ax.text(7.0, 7.6, "Library Management System -- 3-Tier System Architecture", 
            ha="center", va="center", fontsize=16, fontweight="bold", color="#0f172a")
    ax.text(7.0, 7.25, "Layered Design: Presentation, Application/REST Engine, and Relational Database", 
            ha="center", va="center", fontsize=10.5, color="#475569")

    # Layer 1: Presentation Layer
    layer1 = patches.FancyBboxPatch(
        (0.8, 4.8), 12.4, 1.8,
        boxstyle="round,pad=0.04,rounding_size=0.15",
        edgecolor="#3b82f6", facecolor="#eff6ff", linewidth=1.5
    )
    ax.add_patch(layer1)
    ax.text(1.2, 6.3, "TIER 1: PRESENTATION LAYER (USER INTERFACES)", fontsize=11, fontweight="bold", color="#1d4ed8")
    
    # Subcards in Tier 1
    ui1 = patches.FancyBboxPatch(
        (1.2, 5.0), 5.6, 1.0,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        edgecolor="#93c5fd", facecolor="#ffffff", linewidth=1.2
    )
    ax.add_patch(ui1)
    ax.text(4.0, 5.65, "[Desktop GUI] Python Tkinter Interface", ha="center", fontsize=10, fontweight="bold", color="#1e3a8a")
    ax.text(4.0, 5.25, "Tabbed catalog, quick author add, fine collection dialogs", ha="center", fontsize=8.0, color="#475569")

    ui2 = patches.FancyBboxPatch(
        (7.2, 5.0), 5.6, 1.0,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        edgecolor="#93c5fd", facecolor="#ffffff", linewidth=1.2
    )
    ax.add_patch(ui2)
    ax.text(10.0, 5.65, "[Web Application] HTML5, Bootstrap 5, REST Client", ha="center", fontsize=10, fontweight="bold", color="#1e3a8a")
    ax.text(10.0, 5.25, "Dynamic dashboard, interactive modals, live search filter", ha="center", fontsize=8.0, color="#475569")

    # Layer 2: Application / Controller Layer
    layer2 = patches.FancyBboxPatch(
        (0.8, 2.6), 12.4, 1.7,
        boxstyle="round,pad=0.04,rounding_size=0.15",
        edgecolor="#6366f1", facecolor="#eef2ff", linewidth=1.5
    )
    ax.add_patch(layer2)
    ax.text(1.2, 4.0, "TIER 2: APPLICATION & BUSINESS LOGIC LAYER", fontsize=11, fontweight="bold", color="#4338ca")

    app1 = patches.FancyBboxPatch(
        (1.2, 2.8), 3.6, 0.9,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        edgecolor="#c7d2fe", facecolor="#ffffff", linewidth=1.2
    )
    ax.add_patch(app1)
    ax.text(3.0, 3.35, "HTTP / REST Server", ha="center", fontsize=9.5, fontweight="bold", color="#312e81")
    ax.text(3.0, 3.0, "JSON endpoints, CORS handler", ha="center", fontsize=8.0, color="#475569")

    app2 = patches.FancyBboxPatch(
        (5.2, 2.8), 3.6, 0.9,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        edgecolor="#c7d2fe", facecolor="#ffffff", linewidth=1.2
    )
    ax.add_patch(app2)
    ax.text(7.0, 3.35, "Business Rules & Validation", ha="center", fontsize=9.5, fontweight="bold", color="#312e81")
    ax.text(7.0, 3.0, "Borrowing quotas, stock checks", ha="center", fontsize=8.0, color="#475569")

    app3 = patches.FancyBboxPatch(
        (9.2, 2.8), 3.6, 0.9,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        edgecolor="#c7d2fe", facecolor="#ffffff", linewidth=1.2
    )
    ax.add_patch(app3)
    ax.text(11.0, 3.35, "DB Manager Interface", ha="center", fontsize=9.5, fontweight="bold", color="#312e81")
    ax.text(11.0, 3.0, "sqlite3 / psycopg connector", ha="center", fontsize=8.0, color="#475569")

    # Layer 3: Database Engine Layer
    layer3 = patches.FancyBboxPatch(
        (0.8, 0.4), 12.4, 1.7,
        boxstyle="round,pad=0.04,rounding_size=0.15",
        edgecolor="#059669", facecolor="#ecfdf5", linewidth=1.5
    )
    ax.add_patch(layer3)
    ax.text(1.2, 1.8, "TIER 3: RELATIONAL DATABASE MANAGEMENT SYSTEM (DBMS)", fontsize=11, fontweight="bold", color="#065f46")

    db1 = patches.FancyBboxPatch(
        (1.2, 0.6), 3.6, 0.9,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        edgecolor="#a7f3d0", facecolor="#ffffff", linewidth=1.2
    )
    ax.add_patch(db1)
    ax.text(3.0, 1.15, "Normalized Schema (3NF)", ha="center", fontsize=9.5, fontweight="bold", color="#064e3b")
    ax.text(3.0, 0.8, "8 Tables, PK, FK, Constraints", ha="center", fontsize=8.0, color="#475569")

    db2 = patches.FancyBboxPatch(
        (5.2, 0.6), 3.6, 0.9,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        edgecolor="#a7f3d0", facecolor="#ffffff", linewidth=1.2
    )
    ax.add_patch(db2)
    ax.text(7.0, 1.15, "Database Triggers", ha="center", fontsize=9.5, fontweight="bold", color="#064e3b")
    ax.text(7.0, 0.8, "Auto stock dec/inc, fine calc Rs 5/d", ha="center", fontsize=8.0, color="#475569")

    db3 = patches.FancyBboxPatch(
        (9.2, 0.6), 3.6, 0.9,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        edgecolor="#a7f3d0", facecolor="#ffffff", linewidth=1.2
    )
    ax.add_patch(db3)
    ax.text(11.0, 1.15, "Analytical Views & Audit", ha="center", fontsize=9.5, fontweight="bold", color="#064e3b")
    ax.text(11.0, 0.8, "vw_catalog, vw_active_loans, logs", ha="center", fontsize=8.0, color="#475569")

    # Arrows between layers
    arrow_props = dict(facecolor="#475569", edgecolor="#334155", width=1.5, headwidth=8, headlength=8)
    ax.annotate("", xy=(7.0, 4.3), xytext=(7.0, 4.8), arrowprops=arrow_props)
    ax.annotate("", xy=(7.0, 4.8), xytext=(7.0, 4.3), arrowprops=arrow_props)

    ax.annotate("", xy=(7.0, 2.1), xytext=(7.0, 2.6), arrowprops=arrow_props)
    ax.annotate("", xy=(7.0, 2.6), xytext=(7.0, 2.1), arrowprops=arrow_props)

    output_path = os.path.join(DIAG_DIR, "architecture_diagram.png")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[+] Architecture Diagram generated: {output_path}")


if __name__ == "__main__":
    draw_er_diagram()
    draw_architecture_diagram()
