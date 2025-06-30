def draw_fridge_section(pdf, meal_totals, xpos, col_w, ch, pad, bottom):
    from math import ceil

    # Table definitions
    fridge_tables = [
        {
            "title": "Sauces to Prepare",
            "headers": [("Sauce", 0.4), ("Qty", 0.2), ("Amt", 0.2), ("Total", 0.2)],
            "rows": [
                ("MONGOLIAN", 70, "MONGOLIAN BEEF"),
                ("MEATBALLS", 120, "BEEF MEATBALLS"),
                ("LEMON", 50, "ROASTED LEMON CHICKEN"),
                ("MUSHROOM", 100, "STEAK WITH MUSHROOM SAUCE"),
                ("FAJITA SAUCE", 33, "CHICKEN FAJITA BOWL"),
                ("BURRITO SAUCE", 43, "BEEF BURRITO BOWL")
            ]
        },
        {
            "title": "Beef Burrito Mix",
            "headers": [("Ingredient", 0.4), ("Qty", 0.2), ("Amt", 0.2), ("Total", 0.2)],
            "rows": [
                ("Salsa", 43),
                ("Black Beans", 50),
                ("Corn", 50),
                ("Rice", 130)
            ],
            "meal_key": "BEEF BURRITO BOWL",
            "divisor": 60
        },
        {
            "title": "Parma Mix",
            "headers": [("Ingredient", 0.5), ("Qty", 0.25), ("Amt", 0.25)],
            "rows": [
                ("Napoli Sauce", 50),
                ("Mozzarella Cheese", 40)
            ],
            "meal_key": "NAKED CHICKEN PARMA"
        }
    ]

    # Heading
    pdf.set_xy(xpos[0], pdf.get_y() + pad)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(col_w*2+10, ch, "To Pack In Fridge", ln=1, align='L')
    pdf.ln(3)

    y_start = pdf.get_y()
    heights = [y_start, y_start]

    # Draw first two tables side by side
    for idx, tdef in enumerate(fridge_tables[:2]):
        x = xpos[idx]
        y = heights[idx]
        pdf.set_xy(x, y)
        pdf.set_font("Arial", "B", 11)
        pdf.set_fill_color(230,230,230)
        pdf.cell(col_w, ch, tdef["title"], ln=1, fill=True)
        pdf.set_x(x)
        pdf.set_font("Arial", "B", 8)
        for h, w in tdef["headers"]:
            pdf.cell(col_w*w, ch, h, 1)
        pdf.ln(ch)
        pdf.set_font("Arial", "", 8)
        if idx == 0:
            # Sauces to Prepare
            for sauce, qty, meal_key in tdef["rows"]:
                amt = meal_totals.get(meal_key, 0)
                tot = qty * amt
                pdf.set_x(x)
                pdf.cell(col_w*0.4, ch, sauce, 1)
                pdf.cell(col_w*0.2, ch, str(qty), 1)
                pdf.cell(col_w*0.2, ch, str(amt), 1)
                pdf.cell(col_w*0.2, ch, str(tot), 1)
                pdf.ln(ch)
        else:
            # Beef Burrito Mix
            amt = meal_totals.get(tdef["meal_key"], 0)
            divisor = tdef.get("divisor", 1)
            for ing, qty in tdef["rows"]:
                tot = (qty * amt) / divisor if divisor else 0
                pdf.set_x(x)
                pdf.cell(col_w*0.4, ch, ing, 1)
                pdf.cell(col_w*0.2, ch, str(qty), 1)
                pdf.cell(col_w*0.2, ch, str(amt), 1)
                pdf.cell(col_w*0.2, ch, str(round(tot,2)), 1)
                pdf.ln(ch)
        heights[idx] = pdf.get_y()

    # Parma Mix starts below the taller of the first two columns, left column
    y_next = max(heights) + pad
    pdf.set_xy(xpos[0], y_next)
    tdef = fridge_tables[2]
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, tdef["title"], ln=1, fill=True)
    pdf.set_x(xpos[0])
    pdf.set_font("Arial", "B", 8)
    for h, w in tdef["headers"]:
        pdf.cell(col_w*w, ch, h, 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    amt = meal_totals.get(tdef["meal_key"], 0)
    for ing, qty in tdef["rows"]:
        pdf.set_x(xpos[0])
        pdf.cell(col_w*0.5, ch, ing, 1)
        pdf.cell(col_w*0.25, ch, str(qty), 1)
        pdf.cell(col_w*0.25, ch, str(amt), 1)
        pdf.ln(ch)

    # Set y to be after the bottom of this table for next section
    pdf.set_y(pdf.get_y() + pad)
