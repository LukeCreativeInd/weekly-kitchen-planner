import math

def draw_meat_veg_section(
    pdf, meal_totals, meal_recipes, bulk_sections, xpos, col_w, ch, pad, bottom, start_y=None
):
    # Start on new page for safety, and position y accordingly
    pdf.add_page()
    y = start_y or pdf.get_y()
    pdf.set_y(y)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Meat Order and Veg Prep", ln=1, align="C")
    pdf.ln(2)
    y = pdf.get_y()
    left_x, right_x = xpos[0], xpos[1]

    # --- MEAT ORDER ---

    # Helper to get Qty/Meal from a recipe's ingredient
    def get_qty_meal(recipe_name, ing_name):
        data = meal_recipes.get(recipe_name, {})
        return data.get("ingredients", {}).get(ing_name, 0)

    # Helper to get number of meals from meal_totals (by exact product name)
    def get_meals(product):
        return meal_totals.get(product.upper(), 0)

    # -- CHICKEN GROUPS for Italian Chicken and Normal Chicken --
    # Italian Chicken = Chicken with Vegetables, Chicken with Sweet Potato and Beans, Naked Chicken Parma, Chicken On Its Own
    italian_chicken_meals = [
        "Chicken with Vegetables",
        "Chicken with Sweet Potato and Beans",
        "Naked Chicken Parma",
        "Chicken On Its Own",
    ]
    italian_chicken_total_meals = sum(get_meals(name) for name in italian_chicken_meals)
    italian_chicken_total = italian_chicken_total_meals * 153

    # Normal Chicken = Chicken Pesto Pasta, Butter Chicken, Chicken and Broccoli Pasta, Thai Green Chicken Curry, Creamy Chicken & Mushroom Gnocchi
    normal_chicken_meals = [
        "Chicken Pesto Pasta",
        "Chicken and Broccoli Pasta",
        "Butter Chicken",
        "Thai Green Chicken Curry",
        "Creamy Chicken & Mushroom Gnocchi"
    ]
    normal_chicken_total_meals = sum(get_meals(name) for name in normal_chicken_meals)
    normal_chicken_total = normal_chicken_total_meals * 130

    # CHICKEN THIGH is pulled from bulk_section "Chicken Thigh" table and "Chicken" row (see bulk_sections structure)
    def get_bulk_total(section_title, ing_name):
        # Find bulk section by title
        for sec in bulk_sections:
            if sec["title"] == section_title:
                qty_per = sec["ingredients"].get(ing_name, 0)
                total_meals = sum(get_meals(m) for m in sec["meals"])
                return qty_per * total_meals
        return 0

    meat_order = [
        ("CHUCK ROLL (LEBO)",
         get_qty_meal("Lebanese Beef Stew", "Chuck Diced") * get_meals("Lebanese Beef Stew")),
        ("BEEF TOPSIDE (MONG)",
         get_qty_meal("Mongolian Beef", "Chuck") * get_meals("Mongolian Beef")),
        ("MINCE",
         sum(get_qty_meal(m, "Beef Mince") * get_meals(m) for m in [
             "Spaghetti Bolognese", "Beef Chow Mein", "Shepherd's Pie", "Beef Burrito Bowl"]) +
         get_qty_meal("Beef Meatballs", "Mince") * get_meals("Beef Meatballs")),
        ("TOPSIDE STEAK",
         get_bulk_total("Steak", "Steak")),
        ("LAMB SHOULDER",
         get_bulk_total("Lamb Marinate", "Lamb Shoulder")),
        ("MORROCAN CHICKEN",
         get_bulk_total("Moroccan Chicken", "Chicken")),
        ("ITALIAN CHICKEN", italian_chicken_total),
        ("NORMAL CHICKEN", normal_chicken_total),
        ("CHICKEN THIGH", get_bulk_total("Chicken Thigh", "Chicken")),
    ]

    # --- Render Meat Order table ---
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.set_xy(left_x, y)
    pdf.cell(col_w, ch, "Meat Order", ln=1, fill=True)
    pdf.set_x(left_x)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_w * 0.7, ch, "Meat Type", 1)
    pdf.cell(col_w * 0.3, ch, "Amount (g)", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    for name, amount in meat_order:
        pdf.set_x(left_x)
        pdf.cell(col_w * 0.7, ch, name, 1)
        pdf.cell(col_w * 0.3, ch, str(int(round(amount))), 1)
        pdf.ln(ch)
    meat_end_y = pdf.get_y()

    # --- VEG PREP TABLE (unchanged, still all zero for now) ---
    veg_prep = [
        "10MM DICED CARROT", "10MM DICED POTATO (LEBO)", "10MM DICED ZUCCHINI",
        "5MM DICED CABBAGE", "5MM DICED CAPSICUM", "5MM DICED CARROTS", "5MM DICED CELERY",
        "5MM DICED MUSHROOMS", "5MM DICED ONION", "5MM MONGOLIAN CAPSICUM", "5MM MONGOLIAN ONION",
        "5MM SLICED MUSHROOMS", "BROCCOLI", "CRATED CARROTS", "CRATED ZUCCHINI", "LEMON POTATO",
        "ROASTED POTATO", "THAI POTATOS", "POTATO MASH", "SWEET POTATO MASH", "SPINACH", "RED ONION", "PARSLEY"
    ]
    veg_start_y = y
    if meat_end_y > y:
        veg_start_y = meat_end_y + 2

    pdf.set_xy(right_x, veg_start_y)
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Veg Prep", ln=1, fill=True)
    pdf.set_x(right_x)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_w * 0.7, ch, "Veg Prep", 1)
    pdf.cell(col_w * 0.3, ch, "Amount (g)", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    for veg in veg_prep:
        pdf.set_x(right_x)
        pdf.cell(col_w * 0.7, ch, veg, 1)
        pdf.cell(col_w * 0.3, ch, "0", 1)
        pdf.ln(ch)

    # Return lowest y (for completeness if chaining sections, but not required)
    return max(meat_end_y, pdf.get_y())
