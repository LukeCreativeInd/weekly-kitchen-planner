def draw_meat_veg_section(pdf, meal_totals, meal_recipes, bulk_sections, xpos, col_w, ch, pad, bottom, start_y=None):
    y = start_y or pdf.get_y()
    pdf.set_y(y)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Meat Order and Veg Prep", ln=1, align="C")
    pdf.ln(2)

    # --- Meat Order table ---
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, "Meat Order", ln=1, fill=True)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_w*0.7, ch, "Meat Type", 1)
    pdf.cell(col_w*0.3, ch, "Amount", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)

    # --- Calculation Example (replace with your real logic as needed) ---
    # The following assumes your meal_recipes and bulk_sections are passed in as params
    # and that meal_totals is a dict keyed by UPPERCASE names.
    def get_total_qty(meal, ingredient):
        if meal in meal_recipes and ingredient in meal_recipes[meal]["ingredients"]:
            qty_per_meal = meal_recipes[meal]["ingredients"][ingredient]
            meal_amt = meal_totals.get(meal.upper(), 0)
            return qty_per_meal * meal_amt
        return 0

    def get_bulk_total(section_title, ingredient):
        for section in bulk_sections:
            if section['title'] == section_title and ingredient in section["ingredients"]:
                tot_meals = sum(meal_totals.get(m.upper(),0) for m in section["meals"])
                return section["ingredients"][ingredient] * tot_meals
        return 0

    meat_order = [
        ("CHUCK ROLL (LEBO)", get_total_qty("Lebanese Beef Stew", "Chuck Diced")),
        ("BEEF TOPSIDE (MONG)", get_total_qty("Mongolian Beef", "Chuck")),
        ("MINCE",
            sum([
                get_total_qty("Spaghetti Bolognese", "Beef Mince"),
                get_total_qty("Shepherd's Pie", "Beef Mince"),
                get_total_qty("Beef Chow Mein", "Beef Mince"),
                get_total_qty("Beef Burrito Bowl", "Beef Mince"),
                get_total_qty("Beef Meatballs", "Mince")
            ])
        ),
        ("TOPSIDE STEAK", get_bulk_total("Steak", "Steak")),
        ("LAMB SHOULDER", get_bulk_total("Lamb Marinate", "Lamb Shoulder")),
        ("MORROCAN CHICKEN", get_bulk_total("Moroccan Chicken", "Chicken")),
        ("ITALIAN CHICKEN", 0),
        ("NORMAL CHICKEN", 0),
        ("CHICKEN THIGH", 0),
    ]

    for name, amt in meat_order:
        pdf.cell(col_w*0.7, ch, name, 1)
        pdf.cell(col_w*0.3, ch, str(int(amt)), 1)
        pdf.ln(ch)

    pdf.ln(5)
    # --- Veg Prep table ---
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, "Veg Prep", ln=1, fill=True)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_w*0.7, ch, "Veg Prep", 1)
    pdf.cell(col_w*0.3, ch, "Amount", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)

    veg_preps = [
        "10MM DICED CARROT", "10MM DICED POTATO (LEBO)", "10MM DICED ZUCCHINI", "5MM DICED CABBAGE",
        "5MM DICED CAPSICUM", "5MM DICED CARROTS", "5MM DICED CELERY", "5MM DICED MUSHROOMS",
        "5MM DICED ONION", "5MM MONGOLIAN CAPSICUM", "5MM MONGOLIAN ONION", "5MM SLICED MUSHROOMS",
        "BROCCOLI", "CRATED CARROTS", "CRATED ZUCCHINI", "LEMON POTATO", "ROASTED POTATO",
        "THAI POTATOS", "POTATO MASH", "SWEET POTATO MASH", "SPINACH", "RED ONION", "PARSLEY"
    ]
    for name in veg_preps:
        pdf.cell(col_w*0.7, ch, name, 1)
        pdf.cell(col_w*0.3, ch, "0", 1)
        pdf.ln(ch)
    # Return Y for consistency
    return pdf.get_y()
