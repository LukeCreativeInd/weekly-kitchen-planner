def draw_meat_veg_section(pdf, xpos, col_w, ch, pad, bottom, start_y):
    pdf.set_xy(xpos[0], start_y)
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"Meat Order and Veg Prep",ln=1,align='C')
    pdf.ln(5)
    # Meat Order table (left)
    x1 = xpos[0]
    pdf.set_xy(x1, pdf.get_y())
    pdf.set_font("Arial","B",11)
    pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, "Meat Order", ln=1, fill=True)
    pdf.set_x(x1)
    pdf.set_font("Arial","B",8)
    for h,w in [("Meat Type",0.6),("Amount",0.4)]:
        pdf.cell(col_w*w, ch, h, 1)
    pdf.ln(ch)
    pdf.set_font("Arial","",8)
    meat_types = [
        "CHUCK ROLL (LEBO)","BEEF TOPSIDE (MONG)","MINCE","TOPSIDE STEAK","LAMB SHOULDER",
        "MORROCAN CHICKEN","ITALIAN CHICKEN","NORMAL CHICKEN","CHICKEN THIGH"
    ]
    for meat in meat_types:
        pdf.set_x(x1)
        pdf.cell(col_w*0.6, ch, meat, 1)
        pdf.cell(col_w*0.4, ch, "0", 1)
        pdf.ln(ch)
    # Veg Prep table (right)
    x2 = xpos[1]
    y2 = pdf.get_y() - ch * len(meat_types) - 15 # Align top with Meat Order
    pdf.set_xy(x2, y2)
    pdf.set_font("Arial","B",11)
    pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, "Veg Prep", ln=1, fill=True)
    pdf.set_x(x2)
    pdf.set_font("Arial","B",8)
    for h,w in [("Veg Prep",0.6),("Amount",0.4)]:
        pdf.cell(col_w*w, ch, h, 1)
    pdf.ln(ch)
    pdf.set_font("Arial","",8)
    veg_types = [
        "10MM DICED CARROT","10MM DICED POTATO (LEBO)","10MM DICED ZUCCHINI","5MM DICED CABBAGE",
        "5MM DICED CAPSICUM","5MM DICED CARROTS","5MM DICED CELERY","5MM DICED MUSHROOMS","5MM DICED ONION",
        "5MM MONGOLIAN CAPSICUM","5MM MONGOLIAN ONION","5MM SLICED MUSHROOMS","BROCCOLI","CRATED CARROTS",
        "CRATED ZUCCHINI","LEMON POTATO","ROASTED POTATO","THAI POTATOS","POTATO MASH","SWEET POTATO MASH",
        "SPINACH","RED ONION","PARSLEY"
    ]
    for veg in veg_types:
        pdf.set_x(x2)
        pdf.cell(col_w*0.6, ch, veg, 1)
        pdf.cell(col_w*0.4, ch, "0", 1)
        pdf.ln(ch)
    return max(pdf.get_y(), pdf.get_y())
