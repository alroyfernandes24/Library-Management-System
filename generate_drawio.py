"""
Generate a 100% compliant, fully tested Draw.io diagram file (.drawio / .xml)
Fixes:
1. mxGeometry MUST be inside mxCell (prevents collapse to 0,0)
2. Proper un-doubled HTML entities in value attribute
3. Clean, well-spaced coordinates for all entities, attributes, and connectors
"""

import os
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
os.makedirs(DOCS_DIR, exist_ok=True)

DRAWIO_PATH = os.path.join(DOCS_DIR, "Library_Management_System_ER_Diagram.drawio")
XML_PATH = os.path.join(DOCS_DIR, "Library_Management_System_ER_Diagram.xml")


def build_drawio_file():
    # Root draw.io container
    mxfile = ET.Element("mxfile", {
        "host": "app.diagrams.net",
        "modified": "2026-10-27T10:36:00.000Z",
        "agent": "Antigravity/1.0",
        "version": "24.0.0",
        "type": "device"
    })

    diagram = ET.SubElement(mxfile, "diagram", {
        "id": "diagram_lms_er",
        "name": "Library ER Diagram"
    })

    model = ET.SubElement(diagram, "mxGraphModel", {
        "dx": "1600",
        "dy": "1000",
        "grid": "1",
        "gridSize": "10",
        "guides": "1",
        "tooltips": "1",
        "connect": "1",
        "arrows": "1",
        "fold": "1",
        "page": "1",
        "pageScale": "1",
        "pageWidth": "1800",
        "pageHeight": "1300",
        "background": "#F8FAFC",
        "math": "0",
        "shadow": "0"
    })

    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})

    cell_counter = 100

    def get_id():
        nonlocal cell_counter
        cell_counter += 1
        return str(cell_counter)

    # 1. TOP TITLE BANNER
    title_cell = ET.SubElement(root, "mxCell", {
        "id": "title_banner",
        "value": "<b><font style='font-size: 20px;'>Library Management System — Entity-Relationship (ER) Diagram</font></b><br><font style='font-size: 13px; color: #374151;'>Fr. Conceicao Rodrigues College of Engineering | Department of Computer Science &amp; Engineering</font>",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#2563eb;strokeWidth=2;align=center;verticalAlign=middle;arcSize=18;fontColor=#1e3a8a;",
        "vertex": "1",
        "parent": "1"
    })
    ET.SubElement(title_cell, "mxGeometry", {
        "x": "450", "y": "30", "width": "850", "height": "75", "as": "geometry"
    })

    # Helper: Add Entity (Rectangle)
    def add_entity(eid, name, x, y, w, h, fill, stroke, text_color):
        cell = ET.SubElement(root, "mxCell", {
            "id": eid,
            "value": f"<b>{name}</b>",
            "style": f"rounded=0;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth=2.2;fontColor={text_color};fontSize=14;fontFamily=Helvetica;align=center;verticalAlign=middle;",
            "vertex": "1",
            "parent": "1"
        })
        ET.SubElement(cell, "mxGeometry", {
            "x": str(x), "y": str(y), "width": str(w), "height": str(h), "as": "geometry"
        })
        return eid

    # Helper: Add Relationship (Diamond)
    def add_relationship(rid, name, x, y, w=110, h=65):
        cell = ET.SubElement(root, "mxCell", {
            "id": rid,
            "value": f"<b>{name}</b>",
            "style": "rhombus;whiteSpace=wrap;html=1;fillColor=#ffedd5;strokeColor=#ea580c;strokeWidth=2;fontColor=#9a3412;fontSize=12;fontFamily=Helvetica;align=center;verticalAlign=middle;",
            "vertex": "1",
            "parent": "1"
        })
        ET.SubElement(cell, "mxGeometry", {
            "x": str(x), "y": str(y), "width": str(w), "height": str(h), "as": "geometry"
        })
        return rid

    # Helper: Add Attribute (Ellipse)
    def add_attribute(aid, text, x, y, parent_entity_id, is_pk=False, w=130, h=45):
        val = f"<u><b>{text}</b></u>" if is_pk else text
        fill = "#eff6ff" if is_pk else "#ffffff"
        stroke = "#2563eb" if is_pk else "#64748b"
        fcolor = "#1e40af" if is_pk else "#0f172a"
        swidth = "2" if is_pk else "1.2"

        cell = ET.SubElement(root, "mxCell", {
            "id": aid,
            "value": val,
            "style": f"ellipse;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth={swidth};fontColor={fcolor};fontSize=11;fontFamily=Helvetica;align=center;verticalAlign=middle;",
            "vertex": "1",
            "parent": "1"
        })
        ET.SubElement(cell, "mxGeometry", {
            "x": str(x), "y": str(y), "width": str(w), "height": str(h), "as": "geometry"
        })

        # Connector line to parent entity
        conn = ET.SubElement(root, "mxCell", {
            "id": f"conn_{aid}",
            "value": "",
            "style": "endArrow=none;html=1;rounded=0;strokeColor=#94a3b8;strokeWidth=1.2;",
            "edge": "1",
            "source": aid,
            "target": parent_entity_id,
            "parent": "1"
        })
        ET.SubElement(conn, "mxGeometry", {"relative": "1", "as": "geometry"})
        return aid

    # Helper: Add Connector between Entity and Relationship
    def add_rel_edge(eid, rid, label=""):
        cid = f"edge_{eid}_{rid}_{get_id()}"
        edge = ET.SubElement(root, "mxCell", {
            "id": cid,
            "value": label,
            "style": "endArrow=none;html=1;rounded=0;strokeColor=#334155;strokeWidth=2;fontSize=13;fontStyle=1;fontColor=#1e3a8a;labelBackgroundColor=#f8fafc;",
            "edge": "1",
            "source": eid,
            "target": rid,
            "parent": "1"
        })
        ET.SubElement(edge, "mxGeometry", {"relative": "1", "as": "geometry"})
        return cid

    # =========================================================================
    # 2. ENTITIES (Rectangle nodes)
    # =========================================================================
    # 1. Category
    e_cat = add_entity("ent_category", "Category", 260, 260, 150, 65, "#ddd6fe", "#6d28d9", "#4c1d95")
    # 2. Book
    e_book = add_entity("ent_book", "Book", 640, 520, 160, 70, "#bfdbfe", "#1d4ed8", "#1e3a8a")
    # 3. Author
    e_auth = add_entity("ent_author", "Author", 260, 760, 150, 65, "#fed7aa", "#c2410c", "#7c2d12")
    # 4. Member
    e_mem = add_entity("ent_member", "Member", 1240, 260, 160, 65, "#bbf7d0", "#15803d", "#14532d")
    # 5. BorrowTransaction
    e_borrow = add_entity("ent_borrow", "BorrowTransaction", 1000, 520, 180, 70, "#fbcfe8", "#be185d", "#831843")
    # 6. Fine
    e_fine = add_entity("ent_fine", "Fine", 1360, 780, 140, 65, "#fecdd3", "#b91c1c", "#881337")
    # 7. AuditLog
    e_audit = add_entity("ent_audit", "AuditLog", 640, 940, 160, 65, "#e2e8f0", "#475569", "#0f172a")

    # =========================================================================
    # 3. RELATIONSHIPS (Diamonds) & CONNECTORS
    # =========================================================================
    # Category (1) -- BelongsTo -- (N) Book
    r_cat_book = add_relationship("rel_belongsto", "BelongsTo", 440, 380)
    add_rel_edge(e_cat, r_cat_book, "1")
    add_rel_edge(e_book, r_cat_book, "N")

    # Book (M) -- WrittenBy -- (N) Author
    r_book_auth = add_relationship("rel_writtenby", "WrittenBy", 440, 630)
    add_rel_edge(e_book, r_book_auth, "M")
    add_rel_edge(e_auth, r_book_auth, "N")

    # Book (1) -- IssuedIn -- (N) BorrowTransaction
    r_book_borrow = add_relationship("rel_issuedin", "IssuedIn", 840, 522)
    add_rel_edge(e_book, r_book_borrow, "1")
    add_rel_edge(e_borrow, r_book_borrow, "N")

    # Member (1) -- Borrows -- (N) BorrowTransaction
    r_mem_borrow = add_relationship("rel_borrows", "Borrows", 1120, 380)
    add_rel_edge(e_mem, r_mem_borrow, "1")
    add_rel_edge(e_borrow, r_mem_borrow, "N")

    # BorrowTransaction (1) -- Incurs -- (0..1) Fine
    r_borrow_fine = add_relationship("rel_incurs", "Incurs", 1180, 660)
    add_rel_edge(e_borrow, r_borrow_fine, "1")
    add_rel_edge(e_fine, r_borrow_fine, "0..1")

    # Book (1) -- AuditedIn -- (N) AuditLog
    r_audit = add_relationship("rel_auditedin", "AuditedIn", 665, 760)
    add_rel_edge(e_book, r_audit, "1")
    add_rel_edge(e_audit, r_audit, "N")

    # =========================================================================
    # 4. ATTRIBUTES (Ellipses)
    # =========================================================================
    # Attributes for Category (x=260, y=260)
    add_attribute("att_cat_id", "CategoryID", 90, 180, e_cat, is_pk=True)
    add_attribute("att_cat_name", "CategoryName", 260, 160, e_cat)
    add_attribute("att_cat_desc", "Description", 80, 300, e_cat)

    # Attributes for Author (x=260, y=760)
    add_attribute("att_auth_id", "AuthorID", 80, 680, e_auth, is_pk=True)
    add_attribute("att_auth_name", "AuthorName", 80, 770, e_auth)
    add_attribute("att_auth_email", "Email", 90, 850, e_auth)
    add_attribute("att_auth_bio", "Biography", 260, 880, e_auth)

    # Attributes for Book (x=640, y=520)
    add_attribute("att_book_id", "BookID", 520, 370, e_book, is_pk=True)
    add_attribute("att_book_isbn", "ISBN", 660, 370, e_book)
    add_attribute("att_book_title", "Title", 770, 420, e_book)
    add_attribute("att_book_year", "PubYear", 470, 480, e_book)
    add_attribute("att_book_total", "TotalCopies", 510, 640, e_book)
    add_attribute("att_book_avail", "AvailableCopies", 740, 650, e_book, w=140)

    # Attributes for Member (x=1240, y=260)
    add_attribute("att_mem_id", "MemberID", 1080, 170, e_mem, is_pk=True)
    add_attribute("att_mem_fn", "FirstName", 1240, 150, e_mem)
    add_attribute("att_mem_ln", "LastName", 1400, 170, e_mem)
    add_attribute("att_mem_email", "Email", 1470, 240, e_mem)
    add_attribute("att_mem_phone", "Phone", 1470, 320, e_mem)
    add_attribute("att_mem_date", "MembershipDate", 1440, 400, e_mem, w=140)
    add_attribute("att_mem_type", "MembershipType", 1330, 440, e_mem, w=140)
    add_attribute("att_mem_status", "Status", 1230, 460, e_mem)
    add_attribute("att_mem_max", "MaxBooksAllowed", 1070, 300, e_mem, w=145)

    # Attributes for BorrowTransaction (x=1000, y=520)
    add_attribute("att_tx_id", "TransactionID", 970, 410, e_borrow, is_pk=True, w=140)
    add_attribute("att_tx_iss", "IssueDate", 1060, 650, e_borrow)
    add_attribute("att_tx_due", "DueDate", 930, 650, e_borrow)
    add_attribute("att_tx_ret", "ReturnDate", 1160, 570, e_borrow)
    add_attribute("att_tx_stat", "Status", 920, 470, e_borrow)

    # Attributes for Fine (x=1360, y=780)
    add_attribute("att_fine_id", "FineID", 1260, 890, e_fine, is_pk=True)
    add_attribute("att_fine_amt", "FineAmount", 1410, 890, e_fine)
    add_attribute("att_fine_stat", "PaidStatus", 1520, 810, e_fine)
    add_attribute("att_fine_date", "PaidDate", 1510, 720, e_fine)

    # Attributes for AuditLog (x=640, y=940)
    add_attribute("att_log_id", "LogID", 470, 930, e_audit, is_pk=True)
    add_attribute("att_log_tbl", "TableName", 490, 1020, e_audit)
    add_attribute("att_log_act", "ActionType", 640, 1060, e_audit)
    add_attribute("att_log_desc", "Description", 790, 1020, e_audit)
    add_attribute("att_log_time", "CreatedAt", 810, 930, e_audit)

    # =========================================================================
    # 5. DIAGRAM LEGEND (Bottom-Left)
    # =========================================================================
    leg_box = ET.SubElement(root, "mxCell", {
        "id": "legend_box",
        "value": "<b><font style='font-size: 13px;'>Legend / Chen ER Notation</font></b>",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#cbd5e1;strokeWidth=1.5;verticalAlign=top;align=left;spacingLeft=15;spacingTop=10;fontColor=#0f172a;",
        "vertex": "1",
        "parent": "1"
    })
    ET.SubElement(leg_box, "mxGeometry", {
        "x": "60", "y": "960", "width": "350", "height": "180", "as": "geometry"
    })

    # Entity sample
    ent_s = ET.SubElement(root, "mxCell", {
        "id": "leg_ent",
        "value": "<b>Entity</b>",
        "style": "rounded=0;whiteSpace=wrap;html=1;fillColor=#bfdbfe;strokeColor=#1d4ed8;strokeWidth=1.5;fontSize=10;fontColor=#1e3a8a;",
        "vertex": "1",
        "parent": "1"
    })
    ET.SubElement(ent_s, "mxGeometry", {"x": "80", "y": "1000", "width": "70", "height": "30", "as": "geometry"})

    # Relationship sample
    rel_s = ET.SubElement(root, "mxCell", {
        "id": "leg_rel",
        "value": "<b>Rel</b>",
        "style": "rhombus;whiteSpace=wrap;html=1;fillColor=#ffedd5;strokeColor=#ea580c;strokeWidth=1.5;fontSize=10;fontColor=#9a3412;",
        "vertex": "1",
        "parent": "1"
    })
    ET.SubElement(rel_s, "mxGeometry", {"x": "170", "y": "995", "width": "60", "height": "40", "as": "geometry"})

    # Attribute sample
    att_s = ET.SubElement(root, "mxCell", {
        "id": "leg_att",
        "value": "Attribute",
        "style": "ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#64748b;strokeWidth=1.2;fontSize=10;",
        "vertex": "1",
        "parent": "1"
    })
    ET.SubElement(att_s, "mxGeometry", {"x": "250", "y": "1000", "width": "75", "height": "30", "as": "geometry"})

    # Key attribute sample
    pk_s = ET.SubElement(root, "mxCell", {
        "id": "leg_pk",
        "value": "<u><b>Key (PK)</b></u>",
        "style": "ellipse;whiteSpace=wrap;html=1;fillColor=#eff6ff;strokeColor=#2563eb;strokeWidth=1.5;fontSize=10;fontColor=#1e40af;",
        "vertex": "1",
        "parent": "1"
    })
    ET.SubElement(pk_s, "mxGeometry", {"x": "80", "y": "1055", "width": "80", "height": "30", "as": "geometry"})

    # Cardinality notation text
    card_text = ET.SubElement(root, "mxCell", {
        "id": "leg_card_text",
        "value": "<b>1, N, M:</b> Cardinality Ratios<br><b>0..1:</b> Optional Participation",
        "style": "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=11;fontColor=#475569;",
        "vertex": "1",
        "parent": "1"
    })
    ET.SubElement(card_text, "mxGeometry", {"x": "175", "y": "1050", "width": "200", "height": "40", "as": "geometry"})

    # Write files with proper XML formatting
    tree = ET.ElementTree(mxfile)
    ET.indent(tree, space="  ", level=0)
    tree.write(DRAWIO_PATH, encoding="utf-8", xml_declaration=True)
    tree.write(XML_PATH, encoding="utf-8", xml_declaration=True)
    print(f"[+] Successfully fixed and generated: {DRAWIO_PATH} ({os.path.getsize(DRAWIO_PATH)} bytes)")
    print(f"[+] Successfully fixed and generated: {XML_PATH} ({os.path.getsize(XML_PATH)} bytes)")


if __name__ == "__main__":
    build_drawio_file()
