import math

def draw_meat_veg_section(pdf, meal_totals, meal_recipes, bulk_sections, xpos, col_w, ch, pad, bottom, start_y=None):
    # Start at the right Y position
    y = start_y or pdf.get_y()
    pdf.set_y(y)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Meat Order and Veg Prep", ln=1, align="C")
    pdf.ln(2)

    # Helper function: Get total for a recipe ingredient
    def recipe_ingredient_total(recipe_name, ingredient):
        rec = meal_recipes.get(recipe_name)
        if rec and ingredient in rec["ingredients"]:
            qty_per_meal = rec["ingredients"][ingredient]
            meal_count = meal_totals.get(recipe_name.upper(), 0)
            return qty_per_meal * meal_count
        return 0

    # Helper: total for ingredient across multiple recipes
    def recipe_multi_total(recipe_names, ingredient):
        return sum(recipe_ingredient_total(r, ingredient) for r in recipe_names)

    # Helper: Get total from bulk sections by ingredient and table
    def bulk_section_total(section_title, ingredient):
        for sec in bulk_sections:
            if sec['title'] == section_title and ingredient in sec['ingredients']:
                qty_per_meal = sec['ingredients'][ingredient]
                total_meals = sum(meal_totals.get(m.upper(), 0) for m in sec['meals'])
                return qty_per_meal * total_meals
        return 0

    # Names as in your product_quantity_summary.xlsx (update as needed if you see discrepancies)
    meat_table = [
        ("CHUCK ROLL (LEBO)", recipe_ingredient_total("Lebanese Beef Stew", "Chuck Diced")),
        ("BEEF TOPSIDE (MONG)", recipe_ingredient_total("Mongolian Beef", "Chuck")),
        ("MINCE", sum([
            recipe_ingredient_total("Spaghetti Bolognese", "Beef Mince"),
            recipe_ingredient_total("Shepherd's Pie", "Beef Mince"),
            recipe_ingredient_total("Beef Chow Mein", "Beef Mince"),
            recipe_ingredient_total("Beef Burrito Bowl", "Beef Mince"),
            recipe_ingredient_total("Beef Meatballs", "Mince")
        ])),
        ("TOPSIDE STEAK", sum([
            recipe_ingredient_total("Steak with Mushroom Sauce", "Topside Steak"),
            recipe_ingredient_total("Steak On Its Own", "Topside Steak"),
        ])),
        ("LAMB SHOULDER", sum([
            bulk_section_total("Lamb Marinate", "Lamb Shoulder"),
            recipe_ingredient_total("Lamb Souvlaki", "Lamb Shoulder"),
        ])),
        ("MORROCAN CHICKEN", bulk_section_total("Moroccan Chicken", "Chicken")),
        # Italian Chicken: combo of several
        ("ITALIAN CHICKEN", sum([
            recipe_ingredient_total("Chicken With Vegetables", "Chicken"),
            recipe_ingredient_total("Chicken with Sweet Potato and Beans", "Chicken"),
            recipe_ingredient_total("Naked Chicken Parma", "Chicken"),
            recipe_ingredient_total("Chicken On Its Own", "Chicken Breast")
        ])),
        # Normal Chicken: combo of several
        ("NORMAL CHICKEN", sum([
            recipe_ingredient_total("Chicken Pesto Pasta", "Chicken"),
            recipe_ingredient_total("Chicken and Broccoli Pasta", "Chicken"),
            recipe_ingredient_total("Butter Chicken", "Chicken"),
            recipe_ingredient_total("Thai Green Chicken Curry", "Chicken"),
            recipe_ingredient_total("Creamy Chicken & Mushroom Gnocchi", "Chicken")
        ])),
        ("CHICKEN THIGH", recipe_ingredient_total("Chicken Fajita Bowl", "Chicken Thigh"))
    ]

    # Draw table
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Meat Order", ln=1, fill=True)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_w*0.65, ch, "Meat Type", 1)
    pdf.cell(col_w*0.35, ch, "Amount (g)", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    for mtype, amt in meat_table:
        pdf.cell(col_w*0.65, ch, mtype, 1)
        pdf.cell(col_w*0.35, ch, f"{int(amt):,}" if amt else "0", 1)
        pdf.ln(ch)

    # Veg prep as before (fill with zeros or actual logic later)
    veg_table = [
        "10MM DICED CARROT", "10MM DICED POTATO (LEBO)", "10MM DICED ZUCCHINI",
        "5MM DICED CABBAGE", "5MM DICED CAPSICUM", "5MM DICED CARROTS", "5MM DICED CELERY",
        "5MM DICED MUSHROOMS", "5MM DICED ONION", "5MM MONGOLIAN CAPSICUM", "5MM MONGOLIAN ONION",
        "5MM SLICED MUSHROOMS", "BROCCOLI", "CRATED CARROTS", "CRATED ZUCCHINI", "LEMON POTATO",
        "ROASTED POTATO", "THAI POTATOS", "POTATO MASH", "SWEET POTATO MASH", "SPINACH", "RED ONION", "PARSLEY"
    ]
    pdf.ln(3)
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Veg Prep", ln=1, fill=True)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_w*0.65, ch, "Veg Prep", 1)
    pdf.cell(col_w*0.35, ch, "Amount (g)", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    for veg in veg_table:
        pdf.cell(col_w*0.65, ch, veg, 1)
        pdf.cell(col_w*0.35, ch, "0", 1)
        pdf.ln(ch)

    # Return current y position for next section
    return pdf.get_y() + pad
