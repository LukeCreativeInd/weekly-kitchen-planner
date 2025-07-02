from fpdf import FPDF

def draw_fridge_section(pdf, meal_totals, xpos, col_w, ch, pad, bottom, start_y=None):
    # Table data
    sauces_to_prepare = [
        ("MONGOLIAN", 70, "MONGOLIAN BEEF"),
        ("MEATBALLS", 120, "BEEF MEATBALLS"),
        ("LEMON", 50, "ROASTED LEMON CHICKEN"),
        ("MUSHROOM", 100, "STEAK WITH MUSHROOM SAUCE"),
        ("FAJITA SAUCE", 33, "CHICKEN FAJITA BOWL"),
        ("BURRITO SAUCE", 43, "BEEF BURRITO BOWL")
    ]
    beef_burrito_mix = [
        ("Salsa", 43),
        ("Black Beans", 50),
        ("Corn", 50),
        ("Rice", 130)
    ]
    parma_mix = [
        ("Napoli Sauce", 50),
        ("Mozzarella Cheese", 40)
    ]

    if start_y:
        pdf.set_y(start_y)
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"To Pack In Fridge",ln=1,align='C')
    pdf.ln(5)
    col_heights = [pdf.get_y(), pdf.get_y()]

    # --- Left Column: Sauces to Prepare ---
    x = xpos[0]
    pdf.set_xy(x, col_heights[0])
    pdf.set_font("Arial","B",11)
    pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, "Sauces to Prepare", ln=1, fill=True)
    pdf.set_x(x)
    pdf.set_font("Arial","B",8)
    for h,w in [("Sauce",0.4),("Qty",0.2),("Amt",0.2),("Total",0.2)]:
        pdf.cell(col_w*w, ch, h, 1)
    pdf.ln(ch)
    pdf.set_font("Arial","",8)
    for sauce, qty, meal_key in sauces_to_prepare:
        amt = meal_totals.get(meal_key.upper(),0)
        tot = qty * amt
        pdf.set_x(x)
        pdf.cell(col_w*0.4, ch, sauce, 1)
        pdf.cell(col_w*0.2, ch, str(qty), 1)
        pdf.cell(col_w*0.2, ch, str(amt), 1)
        pdf.cell(col_w*0.2, ch, str(tot), 1)
        pdf.ln(ch)
    col_heights[0] = pdf.get_y() + pad

    # --- Right Column: Beef Burrito Mix ---
    x = xpos[1]
    pdf.set_xy(x, col_heights[1])
    pdf.set_font("Arial","B",11)
    pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, "Beef Burrito Mix", ln=1, fill=True)
    pdf.set_x(x)
    pdf.set_font("Arial","B",8)
    for h,w in [("Ingredient",0.4),("Qty",0.2),("Amt",0.2),("Total",0.2)]:
        pdf.cell(col_w*w, ch, h, 1)
    pdf.ln(ch)
    pdf.set_font("Arial","",8)
    amt = meal_totals.get("BEEF BURRITO BOWL",0)
    for ing, qty in beef_burrito_mix:
        tot = (qty * amt) / 60 if amt else 0
        pdf.set_x(x)
        pdf.cell(col_w*0.4, ch, ing, 1)
        pdf.cell(col_w*0.2, ch, str(qty), 1)
        pdf.cell(col_w*0.2, ch, str(amt), 1)
        pdf.cell(col_w*0.2, ch, str(round(tot,2)), 1)
        pdf.ln(ch)
    col_heights[1] = pdf.get_y() + pad

    # --- Left Column below: Parma Mix ---
    x = xpos[0]
    pdf.set_xy(x, col_heights[0])
    pdf.set_font("Arial","B",11)
    pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, "Parma Mix", ln=1, fill=True)
    pdf.set_x(x)
    pdf.set_font("Arial","B",8)
    for h,w in [("Ingredient",0.6),("Qty",0.2),("Amt",0.2)]:
        pdf.cell(col_w*w, ch, h, 1)
    pdf.ln(ch)
    pdf.set_font("Arial","",8)
    amt = meal_totals.get("NAKED CHICKEN PARMA",0)
    for ing, qty in parma_mix:
        pdf.set_x(x)
        pdf.cell(col_w*0.6, ch, ing, 1)
        pdf.cell(col_w*0.2, ch, str(qty), 1)
        pdf.cell(col_w*0.2, ch, str(amt), 1)
        pdf.ln(ch)
    col_heights[0] = pdf.get_y() + pad

    return max(col_heights)
