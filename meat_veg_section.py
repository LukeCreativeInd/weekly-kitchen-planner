import math

def draw_meat_veg_section(
    pdf, meal_totals, meal_recipes, bulk_sections, chicken_mixing_data,
    xpos, col_w, ch, pad, bottom, start_y=None
):
    y = start_y or pdf.get_y()
    pdf.set_y(y)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Meat Order and Veg Prep", ln=1, align="C")
    pdf.ln(2)

    left_x, right_x = xpos
    curr_y = pdf.get_y()

    # --- MEAT ORDER LOGIC ---
    def get_total_from_recipe(recipe_name, ing, default_batch=None):
        rec = meal_recipes.get(recipe_name)
        if not rec: return 0
        qty_per_meal = rec["ingredients"].get(ing, 0)
        tot_meals = meal_totals.get(recipe_name.upper(), 0)
        batch = rec.get("batch", 0) if rec.get("batch", 0) > 0 else default_batch or 1
        return qty_per_meal * tot_meals

    def get_total_from_bulk(title, ing):
        for section in bulk_sections:
            if section["title"] == title:
                qty_per_meal = section["ingredients"].get(ing, 0)
                tot_meals = sum(meal_totals.get(m.upper(),0) for m in section["meals"])
                batch_size = section.get("batch_size", 0)
                batches = math.ceil(tot_meals / batch_size) if batch_size > 0 else 1
                return qty_per_meal * tot_meals
        return 0

    def get_total_from_chicken_mixing(mix_name, ing):
        mix = chicken_mixing_data.get(mix_name)
        if not mix: return 0
        qty_per_meal = dict(mix["ingredients"]).get(ing, 0)
        tot_meals = meal_totals.get(mix["meal"], 0)
        divisor = mix.get("divisor", 1)
        raw_b = math.ceil(tot_meals / divisor) if divisor > 0 else 1
        batches = raw_b + (raw_b % 2)
        return qty_per_meal * tot_meals if batches else 0

    meat_types = [
        ("CHUCK ROLL (LEBO)", get_total_from_recipe("Lebanese Beef Stew", "Chuck Diced")),
        ("BEEF TOPSIDE (MONG)", get_total_from_recipe("Mongolian Beef", "Chuck")),
        ("MINCE",
         sum(get_total_from_recipe(name, "Beef Mince")
             for name in ["Spaghetti Bolognese", "Shepherd's Pie", "Beef Chow Mein", "Beef Burrito Bowl"]) +
         get_total_from_recipe("Beef Meatballs", "Mince")
        ),
        ("TOPSIDE STEAK", get_total_from_bulk("Steak", "Steak")),
        ("LAMB SHOULDER", get_total_from_bulk("Lamb Marinate", "Lamb Shoulder")),
        ("MORROCAN CHICKEN", get_total_from_bulk("Moroccan Chicken", "Chicken")),
        # ITALIAN CHICKEN: Chicken With Vegetables, Chicken with Sweet Potato and Beans, Naked Chicken Parma, Chicken On Its Own
        ("ITALIAN CHICKEN", sum(get_total_from_recipe(n, "Chicken")
            for n in ["Chicken With Vegetables", "Chicken with Sweet Potato and Beans", "Naked Chicken Parma", "Chicken On Its Own"]
        )),
        # NORMAL CHICKEN: Chicken Pesto Pasta, Butter Chicken, Chicken and Broccoli Pasta, Thai Green Chicken Curry, Creamy Chicken & Mushroom Gnocchi
        ("NORMAL CHICKEN", sum(get_total_from_recipe(n, "Chicken")
            for n in ["Chicken Pesto Pasta", "Butter Chicken", "Chicken and Broccoli Pasta", "Thai Green Chicken Curry", "Creamy Chicken & Mushroom Gnocchi"]
        )),
        # CHICKEN THIGH: Chicken row from Chicken Thigh (assumed to be bulk section title)
        ("CHICKEN THIGH", get_total_from_bulk("Chicken Thigh", "Chicken"))
    ]

    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.set_xy(left_x, curr_y)
    pdf.cell(col_w, ch, "Meat Order", ln=1, fill=True)
    pdf.set_x(left_x)
    pdf.set_font("Arial", "B", 8)
    for h, w in [("Meat Type", 0.65), ("Amount", 0.35)]:
        pdf.cell(col_w * w, ch, h, 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    for name, val in meat_types:
        pdf.set_x(left_x)
        pdf.cell(col_w * 0.65, ch, name, 1)
        pdf.cell(col_w * 0.35, ch, str(int(val) if val else 0), 1)
        pdf.ln(ch)
    left_end_y = pdf.get_y()

    # --- VEG PREP LOGIC ---
    def get_batch_total(recipe_name, ing, from_subsection=False):
        rec = meal_recipes.get(recipe_name)
        if not rec:
            return 0
        tot_meals = meal_totals.get(recipe_name.upper(), 0)
        batch = rec.get("batch", 0)
        # If batch==0 treat as single batch
        if not from_subsection:
            qty_per_meal = rec["ingredients"].get(ing, 0)
        else:
            qty_per_meal = rec["sub_section"]["ingredients"].get(ing, 0) if "sub_section" in rec else 0
        if batch > 0:
            batches = math.ceil(tot_meals / batch)
            batch_total = qty_per_meal * tot_meals / batch
            return batch_total * batches
        else:
            return qty_per_meal * tot_meals

    def get_batch_total_bulk(title, ing):
        for section in bulk_sections:
            if section["title"] == title:
                qty_per_meal = section["ingredients"].get(ing, 0)
                tot_meals = sum(meal_totals.get(m.upper(), 0) for m in section["meals"])
                batch_size = section.get("batch_size", 0)
                if batch_size > 0:
                    batches = math.ceil(tot_meals / batch_size)
                    batch_total = qty_per_meal * tot_meals / batch_size
                    return batch_total * batches
                else:
                    return qty_per_meal * tot_meals
        return 0

    veg_prep = [
        ("10MM DICED CARROT", get_batch_total("Lebanese Beef Stew", "Carrot")),
        ("10MM DICED POTATO (LEBO)", get_batch_total("Lebanese Beef Stew", "Potato")),
        ("10MM DICED ZUCCHINI", get_batch_total("Moroccan Chicken", "Zucchini", from_subsection=True)),
        ("5MM DICED CABBAGE", get_batch_total("Beef Chow Mein", "Cabbage")),
        ("5MM DICED CAPSICUM", get_batch_total("Shepherd's Pie", "Capsicum") + get_batch_total("Beef Burrito Bowl", "Capsicum")),
        ("5MM DICED CARROTS", get_batch_total("Shepherd's Pie", "Carrots") + get_batch_total("Beef Burrito Bowl", "Carrot")),
        ("5MM DICED CELERY", get_batch_total("Beef Chow Mein", "Celery")),
        ("5MM DICED MUSHROOMS", get_batch_total("Shepherd's Pie", "Mushroom")),
        # Fill these in if needed:
        # ("5MM DICED ONION", ... ),
        ("5MM MONGOLIAN CAPSICUM", get_batch_total("Mongolian Beef", "Capsicum")),
        ("5MM MONGOLIAN ONION", get_batch_total("Mongolian Beef", "Onion")),
        # ("5MM SLICED MUSHROOMS", ... ),
        ("BROCCOLI", get_batch_total("Chicken and Broccoli Pasta", "Broccoli")),
        ("CRATED CARROTS", get_batch_total("Spaghetti Bolognese", "Carrot")), # + Bean Nachos if present
        ("CRATED ZUCCHINI", get_batch_total("Spaghetti Bolognese", "Zucchini")),
        ("LEMON POTATO", get_batch_total_bulk("Roasted Lemon Potatoes", "Potatoes")),
        ("ROASTED POTATO", get_batch_total_bulk("Roasted Potatoes", "Roasted Potatoes")),
        ("THAI POTATOS", get_batch_total_bulk("Roasted Thai Potatoes", "Potato")),
        ("POTATO MASH", get_batch_total_bulk("Potato Mash", "Potato")),
        ("SWEET POTATO MASH", get_batch_total_bulk("Sweet Potato Mash", "Sweet Potato")),
        # For Chicken Mixing
        ("SPINACH", get_total_from_chicken_mixing("Gnocchi", "Spinach")),
        ("RED ONION", get_batch_total_bulk("Lamb Onion Marinated", "Red Onion")),
        ("PARSLEY", get_batch_total_bulk("Lamb Onion Marinated", "Parsley")),
    ]

    pdf.set_xy(right_x, curr_y)
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Veg Prep", ln=1, fill=True)
    pdf.set_x(right_x)
    pdf.set_font("Arial", "B", 8)
    for h, w in [("Veg Prep", 0.7), ("Amount", 0.3)]:
        pdf.cell(col_w * w, ch, h, 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    for name, val in veg_prep:
        pdf.set_x(right_x)
        pdf.cell(col_w * 0.7, ch, name, 1)
        pdf.cell(col_w * 0.3, ch, str(int(val) if val else 0), 1)
        pdf.ln(ch)
    right_end_y = pdf.get_y()

    return max(left_end_y, right_end_y) + pad
