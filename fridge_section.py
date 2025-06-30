import math

def draw_fridge_section(pdf, meal_totals, xpos, col_w, ch, pad, bottom, start_y):
    y = start_y
    pdf.set_xy(xpos[0], y)
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"To Pack In Fridge",ln=1,align='C')
    pdf.ln(5)
    # Sauces to Prepare - left column
    x = xpos[0]
    pdf.set_xy(x, pdf.get_y())
    pdf.set_font("Arial","B",11)
    pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, "Sauces to Prepare", ln=1, fill=True)
    pdf.set_x(x)
    pdf.set_font("Arial","B",8)
    for h,w in [("Sauce",0.4),("Qty",0.2),("Amt",0.2),("Total",0.2)]:
        pdf.cell(col_w*w, ch, h, 1)
    pdf.ln(ch)
    pdf.set_font("Arial","",8)
    sauce_prep = [
        ("MONGOLIAN", 70, "MONGOLIAN BEEF"),
        ("MEATBALLS", 120, "BEEF MEATBALLS"),
        ("LEMON", 50, "ROASTED LEMON CHICKEN"),
        ("MUSHROOM", 100, "STEAK WITH MUSHROOM SAUCE"),
        ("FAJITA SAUCE", 33, "CHICKEN FAJITA BOWL"),
        ("BURRITO SAUCE", 43, "BEEF BURRITO BOWL")
    ]
    for sauce, qty, meal_key in sauce_prep:
        amt = meal_totals.get(meal_key,0)
        tot = qty * amt
        pdf.set_x(x)
        pdf.cell(col_w*0.4, ch, sauce, 1)
        pdf.cell(col_w*0.2, ch, str(qty), 1)
        pdf.cell(col_w*0.2, ch, str(amt), 1)
        pdf.cell(col_w*0.2, ch, str(tot), 1)
        pdf.ln(ch)

    # Beef Burrito Mix - right column
    x2 = xpos[1]
    y2 = y
    pdf.set_xy(x2, y2)
    pdf.set_font("Arial","B",11)
    pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, "Beef Burrito Mix", ln=1, fill=True)
    pdf.set_x(x2)
    pdf.set_font("Arial","B",8)
    for h,w in [("Ingredient",0.4),("Qty",0.2),("Amt",0.2),("Total",0.2)]:
        pdf.cell(col_w*w, ch, h, 1)
    pdf.ln(ch)
    pdf.set_font("Arial","",8)
    burrito_rows = [("Salsa",43),("Black Beans",50),("Corn",50),("Rice",130)]
    amt = meal_totals.get("BEEF BURRITO BOWL",0)
    for ing, qty in burrito_rows:
        tot = (qty * amt) / 60 if amt else 0
        pdf.set_x(x2)
        pdf.cell(col_w*0.4, ch, ing, 1)
        pdf.cell(col_w*0.2, ch, str(qty), 1)
        pdf.cell(col_w*0.2, ch, str(amt), 1)
        pdf.cell(col_w*0.2, ch, str(round(tot,2)), 1)
        pdf.ln(ch)

    # Parma Mix - right below left column
    pdf.set_xy(xpos[0], pdf.get_y())
    pdf.set_font("Arial","B",11)
    pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, "Parma Mix", ln=1, fill=True)
    pdf.set_x(xpos[0])
    pdf.set_font("Arial","B",8)
    for h,w in [("Ingredient",0.5),("Qty",0.25),("Amt",0.25)]:
        pdf.cell(col_w*w, ch, h, 1)
    pdf.ln(ch)
    pdf.set_font("Arial","",8)
    parma_rows = [("Napoli Sauce",50),("Mozzarella Cheese",40)]
    amt = meal_totals.get("NAKED CHICKEN PARMA",0)
    for ing, qty in parma_rows:
        pdf.set_x(xpos[0])
        pdf.cell(col_w*0.5, ch, ing, 1)
        pdf.cell(col_w*0.25, ch, str(qty), 1)
        pdf.cell(col_w*0.25, ch, str(amt), 1)
        pdf.ln(ch)

    return max(pdf.get_y(), pdf.get_y())
