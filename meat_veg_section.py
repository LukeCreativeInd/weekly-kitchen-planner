import math

def draw_meat_veg_section(pdf, meal_totals, meal_recipes, bulk_sections, xpos, col_w, ch, pad, bottom, start_y=None):
    y = start_y or pdf.get_y()
    pdf.set_y(y)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Meat Order and Veg Prep", ln=1, align="C")
    pdf.ln(2)

    # --- Meat Order Calculation ---
    def recipe_total(recipe, ingredient):
        data = meal_recipes.get(recipe, {})
        if not data or ingredient not in data["ingredients"]: return 0
        qty_per_meal = data["ingredients"][ingredient]
        meals = meal_totals.get(recipe.upper(), 0)
        return qty_per_meal * meals

    def bulk_total(section_title, ingredient):
        for sec in bulk_sections:
            if sec["title"].upper() == section_title.upper():
                meals = 0
                if "meals" in sec and len(sec["meals"]) > 0:
                    meals = sum(meal_totals.get(m.upper(), 0) for m in sec["meals"])
                if ingredient in sec["ingredients"]:
                    qty_per_meal = sec["ingredients"][ingredient]
                    if meals:
                        return qty_per_meal * meals
                    else:
                        return qty_per_meal
        return 0

    # --- Special calculations for Italian Chicken and Normal Chicken ---
    # Meals for Italian Chicken
    italian_chicken_meals = (
        meal_totals.get("CHICKEN WITH VEGETABLES", 0)
        + meal_totals.get("CHICKEN SWEET POTATO AND BEANS", 0)
        + meal_totals.get("NAKED CHICKEN PARMA", 0)
        + meal_totals.get("CHICKEN ON ITS OWN", 0)
    )
    italian_chicken_total = italian_chicken_meals * 153  # 153g per meal

    # Meals for Normal Chicken
    normal_chicken_meals = (
        meal_totals.get("CHICKEN PESTO PASTA", 0)
        + meal_totals.get("CHICKEN AND BROCCOLI PASTA", 0)
        + meal_totals.get("BUTTER CHICKEN", 0)
        + meal_totals.get("THAI GREEN CHICKEN CURRY", 0)
        + meal_totals.get("CREAMY CHICKEN & MUSHROOM GNOCCHI", 0)
    )
    normal_chicken_total = normal_chicken_meals * 130  # 130g per meal

    meat_rows = [
        ["CHUCK ROLL (LEBO)", recipe_total("Lebanese Beef Stew", "Chuck Diced")],
        ["BEEF TOPSIDE (MONG)", recipe_total("Mongolian Beef", "Chuck")],
        ["MINCE", (
            recipe_total("Spaghetti Bolognese", "Beef Mince") +
            recipe_total("Shepherd's Pie", "Beef Mince") +
            recipe_total("Beef Chow Mein", "Beef Mince") +
            recipe_total("Beef Burrito Bowl", "Beef Mince") +
            recipe_total("Beef Meatballs", "Mince")
        )],
        ["TOPSIDE STEAK", bulk_total("Steak", "Steak")],
        ["LAMB SHOULDER", bulk_total("Lamb Marinate", "Lamb Shoulder")],
        ["MORROCAN CHICKEN", bulk_total("Moroccan Chicken", "Chicken")],
        ["ITALIAN CHICKEN", italian_chicken_total],
        ["NORMAL CHICKEN", normal_chicken_total],
        ["CHICKEN THIGH", bulk_total("Chicken Thigh", "Chicken")],
    ]

    # --- Meat Order Table ---
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Meat Order", ln=1, fill=True)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_w * 0.6, ch, "Meat Type", 1)
    pdf.cell(col_w * 0.4, ch, "Amount", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    for meat, amt in meat_rows:
        pdf.cell(col_w * 0.6, ch, meat, 1)
        pdf.cell(col_w * 0.4, ch, str(round(amt, 2)), 1)
        pdf.ln(ch)

    pdf.ln(4)

    # --- Veg Prep Table (unchanged) ---
    veg_rows = [
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
        "PARSLEY"
    ]
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Veg Prep", ln=1, fill=True)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_w * 0.6, ch, "Veg Prep", 1)
    pdf.cell(col_w * 0.4, ch, "Amount", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    for veg in veg_rows:
        pdf.cell(col_w * 0.6, ch, veg, 1)
        pdf.cell(col_w * 0.4, ch, "0", 1)
        pdf.ln(ch)

    pdf.ln(pad)
    return pdf.get_y()
