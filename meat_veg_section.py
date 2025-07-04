import math

def draw_meat_veg_section(
    pdf, meal_totals, meal_recipes, bulk_sections, xpos, col_w, ch, pad, bottom, start_y=None
):
    # Helper to get meal total times quantity per meal
    def total_ingredient(meal, ingredient, qty_override=None):
        meals = meal_totals.get(meal.upper(), 0)
        qty = qty_override if qty_override is not None else meal_recipes.get(meal, {}).get('ingredients', {}).get(ingredient, 0)
        return meals * qty

    # Calculate all meat values
    meat_order = [
        ("CHUCK ROLL (LEBO)", total_ingredient("Lebanese Beef Stew", "Chuck Diced")),
        ("BEEF TOPSIDE (MONG)", total_ingredient("Mongolian Beef", "Chuck")),
        ("MINCE", sum([
            total_ingredient("Spaghetti Bolognese", "Beef Mince"),
            total_ingredient("Shepherd's Pie", "Beef Mince"),
            total_ingredient("Beef Chow Mein", "Beef Mince"),
            total_ingredient("Beef Burrito Bowl", "Beef Mince"),
            total_ingredient("Beef Meatballs", "Mince")
        ])),
        ("TOPSIDE STEAK", sum([
            total_ingredient("Steak with Mushroom Sauce", "Topside Steak"),
            total_ingredient("Steak On Its Own", "Topside Steak")
        ])),
        ("LAMB SHOULDER", sum([
            s['ingredients']['Lamb Shoulder'] * meal_totals.get(m.upper(), 0)
            for s in bulk_sections if s['title'] == "Lamb Marinate"
            for m in s['meals']
        ])),
        ("MORROCAN CHICKEN", sum([
            s['ingredients']['Chicken'] * meal_totals.get(m.upper(), 0)
            for s in bulk_sections if s['title'] == "Moroccan Chicken"
            for m in s['meals']
        ])),
        ("ITALIAN CHICKEN", sum([
            total_ingredient("Chicken with Vegetables", "Chicken", 153),
            total_ingredient("Chicken with Sweet Potato and Beans", "Chicken", 153),
            total_ingredient("Naked Chicken Parma", "Chicken", 153),
            total_ingredient("Chicken On Its Own", "Chicken Breast", 153)  # adjust if needed
        ])),
        ("NORMAL CHICKEN", sum([
            total_ingredient("Chicken Pesto Pasta", "Chicken", 130),
            total_ingredient("Chicken and Broccoli Pasta", "Chicken", 130),
            total_ingredient("Butter Chicken", "Chicken", 130),
            total_ingredient("Thai Green Chicken Curry", "Chicken", 130),
            total_ingredient("Creamy Chicken & Mushroom Gnocchi", "Chicken", 130)
        ])),
        ("CHICKEN THIGH", sum([
            s['ingredients']['Chicken'] * meal_totals.get(m.upper(), 0)
            for s in bulk_sections if s['title'] == "Chicken Thigh"
            for m in s['meals']
        ]) if any(s['title'] == "Chicken Thigh" for s in bulk_sections) else 0)
    ]

    # Start at new page if too close to bottom
    if start_y is not None:
        if start_y + (len(meat_order) + 8) * ch > bottom:
            pdf.add_page()
            y = pdf.get_y()
        else:
            y = start_y
    else:
        y = pdf.get_y()

    pdf.set_y(y)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Meat Order and Veg Prep", ln=1, align="C")
    pdf.ln(2)

    # --- Meat Order Table ---
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Meat Order", ln=1, fill=True)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_w * 0.7, ch, "Meat Type", 1)
    pdf.cell(col_w * 0.3, ch, "Amount (g)", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    for meat, amt in meat_order:
        pdf.cell(col_w * 0.7, ch, meat, 1)
        pdf.cell(col_w * 0.3, ch, f"{int(amt):,}" if amt else "0", 1)
        pdf.ln(ch)

    pdf.ln(4)

    # --- Veg Prep Table ---
    veg_preps = [
        "10MM DICED CARROT", "10MM DICED POTATO (LEBO)", "10MM DICED ZUCCHINI", "5MM DICED CABBAGE",
        "5MM DICED CAPSICUM", "5MM DICED CARROTS", "5MM DICED CELERY", "5MM DICED MUSHROOMS",
        "5MM DICED ONION", "5MM MONGOLIAN CAPSICUM", "5MM MONGOLIAN ONION", "5MM SLICED MUSHROOMS",
        "BROCCOLI", "CRATED CARROTS", "CRATED ZUCCHINI", "LEMON POTATO", "ROASTED POTATO",
        "THAI POTATOS", "POTATO MASH", "SWEET POTATO MASH", "SPINACH", "RED ONION", "PARSLEY"
    ]
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Veg Prep", ln=1, fill=True)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_w * 0.7, ch, "Veg Prep", 1)
    pdf.cell(col_w * 0.3, ch, "Amount (g)", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    for veg in veg_preps:
        pdf.cell(col_w * 0.7, ch, veg, 1)
        pdf.cell(col_w * 0.3, ch, "0", 1)
        pdf.ln(ch)

    return pdf.get_y() + pad
