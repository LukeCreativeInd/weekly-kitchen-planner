def draw_meat_veg_section(pdf, xpos, col_w, ch, pad, bottom, start_y=None):
    pdf.set_y(start_y if start_y else pdf.get_y())
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"Meat Order and Veg Prep",ln=1,align='C')
    pdf.ln(5)
    # Meat Order
    pdf.set_font("Arial","B",11)
    pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, "Meat Order", ln=1, fill=True)
    pdf.set_font("Arial","B",8)
    for h, w in [("Meat Type", 0.6), ("Amount", 0.4)]:
        pdf.cell(col_w*w, ch, h, 1)
    pdf.ln(ch)
    pdf.set_font("Arial","",8)
    meats = [
        "CHUCK ROLL (LEBO)", "BEEF TOPSIDE (MONG)", "MINCE", "TOPSIDE STEAK",
        "LAMB SHOULDER", "MORROCAN CHICKEN", "ITALIAN CHICKEN", "NORMAL CHICKEN", "CHICKEN THIGH"
    ]
    for meat in meats:
        pdf.cell(col_w*0.6, ch, meat, 1)
        pdf.cell(col_w*0.4, ch, "0", 1)
        pdf.ln(ch)
    # Veg Prep
    pdf.ln(4)
    pdf.set_font("Arial","B",11)
    pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, "Veg Prep", ln=1, fill=True)
    pdf.set_font("Arial","B",8)
    for h, w in [("Veg Prep", 0.7), ("Amount", 0.3)]:
        pdf.cell(col_w*w, ch, h, 1)
    pdf.ln(ch)
    pdf.set_font("Arial","",8)
    vegs = [
        "10MM DICED CARROT", "10MM DICED POTATO (LEBO)", "10MM DICED ZUCCHINI",
        "5MM DICED CABBAGE", "5MM DICED CAPSICUM", "5MM DICED CARROTS", "5MM DICED CELERY",
        "5MM DICED MUSHROOMS", "5MM DICED ONION", "5MM MONGOLIAN CAPSICUM", "5MM MONGOLIAN ONION",
        "5MM SLICED MUSHROOMS", "BROCCOLI", "CRATED CARROTS", "CRATED ZUCCHINI",
        "LEMON POTATO", "ROASTED POTATO", "THAI POTATOS", "POTATO MASH", "SWEET POTATO MASH",
        "SPINACH", "RED ONION", "PARSLEY"
    ]
    for veg in vegs:
        pdf.cell(col_w*0.7, ch, veg, 1)
        pdf.cell(col_w*0.3, ch, "0", 1)
        pdf.ln(ch)
    return pdf.get_y() + pad
