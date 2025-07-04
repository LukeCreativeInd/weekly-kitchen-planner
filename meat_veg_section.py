import math

def draw_meat_veg_section(pdf, meal_totals, meal_recipes, bulk_sections, xpos, col_w, ch, pad, bottom, start_y=None):
    # Set starting Y position
    y = start_y or pdf.get_y()
    pdf.set_y(y)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Meat Order and Veg Prep", ln=1, align="C")
    pdf.ln(2)

    left = xpos[0]
    right = xpos[1]

    # ----------- MEAT ORDER CALCULATIONS -----------

    # Chuck Roll (Lebo) - Chuck Diced from Lebanese Beef Stew (Qty/Meal x Meals)
    chuck_roll_lebo = 0
    if "Lebanese Beef Stew" in meal_recipes:
        qty = meal_recipes["Lebanese Beef Stew"]["ingredients"].get("Chuck Diced", 0)
        meals = meal_totals.get("LEBANESE BEEF STEW", 0)
        chuck_roll_lebo = qty * meals

    # Beef Topside (Mong) - Chuck from Mongolian Beef
    beef_topside_mong = 0
    if "Mongolian Beef" in meal_recipes:
        qty = meal_recipes["Mongolian Beef"]["ingredients"].get("Chuck", 0)
        meals = meal_totals.get("MONGOLIAN BEEF", 0)
        beef_topside_mong = qty * meals

    # Mince - Total Beef Mince from Spaghetti Bolognese, Shepherd's Pie, Beef Chow Mein, Beef Burrito Bowl, plus Mince from Beef Meatballs
    mince = 0
    # Beef Mince recipes
    mince += meal_recipes["Spaghetti Bolognese"]["ingredients"].get("Beef Mince", 0) * meal_totals.get("SPAGHETTI BOLOGNESE", 0)
    mince += meal_recipes["Shepherd's Pie"]["ingredients"].get("Beef Mince", 0) * meal_totals.get("SHEPHERD'S PIE", 0)
    mince += meal_recipes["Beef Chow Mein"]["ingredients"].get("Beef Mince", 0) * meal_totals.get("BEEF CHOW MEIN", 0)
    mince += meal_recipes["Beef Burrito Bowl"]["ingredients"].get("Beef Mince", 0) * meal_totals.get("BEEF BURRITO BOWL", 0)
    # Mince from Beef Meatballs
    mince += meal_recipes["Beef Meatballs"]["ingredients"].get("Mince", 0) * meal_totals.get("BEEF MEATBALLS", 0)

    # Topside Steak - "Steak" from Steak with Mushroom Sauce and Steak On Its Own
    topside_steak = 0
    # Steak with Mushroom Sauce
    if "Steak with Mushroom Sauce" in meal_recipes:
        qty = meal_recipes["Steak with Mushroom Sauce"]["ingredients"].get("Steak", 0)
        meals = meal_totals.get("STEAK WITH MUSHROOM SAUCE", 0)
        topside_steak += qty * meals
    # Steak On Its Own
    if "Steak On Its Own" in meal_recipes:
        qty = meal_recipes["Steak On Its Own"]["ingredients"].get("Steak", 0)
        meals = meal_totals.get("STEAK ON ITS OWN", 0)
        topside_steak += qty * meals

    # Lamb Shoulder - Lamb Shoulder from Lamb Marinate in bulk_sections (Qty/Meal x Meals for relevant meals)
    lamb_shoulder = 0
    for sec in bulk_sections:
        if sec["title"].lower().startswith("lamb marinate"):
            qty = sec["ingredients"].get("Lamb Shoulder", 0)
            meals = 0
            for meal in sec["meals"]:
                meals += meal_totals.get(meal.upper(), 0)
            lamb_shoulder = qty * meals
            break

    # Moroccan Chicken - Chicken from Moroccan Chicken in bulk_sections
    moroccan_chicken = 0
    for sec in bulk_sections:
        if sec["title"].lower().startswith("moroccan chicken"):
            qty = sec["ingredients"].get("Chicken", 0)
            meals = 0
            for meal in sec["meals"]:
                meals += meal_totals.get(meal.upper(), 0)
            moroccan_chicken = qty * meals
            break

    # Italian Chicken - Chicken from Chicken with Vegetables, Chicken Sweet Potato and Beans, Naked Chicken Parma, Chicken On Its Own TIMES 153
    italian_chicken_meals = (
        meal_totals.get("CHICKEN WITH VEGETABLES", 0)
        + meal_totals.get("CHICKEN SWEET POTATO AND BEANS", 0)
        + meal_totals.get("NAKED CHICKEN PARMA", 0)
        + meal_totals.get("CHICKEN ON ITS OWN", 0)
    )
    italian_chicken = italian_chicken_meals * 153

    # Normal Chicken - Chicken from Chicken Pesto Pasta, Butter Chicken, Chicken and Broccoli Pasta, Thai Green Chicken Curry, Creamy Chicken & Mushroom Gnocchi TIMES 130
    normal_chicken_meals = (
        meal_totals.get("CHICKEN PESTO PASTA", 0)
        + meal_totals.get("BUTTER CHICKEN", 0)
        + meal_totals.get("CHICKEN AND BROCCOLI PASTA", 0)
        + meal_totals.get("THAI GREEN CHICKEN CURRY", 0)
        + meal_totals.get("CREAMY CHICKEN & MUSHROOM GNOCCHI", 0)
    )
    normal_chicken = normal_chicken_meals * 130

    # Chicken Thigh - Chicken from Chicken Thigh (in bulk_sections, if it exists)
    chicken_thigh = 0
    for sec in bulk_sections:
        if sec["title"].lower().startswith("chicken thigh"):
            qty = sec["ingredients"].get("Chicken", 0)
            meals = 0
            for meal in sec["meals"]:
                meals += meal_totals.get(meal.upper(), 0)
            chicken_thigh = qty * meals
            break

    # Build and render table
    pdf.set_x(left)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(col_w, ch, "Meat Order", ln=1, fill=True)
    pdf.set_font("Arial", "B", 8)
    for h, w in [("Meat Type", 0.6), ("Amount", 0.4)]:
        pdf.cell(col_w * w, ch, h, 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)

    meats = [
        ("CHUCK ROLL (LEBO)", chuck_roll_lebo),
        ("BEEF TOPSIDE (MONG)", beef_topside_mong),
        ("MINCE", mince),
        ("TOPSIDE STEAK", topside_steak),
        ("LAMB SHOULDER", lamb_shoulder),
        ("MORROCAN CHICKEN", moroccan_chicken),
        ("ITALIAN CHICKEN", italian_chicken),
        ("NORMAL CHICKEN", normal_chicken),
        ("CHICKEN THIGH", chicken_thigh)
    ]
    for meat, amt in meats:
        pdf.set_x(left)
        pdf.cell(col_w * 0.6, ch, meat, 1)
        pdf.cell(col_w * 0.4, ch, str(int(round(amt))), 1)
        pdf.ln(ch)

    # ----------- VEG PREP SECTION (placeholder logic for now) ----------
    veg_prep_types = [
        "10MM DICED CARROT", "10MM DICED POTATO (LEBO)", "10MM DICED ZUCCHINI",
        "5MM DICED CABBAGE", "5MM DICED CAPSICUM", "5MM DICED CARROTS", "5MM DICED CELERY",
        "5MM DICED MUSHROOMS", "5MM DICED ONION", "5MM MONGOLIAN CAPSICUM",
        "5MM MONGOLIAN ONION", "5MM SLICED MUSHROOMS", "BROCCOLI", "CRATED CARROTS",
        "CRATED ZUCCHINI", "LEMON POTATO", "ROASTED POTATO", "THAI POTATOS",
        "POTATO MASH", "SWEET POTATO MASH", "SPINACH", "RED ONION", "PARSLEY"
    ]
    # For now, just fill with 0
    veg_left_y = pdf.get_y() + pad
    pdf.set_y(veg_left_y)
    pdf.set_x(left)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(col_w, ch, "Veg Prep", ln=1, fill=True)
    pdf.set_font("Arial", "B", 8)
    for h, w in [("Veg Prep", 0.7), ("Amount", 0.3)]:
        pdf.cell(col_w * w, ch, h, 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    for veg in veg_prep_types:
        pdf.set_x(left)
        pdf.cell(col_w * 0.7, ch, veg, 1)
        pdf.cell(col_w * 0.3, ch, "0", 1)
        pdf.ln(ch)

    # Return current y position for next section if needed
    return pdf.get_y() + pad
