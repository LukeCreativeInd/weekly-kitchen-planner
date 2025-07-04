import math

def draw_meat_veg_section(pdf, meal_totals, meal_recipes, bulk_sections, xpos, col_w, ch, pad, bottom, start_y=None):
    y = start_y or pdf.get_y()
    pdf.set_y(y)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Meat Order and Veg Prep", ln=1, align="C")
    pdf.ln(3)

    # --------- MEAT ORDER CALCULATIONS ----------
    # Helper to get total for a single ingredient in a meal
    def meal_ing_total(meal, ing, qty=None):
        amt = meal_totals.get(meal, 0)
        if qty is None:
            qty = meal_recipes.get(meal, {}).get("ingredients", {}).get(ing, 0)
        return amt * qty

    # Italian Chicken: Chicken in 4 meals × 153g (use correct names!)
    italian_chicken_meals = [
        "Chicken with Vegetables",
        "Chicken with Sweet Potato and Beans",  # updated as per your message
        "Naked Chicken Parma",
        "Chicken On Its Own"
    ]
    italian_chicken_total_meals = sum(meal_totals.get(m, 0) for m in italian_chicken_meals)
    italian_chicken_amt = italian_chicken_total_meals * 153

    # Normal Chicken: Chicken in 5 meals × 130g
    normal_chicken_meals = [
        "Chicken Pesto Pasta",
        "Chicken and Broccoli Pasta",
        "Butter Chicken",
        "Thai Green Chicken Curry",
        "Creamy Chicken & Mushroom Gnocchi"
    ]
    normal_chicken_total_meals = sum(meal_totals.get(m, 0) for m in normal_chicken_meals)
    normal_chicken_amt = normal_chicken_total_meals * 130

    # Chicken Thigh: from bulk_sections ("Chicken Thigh" table)
    chicken_thigh_amt = 0
    for sec in bulk_sections:
        if sec["title"] == "Chicken Thigh":
            meals = sec.get("meals", [])
            total_meals = sum(meal_totals.get(m, 0) for m in meals)
            chicken_thigh_amt = total_meals * sec["ingredients"].get("Chicken", 0)
            break

    # MEAT ORDER MAPPINGS
    meat_table = [
        ("CHUCK ROLL (LEBO)", meal_ing_total("Lebanese Beef Stew", "Chuck Diced")),
        ("BEEF TOPSIDE (MONG)", meal_ing_total("Mongolian Beef", "Chuck")),
        ("MINCE",
            sum(meal_ing_total(meal, "Beef Mince") for meal in [
                "Spaghetti Bolognese", "Shepherd's Pie", "Beef Chow Mein", "Beef Burrito Bowl"
            ]) + meal_ing_total("Beef Meatballs", "Mince")
        ),
        ("TOPSIDE STEAK", 0),  # To be filled below
        ("LAMB SHOULDER", 0),  # To be filled below
        ("MORROCAN CHICKEN", 0),  # To be filled below
        ("ITALIAN CHICKEN", italian_chicken_amt),
        ("NORMAL CHICKEN", normal_chicken_amt),
        ("CHICKEN THIGH", chicken_thigh_amt),
    ]
    # Fill in bulk-based meats
    # TOPSIDE STEAK from "Steak" in bulk_sections ("Steak" table, "Steak" ingredient)
    topside_steak_amt = 0
    for sec in bulk_sections:
        if sec["title"] == "Steak":
            meals = sec.get("meals", [])
            total_meals = sum(meal_totals.get(m, 0) for m in meals)
            topside_steak_amt = total_meals * sec["ingredients"].get("Steak", 0)
            break
    # LAMB SHOULDER from "Lamb Marinate" bulk section
    lamb_shoulder_amt = 0
    for sec in bulk_sections:
        if sec["title"] == "Lamb Marinate":
            meals = sec.get("meals", [])
            total_meals = sum(meal_totals.get(m, 0) for m in meals)
            lamb_shoulder_amt = total_meals * sec["ingredients"].get("Lamb Shoulder", 0)
            break
    # MORROCAN CHICKEN from "Moroccan Chicken" bulk section
    morrocan_chicken_amt = 0
    for sec in bulk_sections:
        if sec["title"] == "Moroccan Chicken":
            meals = sec.get("meals", [])
            total_meals = sum(meal_totals.get(m, 0) for m in meals)
            morrocan_chicken_amt = total_meals * sec["ingredients"].get("Chicken", 0)
            break

    # Update calculated fields
    meat_table[3] = ("TOPSIDE STEAK", topside_steak_amt)
    meat_table[4] = ("LAMB SHOULDER", lamb_shoulder_amt)
    meat_table[5] = ("MORROCAN CHICKEN", morrocan_chicken_amt)

    # Draw Meat Table
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Meat Order", ln=1, fill=True)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_w * 0.7, ch, "Meat Type", 1)
    pdf.cell(col_w * 0.3, ch, "Amount", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    for meat, amt in meat_table:
        pdf.cell(col_w * 0.7, ch, meat, 1)
        pdf.cell(col_w * 0.3, ch, str(round(amt)), 1)
        pdf.ln(ch)

    # --------- VEG PREP ----------
    pdf.ln(2)
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Veg Prep", ln=1, fill=True)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_w * 0.7, ch, "Veg Prep", 1)
    pdf.cell(col_w * 0.3, ch, "Amount", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    veg_list = [
        "10MM DICED CARROT", "10MM DICED POTATO (LEBO)", "10MM DICED ZUCCHINI",
        "5MM DICED CABBAGE", "5MM DICED CAPSICUM", "5MM DICED CARROTS", "5MM DICED CELERY",
        "5MM DICED MUSHROOMS", "5MM DICED ONION", "5MM MONGOLIAN CAPSICUM",
        "5MM MONGOLIAN ONION", "5MM SLICED MUSHROOMS", "BROCCOLI", "CRATED CARROTS",
        "CRATED ZUCCHINI", "LEMON POTATO", "ROASTED POTATO", "THAI POTATOS",
        "POTATO MASH", "SWEET POTATO MASH", "SPINACH", "RED ONION", "PARSLEY"
    ]
    for veg in veg_list:
        pdf.cell(col_w * 0.7, ch, veg, 1)
        pdf.cell(col_w * 0.3, ch, "0", 1)  # Calculation logic to be added if/when required
        pdf.ln(ch)

    return pdf.get_y() + pad
