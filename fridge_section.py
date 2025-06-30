def draw_fridge_section(pdf, meal_totals, xpos, col_w, ch, pad, bottom, start_y):
    pdf.set_y(start_y)
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"To Pack In Fridge", ln=1, align='C')
    pdf.ln(5)

    # Table 1: Sauces to Prepare (left column)
    x0 = xpos[0]
    pdf.set_xy(x0, pdf.get_y())
    pdf.set_font("Arial","B",11); pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, "Sauces to Prepare", ln=1, fill=True)
    pdf.set_x(x0); pdf.set_font("Arial","B",8)
    headers = [("Sauce",0.4),("Qty",0.2),("Amt",0.2),("Total",0.2)]
    for h,w in headers:
        pdf.cell(col_w*w, ch, h, 1)
    pdf.ln(ch); pdf.set_font("Arial","",8)
    sauce_prep=[("MONGOLIAN",70,"MONGOLIAN BEEF"),("MEATBALLS",120,"BEEF MEATBALLS"),
                ("LEMON",50,"ROASTED LEMON CHICKEN"),("MUSHROOM",100,"STEAK WITH MUSHROOM SAUCE"),
                ("FAJITA SAUCE",33,"CHICKEN FAJITA BOWL"),("BURRITO SAUCE",43,"BEEF BURRITO BOWL")]
    for sauce, qty, meal_key in sauce_prep:
        amt = meal_totals.get(meal_key,0)
        tot = qty * amt
        pdf.set_x(x0)
        pdf.cell(col_w*0.4, ch, sauce, 1)
        pdf.cell(col_w*0.2, ch, str(qty), 1)
        pdf.cell(col_w*0.2, ch, str(amt), 1)
        pdf.cell(col_w*0.2, ch, str(tot), 1)
        pdf.ln(ch)

    # Table 2: Beef Burrito Mix (right column)
    x1 = xpos[1]
    pdf.set_xy(x1, start_y+ch+pad)
    pdf.set_font("Arial","B",11); pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, "Beef Burrito Mix", ln=1, fill=True)
    pdf.set_x(x1); pdf.set_font("Arial","B",8)
    headers = [("Ingredient",0.4),("Qty",0.2),("Amt",0.2),("Total",0.2)]
    for h,w in headers:
        pdf.cell(col_w*w, ch, h, 1)
    pdf.ln(ch); pdf.set_font("Arial","",8)
    for ing,qty in [("Salsa",43),("Black Beans",50),("Corn",50),("Rice",130)]:
        amt = meal_totals.get("BEEF BURRITO BOWL",0)
        tot = (qty * amt) / 60 if amt else 0
        pdf.set_x(x1)
        pdf.cell(col_w*0.4, ch, ing, 1)
        pdf.cell(col_w*0.2, ch, str(qty), 1)
        pdf.cell(col_w*0.2, ch, str(amt), 1)
        pdf.cell(col_w*0.2, ch, str(round(tot,2)), 1)
        pdf.ln(ch)

    # Table 3: Parma Mix (left column, under Sauces to Prepare)
    pdf.set_xy(x0, pdf.get_y() + pad)
    pdf.set_font("Arial","B",11); pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, "Parma Mix", ln=1, fill=True)
    pdf.set_x(x0); pdf.set_font("Arial","B",8)
    headers = [("Ingredient",0.5),("Amt",0.25),("Total",0.25)]
    for h,w in headers:
        pdf.cell(col_w*w, ch, h, 1)
    pdf.ln(ch); pdf.set_font("Arial","",8)
    amt = meal_totals.get("NAKED CHICKEN PARMA",0)
    for ing, qty in [("Napoli Sauce",50),("Mozzarella Cheese",40)]:
        total = qty * amt
        pdf.set_x(x0)
        pdf.cell(col_w*0.5, ch, ing, 1)
        pdf.cell(col_w*0.25, ch, str(qty), 1)
        pdf.cell(col_w*0.25, ch, str(total), 1)
        pdf.ln(ch)

    return max(pdf.get_y(), pdf.get_y())
