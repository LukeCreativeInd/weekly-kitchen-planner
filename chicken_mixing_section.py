def draw_chicken_mixing_section(pdf, meal_totals, xpos, col_w, ch, pad, bottom):
    import math
    mixes = [
        ("Pesto", [("Chicken",110),("Sauce",80)], "CHICKEN PESTO PASTA", 50),
        ("Butter Chicken", [("Chicken",120),("Sauce",90)], "BUTTER CHICKEN", 50),
        ("Broccoli Pasta", [("Chicken",100),("Sauce",100)], "CHICKEN AND BROCCOLI PASTA", 50),
        ("Thai", [("Chicken",110),("Sauce",90)], "THAI GREEN CHICKEN CURRY", 50),
        ("Gnocchi", [("Gnocchi",150),("Chicken",80),("Sauce",200),("Spinach",25)], "CREAMY CHICKEN & MUSHROOM GNOCCHI", 36)
    ]

    # Heading (full width)
    y0 = pdf.get_y()
    pdf.set_xy(xpos[0], y0)
    pdf.set_font("Arial","B",14)
    pdf.cell(col_w*2+10, ch, "Chicken Mixing", ln=1, align='L')
    pdf.ln(3)
    # 2-column placement logic
    col = 0
    heights = [pdf.get_y(), pdf.get_y()]
    for mix_title, ingredients, meal_key, divisor in mixes:
        block_h = (len(ingredients)+2)*ch + pad
        # Fit to next available column, or move to new page
        if heights[col]+block_h > bottom:
            col = 1-col
            if heights[col]+block_h > bottom:
                pdf.add_page()
                y0 = pdf.get_y()
                heights = [y0, y0]
        x, y = xpos[col], heights[col]
        pdf.set_xy(x, y)
        pdf.set_font("Arial","B",11)
        pdf.set_fill_color(230,230,230)
        pdf.cell(col_w, ch, mix_title, ln=1, fill=True)
        pdf.set_x(x)
        pdf.set_font("Arial","B",8)
        for h,w in [("Ingredient",0.3),("Qty",0.2),("Amt",0.2),("Total",0.2),("Batch",0.1)]:
            pdf.cell(col_w*w, ch, h, 1)
        pdf.ln(ch)
        pdf.set_font("Arial","",8)
        amt = meal_totals.get(meal_key, 0)
        raw_b = math.ceil(amt/divisor) if divisor>0 else 0
        batches = raw_b + (raw_b % 2)
        for ing, qty in ingredients:
            total = (qty * amt) / batches if batches else 0
            pdf.set_x(x)
            pdf.cell(col_w*0.3, ch, ing[:20], 1)
            pdf.cell(col_w*0.2, ch, str(qty), 1)
            pdf.cell(col_w*0.2, ch, str(amt), 1)
            pdf.cell(col_w*0.2, ch, str(round(total,2)), 1)
            pdf.cell(col_w*0.1, ch, str(batches), 1)
            pdf.ln(ch)
        heights[col] = pdf.get_y() + pad
