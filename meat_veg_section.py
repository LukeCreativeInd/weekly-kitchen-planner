def draw_meat_veg_section(pdf, xpos, col_w, ch, pad, start_y=None):
    pdf.set_y(start_y or pdf.get_y())
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"Meat Order and Veg Prep", ln=1, align='C')
    pdf.ln(5)

    # Meat Order
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
    pdf.set_font("Arial","B",11)
    pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, "Meat Order", ln=1, fill=True)
    pdf.set_font("Arial","B",8)
    pdf.cell(col_w*0.6, ch, "Meat Type", 1)
    pdf.cell(col_w*0.4, ch, "Amount", 1)
    pdf.ln(ch)
    pdf.set_font("Arial","",8)
    for mt in meat_types:
        pdf.cell(col_w*0.6, ch, mt, 1)
        pdf.cell(col_w*0.4, ch, "0", 1)
        pdf.ln(ch)
    pdf.ln(5)

    # Veg Prep
    veg_types = [
        "10MM DICED CARROT", "10MM DICED POTATO (LEBO)","10MM DICED ZUCCHINI",
        "5MM DICED CABBAGE", "5MM DICED CAPSICUM", "5MM DICED CARROTS", "5MM DICED CELERY", "5MM DICED MUSHROOMS",
        "5MM DICED ONION","5MM MONGOLIAN CAPSICUM","5MM MONGOLIAN ONION","5MM SLICED MUSHROOMS",
        "BROCCOLI","CRATED CARROTS","CRATED ZUCCHINI","LEMON POTATO","ROASTED POTATO","THAI POTATOS",
        "POTATO MASH","SWEET POTATO MASH","SPINACH","RED ONION","PARSLEY"
    ]
    pdf.set_font("Arial","B",11)
    pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, "Veg Prep", ln=1, fill=True)
    pdf.set_font("Arial","B",8)
    pdf.cell(col_w*0.6, ch, "Veg Prep", 1)
    pdf.cell(col_w*0.4, ch, "Amount", 1)
    pdf.ln(ch)
    pdf.set_font("Arial","",8)
    for vt in veg_types:
        pdf.cell(col_w*0.6, ch, vt, 1)
        pdf.cell(col_w*0.4, ch, "0", 1)
        pdf.ln(ch)
