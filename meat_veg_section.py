def draw_meat_veg_section(pdf, meal_totals, meal_recipes, bulk_sections, xpos, col_w, ch, pad, bottom, start_y=None):
    import math

    # -- Always start this section on a new page --
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Meat Order and Veg Prep", ln=1, align="C")
    pdf.ln(2)
    y = pdf.get_y()
    x = xpos[0]

    # ---- MEAT ORDER ----
    pdf.set_xy(x, y)
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Meat Order", ln=1, fill=True)
    pdf.set_x(x)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_w * 0.65, ch, "Meat Type", 1)
    pdf.cell(col_w * 0.35, ch, "Amount (g)", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)

    # Compute meat values
    # Italian Chicken calculation matches: Chicken with Vegetables, Chicken with Sweet Potato and Beans, Naked Chicken Parma, Chicken On Its Own
    it_chicken_meals = 0
    for meal in [
        "Chicken With Vegetables", "Chicken with Sweet Potato and Beans", "Naked Chicken Parma", "Chicken On Its Own"
    ]:
        it_chicken_meals += meal_totals.get(meal.upper(), 0)
    it_chicken_total = it_chicken_meals * 153

    # Normal Chicken: Chicken Pesto Pasta, Chicken and Broccoli Pasta, Butter Chicken, Thai Green Chicken Curry, Creamy Chicken & Mushroom Gnocchi
    normal_chicken_meals = 0
    for meal in [
        "Chicken Pesto Pasta", "Chicken and Broccoli Pasta", "Butter Chicken", "Thai Green Chicken Curry", "Creamy Chicken & Mushroom Gnocchi"
    ]:
        normal_chicken_meals += meal_totals.get(meal.upper(), 0)
    normal_chicken_total = normal_chicken_meals * 130

    # Chicken Thigh: Use total from Chicken Thigh table in bulk_sections
    chicken_thigh_total = 0
    for b in bulk_sections:
        if b["title"] == "Chicken Thigh":
            chicken_thigh_total = b["ingredients"]["Chicken"] * meal_totals.get("CHICKEN THIGH", 0)

    # Now all other meats, pulling totals from recipes or bulk as required:
    chuck_lebo = 0
    beef_topside_mong = 0
    mince_total = 0
    topside_steak = 0
    lamb_shoulder = 0
    moroccan_chicken = 0
    # Helper for recipes table lookups
    def get_recipe_total(meal, ingr):
        # For 'Beef Mince' or 'Chicken', etc.
        recipe = meal_recipes.get(meal)
        if not recipe: return 0
        qty = recipe["ingredients"].get(ingr, 0)
        count = meal_totals.get(meal.upper(), 0)
        return qty * count

    # 1. Chuck Roll (Lebo)
    chuck_lebo = get_recipe_total("Lebanese Beef Stew", "Chuck Diced")
    # 2. Beef Topside (Mong)
    beef_topside_mong = get_recipe_total("Mongolian Beef", "Chuck")
    # 3. Mince: Spag, Shep Pie, Chow Mein, Burrito Bowl, Meatballs
    mince_total = (
        get_recipe_total("Spaghetti Bolognese", "Beef Mince") +
        get_recipe_total("Shepherd's Pie", "Beef Mince") +
        get_recipe_total("Beef Chow Mein", "Beef Mince") +
        get_recipe_total("Beef Burrito Bowl", "Beef Mince") +
        get_recipe_total("Beef Meatballs", "Mince")
    )
    # 4. Topside Steak: 'Steak' row from Steak in bulk_sections
    for b in bulk_sections:
        if b["title"] == "Steak":
            topside_steak = b["ingredients"]["Steak"] * meal_totals.get("STEAK WITH MUSHROOM SAUCE", 0)
    # 5. Lamb Shoulder
    for b in bulk_sections:
        if b["title"] == "Lamb Marinate":
            lamb_shoulder = b["ingredients"]["Lamb Shoulder"] * meal_totals.get("LAMB SOUVLAKI", 0)
    # 6. Moroccan Chicken: 'Chicken' from Moroccan Chicken in bulk_sections
    for b in bulk_sections:
        if b["title"] == "Moroccan Chicken":
            moroccan_chicken = b["ingredients"]["Chicken"] * meal_totals.get("MOROCCAN CHICKEN", 0)

    # Write table rows
    meat_rows = [
        ("CHUCK ROLL (LEBO)", chuck_lebo),
        ("BEEF TOPSIDE (MONG)", beef_topside_mong),
        ("MINCE", mince_total),
        ("TOPSIDE STEAK", topside_steak),
        ("LAMB SHOULDER", lamb_shoulder),
        ("MORROCAN CHICKEN", moroccan_chicken),
        ("ITALIAN CHICKEN", it_chicken_total),
        ("NORMAL CHICKEN", normal_chicken_total),
        ("CHICKEN THIGH", chicken_thigh_total),
    ]
    for meat, amt in meat_rows:
        pdf.set_x(x)
        pdf.cell(col_w * 0.65, ch, meat, 1)
        pdf.cell(col_w * 0.35, ch, f"{int(round(amt,0)):,}", 1, ln=1)

    # --- Veg Prep (right column) ---
    veg_types = [
        "10MM DICED CARROT",
        "10MM DICED POTATO (LEBO)",
        "10MM DICED ZUCCHINI",
        "5MM DICED CABBAGE",
        "5MM DICED CAPSICUM",
        "5MM DICED CARROTS",
        "5MM DICED CELERY",
        "5MM DICED MUSHROOMS",
        "5MM DICED ONION",
        "5MM MONGOLIAN CAPSICUM",
        "5MM MONGOLIAN ONION",
        "5MM SLICED MUSHROOMS",
        "BROCCOLI",
        "CRATED CARROTS",
        "CRATED ZUCCHINI",
        "LEMON POTATO",
        "ROASTED POTATO",
        "THAI POTATOS",
        "POTATO MASH",
        "SWEET POTATO MASH",
        "SPINACH",
        "RED ONION",
        "PARSLEY",
    ]
    right_x = xpos[1]
    y_after_meat = pdf.get_y() + 5
    pdf.set_xy(right_x, y + ch)  # Level up with "Meat Order"
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Veg Prep", ln=1, fill=True)
    pdf.set_x(right_x)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_w * 0.65, ch, "Veg Prep", 1)
    pdf.cell(col_w * 0.35, ch, "Amount (g)", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    for veg in veg_types:
        pdf.set_x(right_x)
        pdf.cell(col_w * 0.65, ch, veg, 1)
        pdf.cell(col_w * 0.35, ch, "0", 1, ln=1)

    # Return lowest Y for downstream (in case more sections are ever added)
    return max(pdf.get_y(), y_after_meat + len(veg_types) * ch)
