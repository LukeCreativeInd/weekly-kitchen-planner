import math

def draw_meat_veg_section(pdf, meal_totals, xpos, col_w, ch, pad, bottom, start_y=0, meal_recipes=None, bulk_sections=None):
    # Start new page
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Meat Order and Veg Prep", ln=1, align='C')
    pdf.ln(5)
    left = xpos[0]
    right = xpos[1]

    # --- 1. Meat Order Table ---
    meat_types = [
        "CHUCK ROLL (LEBO)", "BEEF TOPSIDE (MONG)", "MINCE", "TOPSIDE STEAK",
        "LAMB SHOULDER", "MORROCAN CHICKEN", "ITALIAN CHICKEN", "NORMAL CHICKEN", "CHICKEN THIGH"
    ]

    # Lookups for meal recipes and bulk if passed in
    recipes = meal_recipes if meal_recipes else {}
    bulk = bulk_sections if bulk_sections else []

    # 1. CHUCK ROLL (LEBO)
    try:
        lebo_meals = meal_totals.get("LEBANESE BEEF STEW", 0)
        lebo_qty = recipes["Lebanese Beef Stew"]["ingredients"]["Chuck Diced"]
        chuck_roll_lebo = lebo_qty * lebo_meals
    except Exception:
        chuck_roll_lebo = 0

    # 2. BEEF TOPSIDE (MONG)
    try:
        mong_meals = meal_totals.get("MONGOLIAN BEEF", 0)
        mong_qty = recipes["Mongolian Beef"]["ingredients"]["Chuck"]
        beef_topside_mong = mong_qty * mong_meals
    except Exception:
        beef_topside_mong = 0

    # 3. MINCE (sum all Beef Mince from multiple recipes)
    mince_sum = 0
    for recipe_name in ["Spaghetti Bolognese", "Shepherd's Pie", "Beef Chow Mein", "Beef Burrito Bowl", "Beef Meatballs"]:
        try:
            if recipe_name == "Beef Meatballs":
                ingr = "Mince"
            else:
                ingr = "Beef Mince"
            meals = meal_totals.get(recipe_name.upper(), 0)
            qty = recipes[recipe_name]["ingredients"][ingr]
            mince_sum += qty * meals
        except Exception:
            pass

    # 4. TOPSIDE STEAK from bulk ("Steak" in "Steak" bulk section)
    topside_steak = 0
    for sec in bulk:
        if sec["title"].lower().startswith("steak"):
            meals = sum(meal_totals.get(m.upper(), 0) for m in sec["meals"])
            qty = sec["ingredients"].get("Steak", 0)
            topside_steak = qty * meals
            break

    # 5. LAMB SHOULDER from bulk ("Lamb Shoulder" in "Lamb Marinate")
    lamb_shoulder = 0
    for sec in bulk:
        if sec["title"].lower().startswith("lamb marinate"):
            meals = sum(meal_totals.get(m.upper(), 0) for m in sec["meals"])
            qty = sec["ingredients"].get("Lamb Shoulder", 0)
            lamb_shoulder = qty * meals
            break

    # 6. MORROCAN CHICKEN from bulk ("Chicken" in "Moroccan Chicken")
    morrocan_chicken = 0
    for sec in bulk:
        if sec["title"].lower().startswith("moroccan chicken"):
            meals = sum(meal_totals.get(m.upper(), 0) for m in sec["meals"])
            qty = sec["ingredients"].get("Chicken", 0)
            morrocan_chicken = qty * meals
            break

    # 7–9: ITALIAN, NORMAL, CHICKEN THIGH
    italian_chicken = 0
    normal_chicken = 0
    chicken_thigh = 0

    # Now output the table
    meats = [
        chuck_roll_lebo,
        beef_topside_mong,
        mince_sum,
        topside_steak,
        lamb_shoulder,
        morrocan_chicken,
        italian_chicken,
        normal_chicken,
        chicken_thigh,
    ]

    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Meat Order", ln=1, fill=True)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_w * 0.7, ch, "Meat Type", 1)
    pdf.cell(col_w * 0.3, ch, "Amount (g)", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    for mt, amt in zip(meat_types, meats):
        pdf.cell(col_w * 0.7, ch, mt, 1)
        pdf.cell(col_w * 0.3, ch, f"{amt:.0f}", 1)
        pdf.ln(ch)

    # --- 2. Veg Prep Table (same as before, just placeholder 0s) ---
    veg_types = [
        "10MM DICED CARROT", "10MM DICED POTATO (LEBO)", "10MM DICED ZUCCHINI", "5MM DICED CABBAGE",
        "5MM DICED CAPSICUM", "5MM DICED CARROTS", "5MM DICED CELERY", "5MM DICED MUSHROOMS",
        "5MM DICED ONION", "5MM MONGOLIAN CAPSICUM", "5MM MONGOLIAN ONION", "5MM SLICED MUSHROOMS",
        "BROCCOLI", "CRATED CARROTS", "CRATED ZUCCHINI", "LEMON POTATO", "ROASTED POTATO",
        "THAI POTATOS", "POTATO MASH", "SWEET POTATO MASH", "SPINACH", "RED ONION", "PARSLEY"
    ]

    pdf.ln(5)
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Veg Prep", ln=1, fill=True)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_w * 0.7, ch, "Veg Prep", 1)
    pdf.cell(col_w * 0.3, ch, "Amount (g)", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    for vt in veg_types:
        pdf.cell(col_w * 0.7, ch, vt, 1)
        pdf.cell(col_w * 0.3, ch, "0", 1)
        pdf.ln(ch)

    return pdf.get_y()
