def draw_meat_veg_section(
    pdf, meal_totals, meal_recipes, bulk_sections,
    xpos, col_w, ch, pad, bottom, start_y=None
):
    import math

    # Always start at supplied y (should be top of new page)
    y = start_y or pdf.get_y()
    pdf.set_y(y)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Meat Order and Veg Prep", ln=1, align="C")
    pdf.ln(2)

    # --- Meat Order Table ---
    pdf.set_font("Arial", "B", 11)
    pdf.cell(col_w, ch, "Meat Order", ln=1, fill=True)
    pdf.set_font("Arial", "B", 8)
    for h, w in [("Meat Type", 0.6), ("Amount", 0.4)]:
        pdf.cell(col_w * w, ch, h, 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)

    # Helper: get meal count for multiple meals, matching import file case
    def total_meals(names):
        return sum([meal_totals.get(n.upper(), 0) for n in names])

    # Helper: get qty/meal for a recipe
    def get_qty_per_meal(recipe_key, ingr):
        recipe = meal_recipes.get(recipe_key, {})
        if not recipe:
            return 0
        return recipe["ingredients"].get(ingr, 0)

    # Helper: get bulk ingredient from bulk_sections
    def get_bulk_total(bulk_title, ingr):
        for sec in bulk_sections:
            if sec["title"].upper() == bulk_title.upper():
                qty = sec["ingredients"].get(ingr, 0)
                meals = sum(meal_totals.get(m.upper(), 0) for m in sec["meals"])
                return qty * meals
        return 0

    # --- Calculation for each meat type
    meat_rows = []

    # CHUCK ROLL (LEBO): Chuck Diced in Lebanese Beef Stew
    meals_lebo = meal_totals.get("LEBANESE BEEF STEW".upper(), 0)
    qty_chuck_lebo = get_qty_per_meal("Lebanese Beef Stew", "Chuck Diced")
    chuck_roll_lebo = meals_lebo * qty_chuck_lebo
    meat_rows.append(("CHUCK ROLL (LEBO)", chuck_roll_lebo))

    # BEEF TOPSIDE (MONG): Chuck in Mongolian Beef
    meals_mong = meal_totals.get("MONGOLIAN BEEF".upper(), 0)
    qty_chuck_mong = get_qty_per_meal("Mongolian Beef", "Chuck")
    beef_topside_mong = meals_mong * qty_chuck_mong
    meat_rows.append(("BEEF TOPSIDE (MONG)", beef_topside_mong))

    # MINCE: Beef Mince in Spaghetti, Shepherd's Pie, Beef Chow Mein, Beef Burrito Bowl, Beef Meatballs
    mince_meals = 0
    mince_meals += meal_totals.get("SPAGHETTI BOLOGNESE", 0) * get_qty_per_meal("Spaghetti Bolognese", "Beef Mince")
    mince_meals += meal_totals.get("SHEPHERD'S PIE", 0) * get_qty_per_meal("Shepherd's Pie", "Beef Mince")
    mince_meals += meal_totals.get("BEEF CHOW MEIN", 0) * get_qty_per_meal("Beef Chow Mein", "Beef Mince")
    mince_meals += meal_totals.get("BEEF BURRITO BOWL", 0) * get_qty_per_meal("Beef Burrito Bowl", "Beef Mince")
    mince_meals += meal_totals.get("BEEF MEATBALLS", 0) * get_qty_per_meal("Beef Meatballs", "Mince")
    meat_rows.append(("MINCE", mince_meals))

    # TOPSIDE STEAK: Steak in Steak section (bulk)
    steak_bulk_total = get_bulk_total("Steak", "Steak")
    meat_rows.append(("TOPSIDE STEAK", steak_bulk_total))

    # LAMB SHOULDER: Lamb Shoulder in Lamb Marinate (bulk)
    lamb_bulk_total = get_bulk_total("Lamb Marinate", "Lamb Shoulder")
    meat_rows.append(("LAMB SHOULDER", lamb_bulk_total))

    # MOROCCAN CHICKEN: Chicken in Moroccan Chicken (bulk)
    moroccan_chicken_total = get_bulk_total("Moroccan Chicken", "Chicken")
    meat_rows.append(("MOROCCAN CHICKEN", moroccan_chicken_total))

    # ITALIAN CHICKEN: Chicken With Vegetables, Chicken with Sweet Potato and Beans, Naked Chicken Parma, Chicken On Its Own
    italian_meals = (
        meal_totals.get("CHICKEN WITH VEGETABLES", 0) +
        meal_totals.get("CHICKEN WITH SWEET POTATO AND BEANS", 0) +
        meal_totals.get("NAKED CHICKEN PARMA", 0) +
        meal_totals.get("CHICKEN ON ITS OWN", 0)
    )
    italian_chicken = italian_meals * 153  # Per instructions
    meat_rows.append(("ITALIAN CHICKEN", italian_chicken))

    # NORMAL CHICKEN: Chicken Pesto Pasta, Butter Chicken, Chicken and Broccoli Pasta, Thai Green Chicken Curry, Creamy Chicken & Mushroom Gnocchi
    normal_meals = (
        meal_totals.get("CHICKEN PESTO PASTA", 0) +
        meal_totals.get("BUTTER CHICKEN", 0) +
        meal_totals.get("CHICKEN AND BROCCOLI PASTA", 0) +
        meal_totals.get("THAI GREEN CHICKEN CURRY", 0) +
        meal_totals.get("CREAMY CHICKEN & MUSHROOM GNOCCHI", 0)
    )
    normal_chicken = normal_meals * 130  # Per instructions
    meat_rows.append(("NORMAL CHICKEN", normal_chicken))

    # CHICKEN THIGH: Chicken in Chicken Thigh (bulk section)
    chicken_thigh_total = get_bulk_total("Chicken Thigh", "Chicken")
    meat_rows.append(("CHICKEN THIGH", chicken_thigh_total))

    # Write rows
    for meat, amt in meat_rows:
        pdf.cell(col_w * 0.6, ch, meat, 1)
        pdf.cell(col_w * 0.4, ch, f"{amt:.0f}", 1)
        pdf.ln(ch)

    pdf.ln(6)

    # --- Veg Prep Table ---
    pdf.set_font("Arial", "B", 11)
    pdf.cell(col_w, ch, "Veg Prep", ln=1, fill=True)
    pdf.set_font("Arial", "B", 8)
    for h, w in [("Veg Prep", 0.6), ("Amount", 0.4)]:
        pdf.cell(col_w * w, ch, h, 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)

    veg_prep_types = [
        "10MM DICED CARROT", "10MM DICED POTATO (LEBO)", "10MM DICED ZUCCHINI",
        "5MM DICED CABBAGE", "5MM DICED CAPSICUM", "5MM DICED CARROTS", "5MM DICED CELERY",
        "5MM DICED MUSHROOMS", "5MM DICED ONION", "5MM MONGOLIAN CAPSICUM", "5MM MONGOLIAN ONION",
        "5MM SLICED MUSHROOMS", "BROCCOLI", "CRATED CARROTS", "CRATED ZUCCHINI",
        "LEMON POTATO", "ROASTED POTATO", "THAI POTATOS", "POTATO MASH", "SWEET POTATO MASH",
        "SPINACH", "RED ONION", "PARSLEY"
    ]
    for veg in veg_prep_types:
        pdf.cell(col_w * 0.6, ch, veg, 1)
        pdf.cell(col_w * 0.4, ch, "0", 1)  # Update logic for calculation as needed
        pdf.ln(ch)

    return pdf.get_y() + pad
