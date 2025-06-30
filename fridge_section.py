def draw_fridge_section(pdf, meal_totals, xpos, col_w, ch, pad, bottom, start_y=None):
    # Dual column layout: first table left, second table right, heading spans full width above both
    fridge_tables = [
        ("Sauces to Prepare", [("MONGOLIAN",70,"MONGOLIAN BEEF"),
                               ("MEATBALLS",120,"BEEF MEATBALLS"),
                               ("LEMON",50,"ROASTED LEMON CHICKEN"),
                               ("MUSHROOM",100,"STEAK WITH MUSHROOM SAUCE"),
                               ("FAJITA SAUCE",33,"CHICKEN FAJITA BOWL"),
                               ("BURRITO SAUCE",43,"BEEF BURRITO BOWL")]),
        ("Beef Burrito Mix", [("Salsa",43),("Black Beans",50),("Corn",50),("Rice",130)]),
        ("Parma Mix", [("Napoli Sauce",50),("Mozzarella Cheese",40)]),
    ]
    # Heading
    pdf.set_y(start_y if start_y else pdf.get_y())
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"To Pack In Fridge", ln=1, align='C')
    pdf.ln(5)
    # Table 1 left, Table 2 right, Table 3 left below
    # Table 1: Sauces to Prepare (left)
    x_left = xpos[0]
    y_start = pdf.get_y()
    pdf.set_xy(x_left, y_start)
    pdf.set_font("Arial","B",11); pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, fridge_tables[0][0], ln=1, fill=True)
    pdf.set_x(x_left); pdf.set_font("Arial","B",8)
    for h,w in [("Sauce",0.4),("Qty",0.2),("Amt",0.2),("Total",0.2)]:
        pdf.cell(col_w*w, ch, h, 1)
    pdf.ln(ch); pdf.set_font("Arial","",8)
    for sauce,qty,meal_key in fridge_tables[0][1]:
        amt = meal_totals.get(meal_key,0)
        tot = qty * amt
        pdf.set_x(x_left)
        pdf.cell(col_w*0.4, ch, sauce, 1)
        pdf.cell(col_w*0.2, ch, str(qty), 1)
        pdf.cell(col_w*0.2, ch, str(amt), 1)
        pdf.cell(col_w*0.2, ch, str(tot), 1)
        pdf.ln(ch)
    y_left_end = pdf.get_y()
    # Table 2: Beef Burrito Mix (right column, at top)
    x_right = xpos[1]
    pdf.set_xy(x_right, y_start)
    pdf.set_font("Arial","B",11); pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, fridge_tables[1][0], ln=1, fill=True)
    pdf.set_x(x_right); pdf.set_font("Arial","B",8)
    for h,w in [("Ingredient",0.4),("Qty",0.2),("Amt",0.2),("Total",0.2)]:
        pdf.cell(col_w*w, ch, h, 1)
    pdf.ln(ch); pdf.set_font("Arial","",8)
    for ing,qty in fridge_tables[1][1]:
        amt = meal_totals.get("BEEF BURRITO BOWL",0)
        tot = (qty * amt) / 60 if amt else 0
        pdf.set_x(x_right)
        pdf.cell(col_w*0.4, ch, ing, 1)
        pdf.cell(col_w*0.2, ch, str(qty), 1)
        pdf.cell(col_w*0.2, ch, str(amt), 1)
        pdf.cell(col_w*0.2, ch, str(round(tot,2)), 1)
        pdf.ln(ch)
    y_right_end = pdf.get_y()
    # Table 3: Parma Mix (left, below Table 1)
    pdf.set_xy(x_left, y_left_end + pad)
    pdf.set_font("Arial","B",11); pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, fridge_tables[2][0], ln=1, fill=True)
    pdf.set_x(x_left); pdf.set_font("Arial","B",8)
    for h,w in [("Ingredient",0.5),("Qty",0.2),("Amt",0.2),("Total",0.1)]:
        pdf.cell(col_w*w, ch, h, 1)
    pdf.ln(ch); pdf.set_font("Arial","",8)
    for ing,qty in fridge_tables[2][1]:
        amt = meal_totals.get("NAKED CHICKEN PARMA",0)
        tot = qty * amt
        pdf.set_x(x_left)
        pdf.cell(col_w*0.5, ch, ing, 1)
        pdf.cell(col_w*0.2, ch, str(qty), 1)
        pdf.cell(col_w*0.2, ch, str(amt), 1)
        pdf.cell(col_w*0.1, ch, str(round(tot,2)), 1)
        pdf.ln(ch)
    # Calculate end Y
    return max(pdf.get_y(), y_right_end)
