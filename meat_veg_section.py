def draw_meat_veg_section(pdf, xpos, col_w, ch, pad):
    # --- Meat Order Table ---
    pdf.set_y(pdf.get_y() + pad)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(col_w * 2 + 10, ch, "Meat Order and Veg Prep", ln=1, align='L')
    pdf.ln(3)

    # Meat Order Table
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Meat Order", ln=1, fill=True)
    pdf.set_font("Arial", "B", 8)
    pdf.set_x(xpos[0])
    pdf.cell(col_w * 0.7, ch, "Meat Type", 1)
    pdf.cell(col_w * 0.3, ch, "Amount", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
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
    for m in meat_types:
        pdf.set_x(xpos[0])
        pdf.cell(col_w * 0.7, ch, m, 1)
        pdf.cell(col_w * 0.3, ch, "0", 1)
        pdf.ln(ch)

    pdf.ln(5)

    # --- Veg Prep Table ---
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Veg Prep", ln=1, fill=True)
    pdf.set_font("Arial", "B", 8)
    pdf.set_x(xpos[0])
    pdf.cell(col_w * 0.7, ch, "Veg Prep", 1)
    pdf.cell(col_w * 0.3, ch, "Amount", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
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
        "PARSLEY"
    ]
    for v in veg_types:
        pdf.set_x(xpos[0])
        pdf.cell(col_w * 0.7, ch, v, 1)
        pdf.cell(col_w * 0.3, ch, "0", 1)
        pdf.ln(ch)
    pdf.ln(5)
