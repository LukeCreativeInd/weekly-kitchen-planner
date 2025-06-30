def draw_fridge_section(pdf, meal_totals, xpos, col_w, ch, pad, bottom):
    # To Pack In Fridge, two-column layout
    y0 = pdf.get_y() + 2*ch
    pdf.set_xy(xpos[0], y0)
    pdf.set_font("Arial","B",14)
    pdf.cell(col_w*2+10, 10, "To Pack In Fridge", ln=1, align='C')
    pdf.ln(2)

    fridge_tables = [
        ("Sauces to Prepare", [("MONGOLIAN",70,"MONGOLIAN BEEF"),("MEATBALLS",120,"BEEF MEATBALLS"),
                               ("LEMON",50,"ROASTED LEMON CHICKEN"),("MUSHROOM",100,"STEAK WITH MUSHROOM SAUCE"),
                               ("FAJITA SAUCE",33,"CHICKEN FAJITA BOWL"),("BURRITO SAUCE",43,"BEEF BURRITO BOWL")], xpos[0], 0.4, 0.2)
        ,
        ("Beef Burrito Mix", [("Salsa",43),("Black Beans",50),("Corn",50),("Rice",130)], xpos[1], 0.4, 0.2),
        ("Parma Mix", [("Napoli Sauce",50),("Mozzarella Cheese",40)], xpos[1], 0.5, 0.5)
    ]

    for idx, (title, rows, x0, w1, w2) in enumerate(fridge_tables):
        y = pdf.get_y() if x0==xpos[0] else pdf.get_y()
        pdf.set_xy(x0, y)
        pdf.set_font("Arial","B",11); pdf.set_fill_color(230,230,230)
        pdf.cell(col_w, ch, title, ln=1, fill=True)
        pdf.set_x(x0); pdf.set_font("Arial","B",8)
        if title=="Sauces to Prepare":
            headers = [("Sauce",w1),("Qty",w2),("Amt",w2),("Total",w2)]
            for h,w in headers:
                pdf.cell(col_w*w, ch, h, 1)
            pdf.ln(ch); pdf.set_font("Arial","",8)
            for sauce,qty,meal_key in rows:
                amt = meal_totals.get(meal_key.upper(),0)
                tot = qty * amt
                pdf.set_x(x0)
                pdf.cell(col_w*w1, ch, sauce, 1)
                pdf.cell(col_w*w2, ch, str(qty), 1)
                pdf.cell(col_w*w2, ch, str(amt), 1)
                pdf.cell(col_w*w2, ch, str(tot), 1)
                pdf.ln(ch)
        else:
            headers = [("Ingredient",w1),("Qty",
