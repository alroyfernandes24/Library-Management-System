"""
Generate a professional, publication-quality Chen-style ER Diagram image
for the Library Management System, matching academic textbook standards.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIAG_DIR = os.path.join(BASE_DIR, "diagrams")
os.makedirs(DIAG_DIR, exist_ok=True)
OUTPUT_IMG = os.path.join(DIAG_DIR, "er_diagram.png")


def create_er_diagram():
    fig, ax = plt.subplots(figsize=(20, 13.5), dpi=300)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 13.5)
    ax.axis("off")
    fig.patch.set_facecolor("#f8fafc")

    # Title Banner (matches Eyewear Store reference)
    banner_box = patches.FancyBboxPatch(
        (5.5, 12.2), 9.0, 0.95,
        boxstyle="round,pad=0.08,rounding_size=0.3",
        edgecolor="#2563eb", facecolor="#dbeafe", linewidth=2.0
    )
    ax.add_patch(banner_box)
    ax.text(10.0, 12.8, "Library Management System", ha="center", va="center",
            fontsize=18, fontweight="bold", color="#1e3a8a", fontfamily="sans-serif")
    ax.text(10.0, 12.45, "Entity-Relationship (ER) Diagram", ha="center", va="center",
            fontsize=14, fontweight="bold", color="#2563eb", fontfamily="sans-serif")

    # Colors
    ENTITY_COLORS = {
        "Book": {"fill": "#bfdbfe", "edge": "#1d4ed8", "text": "#1e3a8a"},       # Light blue
        "Member": {"fill": "#bbf7d0", "edge": "#15803d", "text": "#14532d"},     # Light green
        "Author": {"fill": "#fed7aa", "edge": "#c2410c", "text": "#7c2d12"},     # Light peach
        "Category": {"fill": "#ddd6fe", "edge": "#6d28d9", "text": "#4c1d95"},   # Light purple
        "Borrow": {"fill": "#fbcfe8", "edge": "#be185d", "text": "#831843"},     # Light pink
        "Fine": {"fill": "#fecdd3", "edge": "#b91c1c", "text": "#881337"},       # Light rose
        "Audit": {"fill": "#e2e8f0", "edge": "#475569", "text": "#0f172a"}       # Light slate
    }

    REL_COLOR = {"fill": "#ffedd5", "edge": "#ea580c", "text": "#9a3412"}       # Diamond peach
    ATTR_COLOR = {"fill": "#ffffff", "edge": "#64748b", "text": "#0f172a"}
    PK_ATTR_COLOR = {"fill": "#eff6ff", "edge": "#2563eb", "text": "#1e40af"}

    # Helper: Draw Line
    def draw_line(x1, y1, x2, y2, color="#475569", lw=1.6, zorder=1):
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw, zorder=zorder)

    # Helper: Draw Entity
    def draw_entity(x, y, w, h, name, key):
        c = ENTITY_COLORS[key]
        box = patches.FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle="square,pad=0",
            edgecolor=c["edge"], facecolor=c["fill"], linewidth=2.2, zorder=3
        )
        ax.add_patch(box)
        ax.text(x, y, name, ha="center", va="center",
                fontsize=13, fontweight="bold", color=c["text"], zorder=4)

    # Helper: Draw Relationship Diamond
    def draw_relationship(x, y, w, h, name):
        poly = patches.Polygon(
            [[x, y + h/2], [x + w/2, y], [x, y - h/2], [x - w/2, y]],
            edgecolor=REL_COLOR["edge"], facecolor=REL_COLOR["fill"], linewidth=2.0, zorder=3
        )
        ax.add_patch(poly)
        ax.text(x, y, name, ha="center", va="center",
                fontsize=10.5, fontweight="bold", color=REL_COLOR["text"], zorder=4)

    # Helper: Draw Attribute Ellipse
    def draw_attribute(x, y, text, is_pk=False, parent_x=0, parent_y=0, w=1.5, h=0.55):
        # Draw connector line first
        if parent_x != 0 and parent_y != 0:
            draw_line(x, y, parent_x, parent_y, color="#94a3b8", lw=1.2, zorder=1)

        c = PK_ATTR_COLOR if is_pk else ATTR_COLOR
        ellipse = patches.Ellipse(
            (x, y), width=w, height=h,
            edgecolor=c["edge"], facecolor=c["fill"], linewidth=1.8 if is_pk else 1.2, zorder=2
        )
        ax.add_patch(ellipse)

        # Text inside attribute
        display_text = text
        ax.text(x, y, display_text, ha="center", va="center",
                fontsize=8.5, fontweight="bold" if is_pk else "normal",
                color=c["text"], zorder=4)
        if is_pk:
            # Underline for PK
            text_len = len(text) * 0.05
            ax.plot([x - text_len, x + text_len], [y - 0.12, y - 0.12], color=c["edge"], lw=1.4, zorder=5)

    # =========================================================================
    # 1. ENTITY COORDINATES (Centered, well-spaced)
    # =========================================================================
    # Category: (3.2, 9.8)
    # Book: (7.8, 6.8)
    # Author: (3.0, 3.8)
    # Member: (15.5, 9.8)
    # BorrowTransaction: (13.0, 5.8)
    # Fine: (17.2, 3.2)
    # AuditLog: (7.8, 1.6)

    # Draw Entities
    draw_entity(3.2, 9.8, 2.4, 1.1, "Category", "Category")
    draw_entity(7.8, 6.8, 2.4, 1.1, "Book", "Book")
    draw_entity(3.0, 3.8, 2.4, 1.1, "Author", "Author")
    draw_entity(15.5, 9.8, 2.5, 1.1, "Member", "Member")
    draw_entity(12.8, 5.8, 2.6, 1.1, "BorrowTransaction", "Borrow")
    draw_entity(17.2, 3.2, 2.2, 1.1, "Fine", "Fine")
    draw_entity(7.8, 1.6, 2.4, 1.1, "AuditLog", "Audit")

    # =========================================================================
    # 2. RELATIONSHIPS (Diamonds) & CONNECTORS
    # =========================================================================

    # --- Rel 1: Category - Book (BelongsTo, 1:N) ---
    draw_relationship(5.5, 8.3, 1.8, 1.0, "BelongsTo")
    draw_line(3.2, 9.25, 5.5, 8.8, lw=1.8)
    draw_line(5.5, 7.8, 7.8, 7.35, lw=1.8)
    ax.text(3.7, 9.2, "1", fontsize=11, fontweight="bold", color="#1e3a8a")
    ax.text(7.2, 7.5, "N", fontsize=11, fontweight="bold", color="#1e3a8a")

    # --- Rel 2: Book - Author (WrittenBy, M:N) ---
    draw_relationship(5.4, 5.3, 1.8, 1.0, "WrittenBy")
    draw_line(7.0, 6.35, 5.4, 5.8, lw=1.8)
    draw_line(5.4, 4.8, 3.0, 4.35, lw=1.8)
    ax.text(6.8, 6.0, "M", fontsize=11, fontweight="bold", color="#1e3a8a")
    ax.text(3.6, 4.6, "N", fontsize=11, fontweight="bold", color="#1e3a8a")

    # --- Rel 3: Book - BorrowTransaction (IssuedIn, 1:N) ---
    draw_relationship(10.3, 6.3, 1.8, 1.0, "IssuedIn")
    draw_line(9.0, 6.8, 9.4, 6.3, lw=1.8)
    draw_line(11.2, 6.3, 11.5, 5.8, lw=1.8)
    ax.text(9.2, 6.7, "1", fontsize=11, fontweight="bold", color="#1e3a8a")
    ax.text(11.3, 5.9, "N", fontsize=11, fontweight="bold", color="#1e3a8a")

    # --- Rel 4: Member - BorrowTransaction (Borrows, 1:N) ---
    draw_relationship(14.2, 7.8, 1.8, 1.0, "Borrows")
    draw_line(15.5, 9.25, 14.2, 8.3, lw=1.8)
    draw_line(14.2, 7.3, 13.3, 6.35, lw=1.8)
    ax.text(15.3, 8.9, "1", fontsize=11, fontweight="bold", color="#1e3a8a")
    ax.text(13.6, 6.7, "N", fontsize=11, fontweight="bold", color="#1e3a8a")

    # --- Rel 5: BorrowTransaction - Fine (Incurs, 1:0..1) ---
    draw_relationship(15.2, 4.5, 1.8, 1.0, "Incurs")
    draw_line(13.8, 5.25, 14.5, 4.8, lw=1.8)
    draw_line(15.9, 4.2, 16.5, 3.75, lw=1.8)
    ax.text(14.0, 5.2, "1", fontsize=11, fontweight="bold", color="#1e3a8a")
    ax.text(15.9, 4.2, "0..1", fontsize=11, fontweight="bold", color="#1e3a8a")

    # --- Rel 6: System/Audit Trigger Link (MonitoredBy) ---
    draw_relationship(7.8, 3.8, 2.0, 1.0, "AuditedIn")
    draw_line(7.8, 6.25, 7.8, 4.3, lw=1.4, color="#94a3b8")
    draw_line(7.8, 3.3, 7.8, 2.15, lw=1.4, color="#94a3b8")
    ax.text(8.0, 5.4, "1", fontsize=10, fontweight="bold", color="#64748b")
    ax.text(8.0, 2.6, "N", fontsize=10, fontweight="bold", color="#64748b")

    # =========================================================================
    # 3. ATTRIBUTES (Ellipses attached to each entity)
    # =========================================================================

    # --- Attributes of CATEGORY (around 3.2, 9.8) ---
    draw_attribute(1.5, 11.2, "CategoryID", is_pk=True, parent_x=3.2, parent_y=9.8, w=1.5, h=0.55)
    draw_attribute(3.2, 11.4, "CategoryName", is_pk=False, parent_x=3.2, parent_y=9.8, w=1.65, h=0.55)
    draw_attribute(1.2, 9.8, "Description", is_pk=False, parent_x=3.2, parent_y=9.8, w=1.5, h=0.55)

    # --- Attributes of AUTHOR (around 3.0, 3.8) ---
    draw_attribute(1.1, 4.8, "AuthorID", is_pk=True, parent_x=3.0, parent_y=3.8, w=1.4, h=0.55)
    draw_attribute(1.0, 3.8, "AuthorName", is_pk=False, parent_x=3.0, parent_y=3.8, w=1.55, h=0.55)
    draw_attribute(1.1, 2.8, "Email", is_pk=False, parent_x=3.0, parent_y=3.8, w=1.2, h=0.55)
    draw_attribute(3.0, 2.4, "Biography", is_pk=False, parent_x=3.0, parent_y=3.8, w=1.4, h=0.55)

    # --- Attributes of BOOK (around 7.8, 6.8) ---
    draw_attribute(7.0, 8.4, "BookID", is_pk=True, parent_x=7.8, parent_y=6.8, w=1.3, h=0.55)
    draw_attribute(8.8, 8.4, "ISBN", is_pk=False, parent_x=7.8, parent_y=6.8, w=1.2, h=0.55)
    draw_attribute(10.2, 7.6, "Title", is_pk=False, parent_x=7.8, parent_y=6.8, w=1.2, h=0.55)
    draw_attribute(6.0, 6.8, "PubYear", is_pk=False, parent_x=7.8, parent_y=6.8, w=1.3, h=0.55)
    draw_attribute(6.5, 5.5, "TotalCopies", is_pk=False, parent_x=7.8, parent_y=6.8, w=1.5, h=0.55)
    draw_attribute(9.0, 5.2, "AvailableCopies", is_pk=False, parent_x=7.8, parent_y=6.8, w=1.75, h=0.55)

    # --- Attributes of MEMBER (around 15.5, 9.8) ---
    draw_attribute(13.5, 11.5, "MemberID", is_pk=True, parent_x=15.5, parent_y=9.8, w=1.5, h=0.55)
    draw_attribute(15.5, 11.7, "FirstName", is_pk=False, parent_x=15.5, parent_y=9.8, w=1.45, h=0.55)
    draw_attribute(17.4, 11.5, "LastName", is_pk=False, parent_x=15.5, parent_y=9.8, w=1.45, h=0.55)
    draw_attribute(18.8, 10.5, "Email", is_pk=False, parent_x=15.5, parent_y=9.8, w=1.25, h=0.55)
    draw_attribute(18.9, 9.5, "Phone", is_pk=False, parent_x=15.5, parent_y=9.8, w=1.25, h=0.55)
    draw_attribute(18.8, 8.5, "MemberDate", is_pk=False, parent_x=15.5, parent_y=9.8, w=1.6, h=0.55)
    draw_attribute(17.5, 7.7, "MemberType", is_pk=False, parent_x=15.5, parent_y=9.8, w=1.6, h=0.55)
    draw_attribute(16.0, 7.5, "Status", is_pk=False, parent_x=15.5, parent_y=9.8, w=1.2, h=0.55)
    draw_attribute(14.2, 9.8, "MaxBooks", is_pk=False, parent_x=15.5, parent_y=9.8, w=1.4, h=0.55)

    # --- Attributes of BORROWTRANSACTION (around 12.8, 5.8) ---
    draw_attribute(11.2, 4.6, "TransactionID", is_pk=True, parent_x=12.8, parent_y=5.8, w=1.75, h=0.55)
    draw_attribute(12.8, 4.3, "IssueDate", is_pk=False, parent_x=12.8, parent_y=5.8, w=1.4, h=0.55)
    draw_attribute(14.0, 3.8, "DueDate", is_pk=False, parent_x=12.8, parent_y=5.8, w=1.35, h=0.55)
    draw_attribute(14.8, 5.2, "ReturnDate", is_pk=False, parent_x=12.8, parent_y=5.8, w=1.5, h=0.55)
    draw_attribute(11.8, 7.0, "Status", is_pk=False, parent_x=12.8, parent_y=5.8, w=1.2, h=0.55)

    # --- Attributes of FINE (around 17.2, 3.2) ---
    draw_attribute(16.0, 1.8, "FineID", is_pk=True, parent_x=17.2, parent_y=3.2, w=1.3, h=0.55)
    draw_attribute(17.7, 1.7, "FineAmount", is_pk=False, parent_x=17.2, parent_y=3.2, w=1.55, h=0.55)
    draw_attribute(19.0, 2.4, "PaidStatus", is_pk=False, parent_x=17.2, parent_y=3.2, w=1.45, h=0.55)
    draw_attribute(19.0, 3.6, "PaidDate", is_pk=False, parent_x=17.2, parent_y=3.2, w=1.4, h=0.55)

    # --- Attributes of AUDITLOG (around 7.8, 1.6) ---
    draw_attribute(5.7, 2.2, "LogID", is_pk=True, parent_x=7.8, parent_y=1.6, w=1.2, h=0.55)
    draw_attribute(5.7, 1.2, "TableName", is_pk=False, parent_x=7.8, parent_y=1.6, w=1.5, h=0.55)
    draw_attribute(7.8, 0.5, "ActionType", is_pk=False, parent_x=7.8, parent_y=1.6, w=1.45, h=0.55)
    draw_attribute(9.8, 0.7, "Description", is_pk=False, parent_x=7.8, parent_y=1.6, w=1.5, h=0.55)
    draw_attribute(10.0, 1.7, "CreatedAt", is_pk=False, parent_x=7.8, parent_y=1.6, w=1.4, h=0.55)

    # =========================================================================
    # 4. DIAGRAM LEGEND (Bottom-Left)
    # =========================================================================
    leg_x, leg_y, leg_w, leg_h = 0.6, 0.5, 4.4, 2.1
    leg_box = patches.FancyBboxPatch(
        (leg_x, leg_y), leg_w, leg_h,
        boxstyle="round,pad=0.05,rounding_size=0.15",
        edgecolor="#cbd5e1", facecolor="#ffffff", linewidth=1.4, zorder=10
    )
    ax.add_patch(leg_box)

    ax.text(leg_x + 0.25, leg_y + leg_h - 0.28, "Legend / ER Notation",
            fontsize=11, fontweight="bold", color="#0f172a", zorder=11)

    # Entity sample
    ent_sample = patches.Rectangle((leg_x + 0.25, leg_y + 1.2), 0.8, 0.35,
                                   edgecolor="#1d4ed8", facecolor="#bfdbfe", linewidth=1.4, zorder=11)
    ax.add_patch(ent_sample)
    ax.text(leg_x + 1.15, leg_y + 1.37, "Entity", fontsize=9.5, fontweight="bold", color="#1e293b", zorder=11)

    # Relationship sample
    rel_sample = patches.Polygon(
        [[leg_x + 2.5, leg_y + 1.55], [leg_x + 2.9, leg_y + 1.37], [leg_x + 2.5, leg_y + 1.2], [leg_x + 2.1, leg_y + 1.37]],
        edgecolor=REL_COLOR["edge"], facecolor=REL_COLOR["fill"], linewidth=1.4, zorder=11
    )
    ax.add_patch(rel_sample)
    ax.text(leg_x + 3.05, leg_y + 1.37, "Relationship", fontsize=9.5, fontweight="bold", color="#1e293b", zorder=11)

    # Attribute sample
    attr_sample = patches.Ellipse((leg_x + 0.65, leg_y + 0.75), width=0.8, height=0.35,
                                  edgecolor="#64748b", facecolor="#ffffff", linewidth=1.2, zorder=11)
    ax.add_patch(attr_sample)
    ax.text(leg_x + 1.15, leg_y + 0.75, "Attribute", fontsize=9.5, color="#1e293b", zorder=11)

    # PK Attribute sample
    pk_sample = patches.Ellipse((leg_x + 2.5, leg_y + 0.75), width=0.8, height=0.35,
                                edgecolor="#2563eb", facecolor="#eff6ff", linewidth=1.5, zorder=11)
    ax.add_patch(pk_sample)
    ax.text(leg_x + 3.05, leg_y + 0.75, "Key (PK)", fontsize=9.5, fontweight="bold", color="#1e40af", zorder=11)

    # Cardinality note
    ax.text(leg_x + 0.25, leg_y + 0.25, "1, N, M : Cardinality Ratio", fontsize=9, color="#475569", zorder=11)
    ax.text(leg_x + 2.3, leg_y + 0.25, "0..1 : Optional Participation", fontsize=9, color="#475569", zorder=11)

    plt.tight_layout()
    plt.savefig(OUTPUT_IMG, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[+] High-resolution Chen ER Diagram generated: {OUTPUT_IMG}")


if __name__ == "__main__":
    create_er_diagram()
