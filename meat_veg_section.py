def draw_meat_veg_section(pdf, xpos, col_w, ch, pad, bottom, start_y=None):
    # Always start on a new page
    pdf.add_page()
    left = xpos[0]
    pdf.set_xy(left, 10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Meat Order and Veg Prep", ln=1, align='C')
    pdf.ln(5)

    # Meat Order Table
    meat_types = [
        "CHUCK ROLL (LEBO)",
        "BEEF TOPSIDE (MONG)",
        "MINCE",
        "TOPSIDE STEAK",
        "LAMB SHOULDER",
        "MORROCAN CHICKEN",
        "ITALIAN CHICKEN",
        "NORMAL CHICKEN",
        "CHICKEN THIGH",
    ]
    col1_x = xpos[0]
    table_w = col_w * 0.7
    pdf.set_x(col1_x)
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(table_w, ch, "Meat Order", ln=1, fill=True)
    pdf.set_x(col1_x)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(table_w * 0.7, ch, "Meat Type", 1)
    pdf.cell(table_w * 0.3, ch, "Amount", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    for meat in meat_types:
        pdf.set_x(col1_x)
        pdf.cell(table_w * 0.7, ch, meat, 1)
        pdf.cell(table_w * 0.3, ch, "0", 1)
        pdf.ln(ch)

    # Veg Prep Table
    veg_types = [
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
        "PARSLEY",
    ]
    pdf.ln(5)
    pdf.set_x(col1_x)
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(table_w, ch, "Veg Prep", ln=1, fill=True)
    pdf.set_x(col1_x)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(table_w * 0.7, ch, "Veg Prep", 1)
    pdf.cell(table_w * 0.3, ch, "Amount", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    for veg in veg_types:
        pdf.set_x(col1_x)
        pdf.cell(table_w * 0.7, ch, veg, 1)
        pdf.cell(table_w * 0.3, ch, "0", 1)
        pdf.ln(ch)
