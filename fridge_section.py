def draw_fridge_section(pdf, meal_totals, xpos, col_w, ch, pad, bottom, start_y=None):
    # Tables for dual column
    fridge_tables = [
        ("Sauces to Prepare", [("MONGOLIAN", 70, "MONGOLIAN BEEF"), ("MEATBALLS", 120, "BEEF MEATBALLS"),
                              ("LEMON", 50, "ROASTED LEMON CHICKEN"), ("MUSHROOM", 100, "STEAK WITH MUSHROOM SAUCE"),
                              ("FAJITA SAUCE", 33, "CHICKEN FAJITA BOWL"), ("BURRITO SAUCE", 43, "BEEF BURRITO BOWL")]),
        ("Beef Burrito Mix", [("Salsa", 43), ("Black Beans", 50), ("Corn", 50), ("Rice", 130)]),
        ("Parma Mix", [("Napoli Sauce", 50), ("Mozzarella Cheese", 40)]),
    ]
    if start_y:
        pdf.set_y(start_y)
    y_start = pdf.get_y()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "To Pack In Fridge", ln=1, align='C')
    pdf.ln(5)

    # First and second table in columns, rest below
    col_y = [pdf.get_y(), pdf.get_y()]
    for idx, (title, rows) in enumerate(fridge_tables):
        col = idx if idx < 2 else 0
        x = xpos[col]
        pdf.set_xy(x, col_y[col])
        pdf.set_font("Arial", "B", 11)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(col_w, ch, title, ln=1, fill=True)
        pdf.set_x(x)
        pdf.set_font("Arial", "B", 8)
        if title == "Sauces to Prepare":
            headers = [("Sauce", 0.4), ("Qty", 0.2), ("Amt", 0.2), ("Total", 0.2)]
            for h, w in headers:
                pdf.cell(col_w * w, ch, h, 1)
            pdf.ln(ch)
            pdf.set_font("Arial", "", 8)
            for sauce, qty, meal_key in rows:
                amt = meal_totals.get(meal_key, 0)
                tot = qty * amt
                pdf.set_x(x)
                pdf.cell(col_w * 0.4, ch, sauce, 1)
                pdf.cell(col_w * 0.2, ch, str(qty), 1)
                pdf.cell(col_w * 0.2, ch, str(amt), 1)
                pdf.cell(col_w * 0.2, ch, str(tot), 1)
                pdf.ln(ch)
        elif title == "Beef Burrito Mix":
            headers = [("Ingredient", 0.4), ("Qty", 0.2), ("Amt", 0.2), ("Total", 0.2)]
            for h, w in headers:
                pdf.cell(col_w * w, ch, h, 1)
            pdf.ln(ch)
            pdf.set_font("Arial", "", 8)
            amt = meal_totals.get("BEEF BURRITO BOWL", 0)
            for ing, qty in rows:
                tot = (qty * amt) / 60 if amt else 0
                pdf.set_x(x)
                pdf.cell(col_w * 0.4, ch, ing, 1)
                pdf.cell(col_w * 0.2, ch, str(qty), 1)
                pdf.cell(col_w * 0.2, ch, str(amt), 1)
                pdf.cell(col_w * 0.2, ch, str(round(tot, 2)), 1)
                pdf.ln(ch)
        elif title == "Parma Mix":
            headers = [("Ingredient", 0.5), ("Qty", 0.25), ("Amt", 0.25)]
            for h, w in headers:
                pdf.cell(col_w * w, ch, h, 1)
            pdf.ln(ch)
            pdf.set_font("Arial", "", 8)
            amt = meal_totals.get("NAKED CHICKEN PARMA", 0)
            for ing, qty in rows:
                pdf.set_x(x)
                pdf.cell(col_w * 0.5, ch, ing, 1)
                pdf.cell(col_w * 0.25, ch, str(qty), 1)
                pdf.cell(col_w * 0.25, ch, str(amt), 1)
                pdf.ln(ch)
        col_y[col] = pdf.get_y() + pad
    # Return max y for next section
    return max(col_y)
