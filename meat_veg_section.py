def draw_meat_veg_section(pdf, xpos, col_w, ch, pad):
    left = xpos[0]
    right = xpos[1]
    y_start = pdf.get_y()
    bottom = 280  # Allow space for footers, etc.

    # --- Meat Order Table ---
    pdf.set_xy(left, y_start)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(col_w, ch + 4, "Meat Order", ln=1)
    pdf.ln(2)
    pdf.set_font("Arial", "B", 9)
    pdf.cell(col_w * 0.6, ch, "Meat Type", 1)
    pdf.cell(col_w * 0.4, ch, "Amount", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 9)
    meat_types = [
        "CHUCK ROLL (LEBO)",
        "BEEF TOPSIDE (MONG)",
        "MINCE",
        "TOPSIDE STEAK",
        "LAMB SHOULDER",
        "MORROCAN CHICKEN",
        "ITALIAN CHICKEN",
        "NORMAL CHICKEN",
        "CHICKEN THIGH"
    ]
    for meat in meat_types:
        pdf.set_x(left)
        pdf.cell(col_w * 0.6, ch, meat, 1)
        pdf.cell(col_w * 0.4, ch, "0", 1)
        pdf.ln(ch)
    meat_table_end_y = pdf.get_y()

    # --- Veg Prep Table ---
    veg_prep_types = [
        "10MM DICED CARROT",
        "10MM DICED POTATO (LEBO)",
        "10MM DICED ZUCCHINI",
        "5MM DICED CABBAGE",
        "5MM DICED CAPSICUM",
        "5MM DICED CARROTS",
        "5MM DICED CELERY",
        "5MM DICED MUSHROOMS",
        "5MM DICED ONION",
        "5MM MONGOLIAN CAPSICUM",
        "5MM MONGOLIAN ONION",
        "5MM SLICED MUSHROOMS",
        "BROCCOLI",
        "CRATED CARROTS",
        "CRATED ZUCCHINI",
        "LEMON POTATO",
        "ROASTED POTATO",
        "THAI POTATOS",
        "POTATO MASH",
        "SWEET POTATO MASH",
        "SPINACH",
        "RED ONION",
        "PARSLEY"
    ]
    veg_table_height = (2 + len(veg_prep_types)) * ch + pad  # 2 rows for heading and space

    # If there isn't enough room for both on the same column, move Veg Prep to next column, top aligned
    if meat_table_end_y + veg_table_height > bottom:
        # Start Veg Prep at y_start in column 2
        pdf.set_xy(right, y_start)
    else:
        # Directly below meat table in column 1
        pdf.set_xy(left, meat_table_end_y + pad)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(col_w, ch + 4, "Veg Prep", ln=1)
    pdf.ln(2)
    pdf.set_font("Arial", "B", 9)
    pdf.cell(col_w * 0.6, ch, "Veg Prep", 1)
    pdf.cell(col_w * 0.4, ch, "Amount", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 9)
    for veg in veg_prep_types:
        pdf.set_x(pdf.get_x())
        pdf.cell(col_w * 0.6, ch, veg, 1)
        pdf.cell(col_w * 0.4, ch, "0", 1)
        pdf.ln(ch)

    # After this section, set y to the lower of the two columns (so the next section doesn't overlap)
    y_after = max(pdf.get_y(), meat_table_end_y)
    pdf.set_xy(left, y_after + pad)
