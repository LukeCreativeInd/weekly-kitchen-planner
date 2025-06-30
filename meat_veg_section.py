def draw_meat_veg_section(pdf, xpos, col_w, ch, pad):
    left = xpos[0]
    y_start = pdf.get_y()
    bottom = 280  # Leave room for footer if any

    # --- Meat Order Table ---
    pdf.set_xy(left, pdf.get_y())
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
    # Save new Y position
    new_y = pdf.get_y()

    # If veg prep won't fit, start new column or new page
    space_needed = (len(meat_types) + 4 + 22 + 3) * ch
    if new_y + (22 + 3) * ch > bottom:
        # Move to second column
        col = 1
        pdf.set_xy(xpos[col], y_start)
    else:
        # Stay in first column, below meat table
        pdf.set_xy(left, new_y + pad)

    # --- Veg Prep Table ---
    pdf.set_font("Arial", "B", 14)
    pdf.cell(col_w, ch + 4, "Veg Prep", ln=1)
    pdf.ln(2)
    pdf.set_font("Arial", "B", 9)
    pdf.cell(col_w * 0.6, ch, "Veg Prep", 1)
    pdf.cell(col_w * 0.4, ch, "Amount", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 9)
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
    for veg in veg_prep_types:
        pdf.set_x(pdf.get_x())
        pdf.cell(col_w * 0.6, ch, veg, 1)
        pdf.cell(col_w * 0.4, ch, "0", 1)
        pdf.ln(ch)
