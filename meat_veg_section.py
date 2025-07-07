import math

def draw_meat_veg_section(
    pdf, meal_totals, meal_recipes, bulk_sections, xpos, col_w, ch, pad, bottom, start_y=None
):
    y = start_y or pdf.get_y()
    pdf.set_y(y)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Meat Order and Veg Prep", ln=1, align="C")
    pdf.ln(2)

    # 1. Meat Order
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Meat Order", ln=1, fill=True)
    pdf.set_font("Arial", "B", 8)
    for h, w in [("Meat Type", 0.6), ("Amount (g)", 0.4)]:
        pdf.cell(col_w * w, ch, h, 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)

    # Recipe mapping for correct ingredient names
    def get_total_recipe_ingredient(recipe, ingredient):
        data = meal_recipes.get(recipe, {})
        meals = meal_totals.get(recipe.upper(), 0)
        qty = data.get("ingredients", {}).get(ingredient, 0)
        return qty * meals

    def get_total_bulk_ingredient(bulk_title, ingredient):
        section = next((b for b in bulk_sections if b['title'] == bulk_title), None)
        if section:
            total_meals = sum(meal_totals.get(m.upper(), 0) for m in section['meals'])
            qty = section['ingredients'].get(ingredient, 0)
            # For bulk, no batch size means direct multiply
            return qty * total_meals
        return 0

    def sum_totals_recipe_ingredients(recipe_list, ingredient_list):
        total = 0
        for rec in recipe_list:
            data = meal_recipes.get(rec, {})
            meals = meal_totals.get(rec.upper(), 0)
            for ing in ingredient_list:
                qty = data.get("ingredients", {}).get(ing, 0)
                total += qty * meals
        return total

    meat_order = [
        ("CHUCK ROLL (LEBO)", get_total_recipe_ingredient("Lebanese Beef Stew", "Chuck Diced")),
        ("BEEF TOPSIDE (MONG)", get_total_recipe_ingredient("Mongolian Beef", "Chuck")),
        ("MINCE", sum_totals_recipe_ingredients(
            ["Spaghetti Bolognese", "Shepherd's Pie", "Beef Chow Mein", "Beef Burrito Bowl"], ["Beef Mince"])
            + get_total_recipe_ingredient("Beef Meatballs", "Mince")),
        ("TOPSIDE STEAK", get_total_bulk_ingredient("Steak", "Steak")),
        ("LAMB SHOULDER", get_total_bulk_ingredient("Lamb Marinate", "Lamb Shoulder")),
        ("MORROCAN CHICKEN", get_total_bulk_ingredient("Moroccan Chicken", "Chicken")),
        ("ITALIAN CHICKEN", sum_totals_recipe_ingredients(
            ["Chicken With Vegetables", "Chicken with Sweet Potato and Beans", "Naked Chicken Parma", "Chicken On Its Own"], ["Chicken"])),
        ("NORMAL CHICKEN", sum_totals_recipe_ingredients(
            ["Chicken Pesto Pasta", "Chicken and Broccoli Pasta", "Butter Chicken", "Thai Green Chicken Curry", "Creamy Chicken & Mushroom Gnocchi"], ["Chicken"])),
        ("CHICKEN THIGH", get_total_bulk_ingredient("Chicken Thigh", "Chicken")),
    ]

    for mtype, amt in meat_order:
        pdf.cell(col_w * 0.6, ch, mtype, 1)
        pdf.cell(col_w * 0.4, ch, str(int(round(amt))), 1)
        pdf.ln(ch)
    pdf.ln(6)

    # 2. Veg Prep
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Veg Prep", ln=1, fill=True)
    pdf.set_font("Arial", "B", 8)
    for h, w in [("Veg Prep", 0.7), ("Amount (g)", 0.3)]:
        pdf.cell(col_w * w, ch, h, 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)

    # --- Veg Prep Calculations ---

    veg_prep = [
        # Each row: (label, total calculated)
        ("10MM DICED CARROT", get_total_recipe_ingredient("Lebanese Beef Stew", "Carrot")),
        ("10MM DICED POTATO (LEBO)", get_total_recipe_ingredient("Lebanese Beef Stew", "Potato")),
        ("10MM DICED ZUCCHINI", meal_recipes.get("Moroccan Chicken", {}).get("sub_section", {}).get("ingredients", {}).get("Zucchini", 0) * meal_totals.get("MOROCCAN CHICKEN".upper(), 0)),
        ("5MM DICED CABBAGE", get_total_recipe_ingredient("Beef Chow Mein", "Cabbage")),
        ("5MM DICED CAPSICUM",
            get_total_recipe_ingredient("Shepherd's Pie", "Capsicum")
            + get_total_recipe_ingredient("Beef Burrito Bowl", "Capsicum")
            + meal_recipes.get("Moroccan Chicken", {}).get("sub_section", {}).get("ingredients", {}).get("Red Capsicum", 0) * meal_totals.get("MOROCCAN CHICKEN".upper(), 0)),
        ("5MM DICED CARROTS",
            get_total_recipe_ingredient("Shepherd's Pie", "Carrots")
            + get_total_recipe_ingredient("Beef Burrito Bowl", "Carrot")),
        ("5MM DICED CELERY", get_total_recipe_ingredient("Beef Chow Mein", "Celery")),
        ("5MM DICED MUSHROOMS", get_total_recipe_ingredient("Shepherd's Pie", "Mushroom")),
        ("5MM DICED ONION",
            get_total_recipe_ingredient("Spaghetti Bolognese", "Onion")
            + get_total_recipe_ingredient("Beef Chow Mein", "Onion")
            + get_total_recipe_ingredient("Shepherd's Pie", "Onion")
            + get_total_recipe_ingredient("Beef Burrito Bowl", "Onion")
            + get_total_recipe_ingredient("Beef Meatballs", "Onion")
            + get_total_recipe_ingredient("Lebanese Beef Stew", "Onion")
            + meal_recipes.get("Moroccan Chicken", {}).get("sub_section", {}).get("ingredients", {}).get("Onion", 0) * meal_totals.get("MOROCCAN CHICKEN".upper(), 0)
            + get_total_recipe_ingredient("Bean Nachos with Rice", "Onion")
        ),
        ("5MM MONGOLIAN CAPSICUM", get_total_recipe_ingredient("Mongolian Beef", "Capsicum")),
        ("5MM MONGOLIAN ONION", get_total_recipe_ingredient("Mongolian Beef", "Onion")),
        ("5MM SLICED MUSHROOMS", 0),
        ("BROCCOLI", get_total_recipe_ingredient("Chicken and Broccoli Pasta", "Broccoli")),
        ("CRATED CARROTS",
            get_total_recipe_ingredient("Spaghetti Bolognese", "Carrot")
            + get_total_recipe_ingredient("Bean Nachos with Rice", "Carrot")),
        ("CRATED ZUCCHINI", get_total_recipe_ingredient("Spaghetti Bolognese", "Zucchini")),
        ("LEMON POTATO", get_total_bulk_ingredient("Roasted Lemon Potatoes", "Potatoes")),
        ("ROASTED POTATO", get_total_bulk_ingredient("Roasted Potatoes", "Roasted Potatoes")),
        ("THAI POTATOS", get_total_bulk_ingredient("Roasted Thai Potatoes", "Potato")),
        ("POTATO MASH", get_total_bulk_ingredient("Potato Mash", "Potato")),
        ("SWEET POTATO MASH", get_total_bulk_ingredient("Sweet Potato Mash", "Sweet Potato")),
        # Spinach (Gnocchi, Chicken Mixing) - use standard logic or add specific
        ("SPINACH", 25 * meal_totals.get("CREAMY CHICKEN & MUSHROOM GNOCCHI".upper(), 0)),
        ("RED ONION", get_total_bulk_ingredient("Lamb Onion Marinated", "Red Onion")),
        ("PARSLEY", get_total_bulk_ingredient("Lamb Onion Marinated", "Parsley")),
    ]

    for veg, amt in veg_prep:
        pdf.cell(col_w * 0.7, ch, veg, 1)
        pdf.cell(col_w * 0.3, ch, str(int(round(amt))), 1)
        pdf.ln(ch)

    pdf.ln(4)
    return pdf.get_y()
