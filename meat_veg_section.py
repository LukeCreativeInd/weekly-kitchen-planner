import math

def draw_meat_veg_section(
    pdf, meal_totals, meal_recipes, bulk_sections, xpos, col_w, ch, pad, bottom, start_y=None
):
    # Always start a new page for this section!
    pdf.add_page()
    pdf.set_y(10)
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
            return qty * total_meals
        return 0

    def sum_totals_recipe_ingredients(recipe_list, ingredient, ingredient_override=None):
        total = 0
        for rec in recipe_list:
            data = meal_recipes.get(rec, {})
            meals = meal_totals.get(rec.upper(), 0)
            ing = ingredient_override if ingredient_override else ingredient
            qty = data.get("ingredients", {}).get(ing, 0)
            total += qty * meals
        return total

    meat_order = [
        ("CHUCK ROLL (LEBO)", get_total_recipe_ingredient("Lebanese Beef Stew", "Chuck Diced")),
        ("BEEF TOPSIDE (MONG)", get_total_recipe_ingredient("Mongolian Beef", "Chuck")),
        ("MINCE", sum_totals_recipe_ingredients(
            ["Spaghetti Bolognese", "Shepherd's Pie", "Beef Chow Mein", "Beef Burrito Bowl"], "Beef Mince") +
            sum_totals_recipe_ingredients(["Beef Meatballs"], "Mince")),
        ("TOPSIDE STEAK", get_total_bulk_ingredient("Steak", "Steak")),
        ("LAMB SHOULDER", get_total_bulk_ingredient("Lamb Marinate", "Lamb Shoulder")),
        ("MORROCAN CHICKEN", get_total_bulk_ingredient("Moroccan Chicken", "Chicken")),
        ("ITALIAN CHICKEN", sum_totals_recipe_ingredients(
            ["Chicken With Vegetables", "Chicken Sweet Potato and Beans", "Naked Chicken Parma", "Chicken On Its Own"], "Chicken")),
        ("NORMAL CHICKEN", sum_totals_recipe_ingredients(
            ["Chicken Pesto Pasta", "Chicken and Broccoli Pasta", "Butter Chicken", "Thai Green Chicken Curry", "Creamy Chicken & Mushroom Gnocchi"], "Chicken")),
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

    # Helper: get batch total from meal recipe table
    def get_batch_total(recipe, ingredient):
        data = meal_recipes.get(recipe, {})
        meals = meal_totals.get(recipe.upper(), 0)
        qty = data.get("ingredients", {}).get(ingredient, 0)
        batch = data.get("batch", 0)
        return qty * meals  # adjust as needed if you use batch

    def get_bulk_total(bulk_title, ingredient):
        section = next((b for b in bulk_sections if b['title'] == bulk_title), None)
        if section:
            total_meals = sum(meal_totals.get(m.upper(), 0) for m in section['meals'])
            qty = section['ingredients'].get(ingredient, 0)
            return qty * total_meals
        return 0

    def get_total_from_chicken_mixing():
        meals = meal_totals.get("CREAMY CHICKEN & MUSHROOM GNOCCHI".upper(), 0)
        qty = 25
        return qty * meals

    veg_prep = [
        ("10MM DICED CARROT", get_batch_total("Lebanese Beef Stew", "Carrot")),
        ("10MM DICED POTATO (LEBO)", get_batch_total("Lebanese Beef Stew", "Potato")),
        ("10MM DICED ZUCCHINI", meal_recipes["Moroccan Chicken"]["sub_section"]["ingredients"].get("Zucchini", 0) * meal_totals.get("MOROCCAN CHICKEN".upper(), 0)),
        ("5MM DICED CABBAGE", get_batch_total("Beef Chow Mein", "Cabbage")),
        ("5MM DICED CAPSICUM", get_batch_total("Shepherd's Pie", "Capsicum") + get_batch_total("Beef Burrito Bowl", "Capsicum") + (meal_recipes.get("Moroccan Chicken", {}).get("sub_section", {}).get("ingredients", {}).get("Red Capsicum", 0) * meal_totals.get("MOROCCAN CHICKEN".upper(), 0))),
        ("5MM DICED CARROTS", get_batch_total("Shepherd's Pie", "Carrots") + get_batch_total("Beef Burrito Bowl", "Carrot")),
        ("5MM DICED CELERY", get_batch_total("Beef Chow Mein", "Celery")),
        ("5MM DICED MUSHROOMS", get_batch_total("Shepherd's Pie", "Mushroom")),
        ("5MM DICED ONION", 0),
        ("5MM MONGOLIAN CAPSICUM", get_batch_total("Mongolian Beef", "Capsicum")),
        ("5MM MONGOLIAN ONION", get_batch_total("Mongolian Beef", "Onion")),
        ("5MM SLICED MUSHROOMS", 0),
        ("BROCCOLI", get_batch_total("Chicken and Broccoli Pasta", "Broccoli")),
        ("CRATED CARROTS", get_batch_total("Spaghetti Bolognese", "Carrot")),
        ("CRATED ZUCCHINI", get_batch_total("Spaghetti Bolognese", "Zucchini")),
        ("LEMON POTATO", get_bulk_total("Roasted Lemon Potatoes", "Potatoes")),
        ("ROASTED POTATO", get_bulk_total("Roasted Potatoes", "Roasted Potatoes")),
        ("THAI POTATOS", get_bulk_total("Roasted Thai Potatoes", "Potato")),
        ("POTATO MASH", get_bulk_total("Potato Mash", "Potato")),
        ("SWEET POTATO MASH", get_bulk_total("Sweet Potato Mash", "Sweet Potato")),
        ("SPINACH", get_total_from_chicken_mixing()),
        ("RED ONION", get_bulk_total("Lamb Onion Marinated", "Red Onion")),
        ("PARSLEY", get_bulk_total("Lamb Onion Marinated", "Parsley")),
    ]

    for veg, amt in veg_prep:
        pdf.cell(col_w * 0.7, ch, veg, 1)
        pdf.cell(col_w * 0.3, ch, str(int(round(amt))), 1)
        pdf.ln(ch)

    pdf.ln(4)
    return pdf.get_y()
