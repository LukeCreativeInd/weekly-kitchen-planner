import math

def draw_meat_veg_section(pdf, meal_totals, meal_recipes, bulk_sections, xpos, col_w, ch, pad, bottom, start_y=None):
    y = start_y or pdf.get_y()
    pdf.set_y(y)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Meat Order and Veg Prep", ln=1, align="C")
    pdf.ln(2)

    # --- MEAT ORDER ---
    meat_rows = []

    # CHUCK ROLL (LEBO)
    stew = meal_recipes["Lebanese Beef Stew"]["ingredients"]
    stew_qty = stew.get("Chuck Diced", 0)
    stew_meals = meal_totals.get("LEBANESE BEEF STEW", 0)
    chuck_roll_lebo = stew_qty * stew_meals
    meat_rows.append(("CHUCK ROLL (LEBO)", chuck_roll_lebo))

    # BEEF TOPSIDE (MONG)
    mong = meal_recipes["Mongolian Beef"]["ingredients"]
    mong_qty = mong.get("Chuck", 0)
    mong_meals = meal_totals.get("MONGOLIAN BEEF", 0)
    beef_topside_mong = mong_qty * mong_meals
    meat_rows.append(("BEEF TOPSIDE (MONG)", beef_topside_mong))

    # MINCE - add up for all relevant recipes
    mince_total = 0
    mince_recipes = [
        ("Spaghetti Bolognese", "Beef Mince"),
        ("Shepherd's Pie", "Beef Mince"),
        ("Beef Chow Mein", "Beef Mince"),
        ("Beef Burrito Bowl", "Beef Mince"),
        ("Beef Meatballs", "Mince"),
    ]
    for recipe, ingredient in mince_recipes:
        if recipe in meal_recipes:
            rec = meal_recipes[recipe]
            qty = rec["ingredients"].get(ingredient, 0)
            meals = meal_totals.get(recipe.upper(), 0)
            mince_total += qty * meals
    meat_rows.append(("MINCE", mince_total))

    # TOPSIDE STEAK (from Steak in bulk area)
    steak_sec = next((s for s in bulk_sections if s["title"].lower().startswith("steak")), None)
    if steak_sec:
        steak_qty = steak_sec["ingredients"].get("Steak", 0)
        steak_meals = sum(meal_totals.get(m.upper(), 0) for m in steak_sec["meals"])
        topside_steak = steak_qty * steak_meals
    else:
        topside_steak = 0
    meat_rows.append(("TOPSIDE STEAK", topside_steak))

    # LAMB SHOULDER
    lamb_sec = next((s for s in bulk_sections if s["title"].lower().startswith("lamb marinate")), None)
    if lamb_sec:
        lamb_qty = lamb_sec["ingredients"].get("Lamb Shoulder", 0)
        lamb_meals = sum(meal_totals.get(m.upper(), 0) for m in lamb_sec["meals"])
        lamb_shoulder = lamb_qty * lamb_meals
    else:
        lamb_shoulder = 0
    meat_rows.append(("LAMB SHOULDER", lamb_shoulder))

    # MOROCCAN CHICKEN
    moro_sec = next((s for s in bulk_sections if s["title"].lower().startswith("moroccan chicken")), None)
    if moro_sec:
        moro_qty = moro_sec["ingredients"].get("Chicken", 0)
        moro_meals = sum(meal_totals.get(m.upper(), 0) for m in moro_sec["meals"])
        moro_chicken = moro_qty * moro_meals
    else:
        moro_chicken = 0
    meat_rows.append(("MORROCAN CHICKEN", moro_chicken))

    # Remaining three
    meat_rows.append(("ITALIAN CHICKEN", 0))
    meat_rows.append(("NORMAL CHICKEN", 0))
    meat_rows.append(("CHICKEN THIGH", 0))

    # Draw table
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Meat Type", 1, 0, "L", True)
    pdf.cell(col_w, ch, "Amount", 1, 1, "L", True)
    pdf.set_font("Arial", "", 10)
    for mt, amt in meat_rows:
        pdf.cell(col_w, ch, mt, 1)
        pdf.cell(col_w, ch, str(amt), 1)
        pdf.ln(ch)

    # (Veg prep table as per your previous logic...)

    return pdf.get_y() + pad
